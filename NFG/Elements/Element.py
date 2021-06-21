from abc import ABC, abstractmethod
from Logic.Setup import Setup
import numpy as np


class Element(ABC):
	"""
	abstract class for Elements
	"""

	def __init__(self, Xs=np.zeros(2), Ys=np.zeros(2)):
		"""
		Constructor of Element
		:param: Xs
		:type Xs: np.array
		:param: Ys:
		:type Xs: np.array
		"""
		self.x = np.copy(Xs)  # All the X coordinates
		self.y = np.copy(Ys)  # All the Y coordinates
		self.id = None  # The id of the element on the draw canvas
		self.neighbors = np.array([], dtype=np.int32)
		self.intersections = np.array([], dtype=np.int32)
		self.parent = self  # At first it is his own parent, but that might change in the future
		self.kids = np.array([])  # At the start, it has no kid

	def getId(self):
		"""
		Getter of id
		:return: an id
		:rtype: int
		"""
		return self.id

	def getX(self, i):
		"""
		Getter of one value of X
		:param: i
		:type i: int
		"""
		return self.x[i]

	def setX(self, i, value):
		"""
		Setter of one value of X
		:param: i
		:type i: int
		:param: value
		:type value: int
		"""
		self.x[i] = value

	def getY(self, i):
		"""
		Getter of one value of Y
		:param: i
		:type i: int
		"""
		return self.y[i]

	def setY(self, i, value):
		"""
		Setter of one value of Y
		:param: i
		:type i: int
		:param: value
		:type value: int
		"""
		self.y[i] = value

	def getIntersectionTag(self) -> str:
		"""
		return the tag for intersection created between elements
		:return: "intersection"
		:rtype: str
		"""
		return "intersection"

	def getIntersections(self):
		return self.intersections

	def removeIntersection(self, intersection):
		self.intersections = np.delete(
			self.intersections,
			np.where(self.intersections == intersection))

	def addIntersection(self, intersection):
		self.intersections = np.append(
			self.intersections, intersection)

	def removeIntersectionsByTag(self, tag, canvas):
		for intersection in self.intersections:
			intersection = int(
				intersection)  # Cast because numpy save int32 with decimal and we need to use int without decimal
			if tag in canvas.gettags(intersection):
				self.intersections = np.delete(
					self.intersections,
					np.where(self.intersections == intersection))

	def getNeighbors(self):
		return self.neighbors

	def removeNeighbor(self, neighbor):
		self.neighbors = np.delete(
			self.neighbors,
			np.where(self.neighbors == neighbor))

	def addNeighbor(self, neighbor):
		self.neighbors = np.append(
			self.neighbors, neighbor)

	def getCoords(self) -> np.array:
		"""
		Getter of Coords
		:return coord: the array with all coordinates
		:rtype coord: np.array
		"""
		coord = np.array([])
		for i in range(0, len(self.x)):
			coord = np.append(coord, self.getX(i))
			coord = np.append(coord, self.getY(i))
		return coord

	def getParent(self):  # -> Element
		"""
		Getter of parent
		:return: the parent of this element
		:rtype: Element
		"""
		return self.parent

	def setParent(self, parent):
		"""
		Setter of parent
		:param parent: the Element parent of this element
		:type parent: Element
		"""
		self.parent = parent

	def getKids(self) -> np.array:
		return self.kids

	def addKid(self, kid):
		"""
		add a kid to the kids list
		:param kid: the kid to add
		:type kid: Element
		"""
		self.kids = np.append(
			self.kids, kid)

	def removeKid(self, kid):
		"""
		remove a kid to the kids list
		:param kid: the kid to remove
		:type kid: Element
		"""
		self.kids = np.delete(
			self.kids,
			np.where(self.kids == kid))

	# Calculation by M. BARD
	@abstractmethod
	def getL(self):
		pass

	def getDividedL(self):
		"""
		Function that calculates each value of the L array div by its last element
		:return res: the division
		:rtype: numpy.ndarray
		"""
		try:
			res = self.getL() / self.getL()[-1]
		except ValueError:
			res = np.array([0, 0])
		return res

	@abstractmethod
	def interpolate(self):
		pass

	@abstractmethod
	def getType(self):
		pass

	@abstractmethod
	def start(self, **kwargs):
		pass

	@abstractmethod
	def motion(self, **kwargs):
		pass

	@abstractmethod
	def end(self, **kwargs):
		pass

	@abstractmethod
	def findNeighbors(self, **kwargs):
		pass

	def addToNeighbors(self, canvas, NF):
		"""
		Last function called in self.end that apply change to the neighbors of this element :
		It add THIS element to the neighbor list of the neighbor itself
		And the intersections to the intersection list of the neighbor itself too
		:key NF: the Navon's Figure
		:type NF: NF
		:key canvas: the TKINTER Canvas
		:type canvas: TKINTER Element 
		:return: method return nothing
		:rtype: None
		"""
		# For each Neighbor of this element
		for neighbor in self.neighbors:
			neighbor = int(neighbor)  # Cast of the id because numpy saved it as a float
			SndElement = NF.getElementById(neighbor)
			# Add this element to its list of neighbors
			SndElement.addNeighbor(self.id)

		# For each intersection of this element
		for intersection in self.getIntersections():
			intersection = int(intersection)  # Cast of the id because numpy saved it as a float
			# Found which one are with this neighbor
			if f"-{self.id}" in canvas.gettags(intersection) and f"-{neighbor}" in canvas.gettags(intersection):
				SndElement.addIntersection(intersection)

	def gather(self, canvas, NF, pointA) -> np.array:
		"""
		Found the nearest element to gather with element, and calculate the coords where to gather both element.
		
		If there is any element nearby, calculate where the pointA will be put on top of it.
		Else, it stay where the event.xy are.
		:param NF: the Navon's Figure
		:type NF: NF
		:param canvas: the TKINTER Canvas
		:type canvas: TKINTER Element 
		:param pointA: point to be brought closer to another element
		:type pointA: np.array([ x , y ])
		:return: the new coordinates
		:rtype: np.array([ x , y ])
		... seealso:: self.whereToGather(self,pointA)
		"""
		radius = 8
		# Find the closest element of pointA
		found = np.array(canvas.find_overlapping(
			pointA[0] - radius, pointA[1] - radius,
			pointA[0] + radius, pointA[1] + radius))

		# We delete the current element from the list
		found = np.delete(found, np.where(found == self.id))

		# We delete the circles that represents intersections
		for circle in canvas.find_withtag(self.getIntersectionTag()):
			found = np.delete(found, np.where(found == circle))

		# Delete all the same multiple value at the same point
		found = np.unique(found)

		if len(found) >= 1:
			# Get the coords of the founded element
			# Even if found is composed of several element, we only use the first found
			return NF.getElementById(found[0]).whereToGather(pointA)

		return pointA

	@abstractmethod
	def whereToGather(self, pointA):
		pass
