from abc import ABC, abstractmethod
from Logic.Setup import Setup
import numpy as np


class Element(ABC):
	"""
	abstract class for elements
	"""
	def __init__(self, Xs=np.zeros(2), Ys=np.zeros(2)):
		"""
		Constructor of Element
		:param: Xs
		:type Xs: np.array
		:param: Ys:
		:type Xs: np.array
		"""
		self.x = np.copy(Xs)	# All the X coordonates
		self.y = np.copy(Ys) 	# All the Y coordonates
		self.id = None			# The id of the element on the draw canvas
		self.neighbors = np.array([], dtype=np.int32)
		self.tag = "intersection"
		self.intersections = np.array([],dtype=np.int32)

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

	def getIntersections(self):
		return self.intersections

	def removeIntersection(self,intersection):
		self.intersections = np.delete(
			self.intersections,
			np.where(self.intersections == intersection))

	def addIntersection(self,intersection):
		self.intersections = np.append(
			self.intersections, intersection)

	def removeIntersectionsByTag(self,tag):
		for intersection in self.intersections:
			if tag == intersection.getTag():
				self.intersections = np.delete(
				self.intersections,
				np.where(self.intersections == intersection))


	def getNeighbors(self):
		return self.neighbors

	def removeNeighbor(self,neighbor):
		self.neighbors = np.delete(
			self.neighbors,
			np.where(self.neighbors == neighbor))

	def addNeighbor(self,neighbor):
		self.neighbors = np.append(
			self.neighbors, neighbor)


	def getCoords(self):
		"""
		Getter of Coords
		"""
		coord = np.array([])
		for i in range(0,len(self.x)):
			coord = np.append(coord,self.getX(i))
			coord = np.append(coord,self.getY(i))
		return coord

	# Calculation by M. BARD
	@abstractmethod
	def getL(self):
		pass

	def getLDiv(self):
		"""
		Function that calculates each value of the L array div by its last element
		"""
		return self.getL() / self.getL()[-1]

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
	def findNeighbors(self,**kwargs):
		pass

	def FinishToFindNeighbors(self, canvas, NF):
		"""
		Last function called in self.end that apply change to the neighbors of this element
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
			neighbor = int(neighbor) # Cast of the id because numpy saved it as a float
			SndElement = NF.getElementById(neighbor)
			# Add this element to its list of neighbors
			SndElement.addNeighbor(self.id)
		
		# For each intersection of this element
		for intersection in self.getIntersections():
			intersection = int(intersection)  # Cast of the id because numpy saved it as a float
		#	 Found which one are with this neighbor
			if  f"-{self.id}" in canvas.gettags(intersection) and f"-{neighbor}" in canvas.gettags(intersection):
				SndElement.addIntersection(intersection)