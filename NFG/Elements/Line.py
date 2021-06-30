from Elements.Element import Element
from Logic.Setup import Setup

import numpy as np
import scipy.interpolate as itp
import math


class Line(Element):
	"""
	Class that extends Element, implements the Line
	"""

	def __init__(self, Xs=np.zeros(2), Ys=np.zeros(2)):
		super().__init__(Xs, Ys)
		
#___________________________________________________________________________________________________________________________
# Getter & Setter

	def getType(self):
		"""
		Getter of type 
		:return: "line"
		:rtype: str
		"""
		return "line"

#___________________________________________________________________________________________________________________________
# Management of the creation of element on the Draw Canvas

	def start(self, **kwargs):
		"""
		Start drawing a line
		:key event: event on canvas
		:key canvas: the canvas
		:return: this method return nothing
		:rtype: None
		"""
		event = kwargs.get('event')
		canvas = kwargs.get('canvas')

		point = self.gather(canvas, kwargs.get('NF'),
		                    np.array([event[0], event[1]]))  # Find if there is any element close to this one
		# The line begins at the click
		self.setX(0, point[0])
		self.setX(1, point[0])
		self.setY(0, point[1])
		self.setY(1, point[1])

		self.id = canvas.create_line(
			self.getX(0), self.getY(0),
			self.getX(1), self.getY(1),
			fill='black', width=1)

	def motion(self, **kwargs):
		"""
		Change the position of the second point of the line at the cursor
		:key event: event on canvas
		:type event: TKINTER EVENT
		:key canvas: the canvas
		:type canvas: TKINTER CANVAS
		:key NF: the Navon's Figure
		:type NF: NF
		:return: this method return nothing
		:rtype: None

		.. seealso:: self.findNeighbors
		"""
		event = kwargs.get('event')
		canvas = kwargs.get('canvas')

		point = self.gather(canvas, kwargs.get('NF'),
		                    np.array([event[0], event[1]]))  # Find if there is any element close to this one
		self.setX(1, point[0])
		self.setY(1, point[1])

		canvas.coords(self.id,
		              self.getX(0), self.getY(0),
		              self.getX(1), self.getY(1))
		self.findNeighbors(canvas=kwargs.get('canvas'))

	def end(self, **kwargs):
		"""
		Add the line to the list of Element
		Add this line to the neighbor list of its neighbor itself
		:key NF: the Navon's Figure
		:type NF: NF
		:key canvas: the TKINTER Canvas
		:type canvas: TKINTER Element 
		:return: method return nothing
		:rtype: None

		.. seealso:: self.addToNeighbors
		.. seealso:: self.determineKids
		.. seealso:: Outcome_Canvas.update()
		"""
		NF = kwargs.get('NF')
		NF.addElement(self) # Add the element to the list of element of the Navon's figure
		canvas = kwargs.get('canvas')
		# We add this element to its neighbors
		self.addToNeighbors(canvas=canvas, NF=NF) # Indiquate this element as neighbor of the neighbor it self

		# Add the element to the outcome canvas
		draw_canvas = kwargs.get('draw_canvas')
		draw_canvas.getOutcome().addElementToIm(self, canvas)

#___________________________________________________________________________________________________________________________
# Management of the creation of element on the Navon's Figure

	def getL(self) -> np.ndarray:
		"""
		Function that calculates the sum (L) of the difference of square root of X and Y
		:return: the length of the element
		:rtype: np.ndarray
		"""
		return np.cumsum(
			np.sqrt(
				np.ediff1d(self.x, to_begin=0) ** 2
				+ np.ediff1d(self.y, to_begin=0) ** 2))

	def interpolate(self) -> np.array:
		"""
		Function that calcultates the interpolation of X and Y of the element
		:return: an array of the interpolation
		:rtype: np.array
		"""
		_x_ = itp.interp1d(self.getDividedL(), self.x)
		_y_ = itp.interp1d(self.getDividedL(), self.y)
		return np.array([_x_, _y_])

#___________________________________________________________________________________________________________________________
# Managing of Element Intersections 

	def findNeighbors(self, canvas):
		"""
		Check at any point of the line if there is another element and therefore an intersection to create
		:param: the TKINTER Canvas
		:type canvas: TKINTER Element 
		:return: method return nothing
		:rtype: None
		"""

		""" There are three tags for intersections :
			Intersection
			-{The ID of this element}-{The ID of the neighbor}
		 """
		tag = f"-{self.id}"
		""" Reset self.intersections and self.neighbor 
			 Because this function is used and ONLY used in self.motion
			 We must clear those Elements before trying add an intersection and a neighbour
			 Because the element is not the same for each motion"""
		canvas.delete(tag)
		self.intersections = np.empty(0)
		self.neighbors = np.empty(0)

		# Calculation of th before the loop to avoid useless repetition 
		# https://stackoverflow.com/questions/22190193/finding-coordinates-of-a-point-on-a-line
		th = math.atan2(self.getY(1) - self.getY(0), self.getX(1) - self.getX(0))

		# For each point of the line
		for i in range(0, int(math.hypot(self.getX(0) - self.getX(1), self.getY(0) - self.getY(1))), 1):
			# Get the coords of the point
			point = np.array([self.getX(0) + i * math.cos(th),
			                  self.getY(0) + i * math.sin(th)])

			self.createNeighbors(canvas, point, tag)

		for idneighbor in self.getNeighbors():
			idneighbor = int(idneighbor)
			self.checkIntersection(canvas=canvas, idNeighbor=idneighbor)


	def whereToGather(self, pointA) -> np.array:
		"""
		Found where to place the pointA on top of the other element
		:param: pointA
		:type pointA: np.array([ x , y ])
		:return: the new coordonates
		:rtype: np.array([ x , y ])
		"""
		# To find where to place pointA on top of this element
		# We need 3 points :

		# A : the point from other element
		# B : The closest end of this line
		pointB = np.array([])

		# To find the closest end, we calculate the difference in length between each end and pointA
		LineB = int(
			math.hypot(self.getX(0) - pointA[0], self.getY(0) - pointA[1]))  # Distance from Beginning of the Line
		LineE = int(math.hypot(self.getX(1) - pointA[0], self.getY(1) - pointA[1]))  # Distance from End of the Line

		if LineB < LineE:
			pointB = np.array([self.getX(0), self.getY(0)])
		else:
			pointB = np.array([self.getX(1), self.getY(1)])

		# C : The calculate point that will be the closest to A
		pointC = np.array([])
		previous = current = 9999  # Initialize previous and current value at extremely high value
		# to begin the while loop because their is not do while loop in python
		lengthBC = 0  # The length of pointB to pointC

		# https://stackoverflow.com/questions/22190193/finding-coordinates-of-a-point-on-a-line
		th = math.atan2(self.getY(1) - self.getY(0), self.getX(1) - self.getX(0))
		while current <= previous:
			previous = current  # Change the previous element
			pointC = np.array([self.getX(0) + lengthBC * math.cos(th),
			                   self.getY(0) + lengthBC * math.sin(th)])  # Calculate pointC
			lengthBC += 1  # Increment the length, 1 by 1
			current = int(math.hypot(pointC[0] - pointA[0], pointC[1] - pointA[1]))  # Calculate the length A-C

		return pointC

#___________________________________________________________________________________________________________________________

	def toString(self):
		return f"{self.getType()} - [{self.getX(0)} {self.getY(0)} {self.getX(1)} {self.getY(1)}]"
