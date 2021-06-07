from IHM.elements.Element import Element
from Logic.Setup import Setup

import numpy as np
import math
import scipy.interpolate as itp


class Circle(Element):
	"""
	Class that extends Element, implements the Circle
	"""

	def __init__(self):
		super().__init__()
		self.center = np.zeros(2)
		self.radius = 0

	def getType(self):
		"""
		Getter of type 
		:return: "circle"
		:rtype: str
		"""
		return "circle"

	def getRadius(self):
		"""
		Getter of radius
		:return: the radius
		:rtype: int
		"""
		return self.radius

	def setRadius(self, newR):
		"""
		Setter of radius
		:param: newR
		:type newR: int
		"""
		self.radius = newR

	def getCenter(self):
		"""
		Getter of center
		:return: the x and y of the center
		:rtype: np.array
		"""
		return self.center

	def setCenter(self, newC):
		"""
		Setter of radius
		:param: the array of new coordonates
		:type newR: np.array
		"""
		self.center = newC

	def start(self, **kwargs):
		"""
		Start drawing a circle
		:key event: event on canvas
		:key canvas: the canvas
		:return: this method return nothing
		:rtype: None
		"""
		event = kwargs.get('event')
		canvas = kwargs.get('canvas')


		self.center = self.gather(canvas,kwargs.get('NF'),np.array([event.x,event.y])) # Find if there is any element close to this one
		# The circle begins at the click
		self.setX(0, self.center[0])
		self.setX(1, self.center[0])
		self.setY(0, self.center[1])
		self.setY(1, self.center[1])

		self.id = canvas.create_oval(
			self.getX(0), self.getY(0),
			self.getX(1), self.getY(1),
			width=1)

	def motion(self, **kwargs):
		"""
		Resize the Circle
		:key event: event on canvas
		:key canvas: the canvas
		:return: this method return nothing
		:rtype: None
		"""
		event = kwargs.get('event')
		canvas = kwargs.get('canvas')

		x, y = self.center
		point = self.gather(canvas,kwargs.get('NF'),np.array([event.x,event.y])) # Find if there is any element close to this one

		self.radius = int(math.hypot(x - point[0], y - point[1]))
		self.setX(0, x - self.radius)
		self.setY(0, y - self.radius)
		self.setX(1, x + self.radius)
		self.setY(1, y + self.radius)

		canvas.coords(self.id,
					  self.getX(0), self.getY(0),
					  self.getX(1), self.getY(1))
		# We add this element to its neighbors
		self.findNeighbors(canvas=kwargs.get('canvas'))

	def end(self, **kwargs):
		"""
		Add the line at the NF's array of circles
		:key NF: the Navon's Figure
		:type NF: NF
		:return: method return nothing
		:rtype:None
		"""
		NF = kwargs.get('NF')
		NF.addElement(self)

		# We add this element to its neighbors
		self.FinishToFindNeighbors(canvas=kwargs.get('canvas'),NF=kwargs.get('NF'))


	def getL(self):
		"""
		Function that calculates L
		this method only used one quarter of the circle because 
			the circle is created with 4 different quarter 
			instead of 1 simple circle
		"""
		angle = np.linspace(-np.pi/2,-np.pi, 10)
		x,y = self.center

		sqrtC = [(x + self.radius * np.cos(a_), 
		y + self.radius * np.sin(a_)) for a_ in angle]
		x_ = np.array([c_[0] for c_ in sqrtC])
		y_ = np.array([c_[1] for c_ in sqrtC])

		return np.cumsum(
			np.sqrt(
				np.ediff1d(x_, to_begin=0) ** 2
				+ np.ediff1d(y_, to_begin=0) ** 2))

	def interpolate(self):
		"""
		Function that calculates the interpolation of X and Y of the element
		"""
		res = np.array([])
		angle = np.array(
			[ 
			 np.linspace(-np.pi/2,-np.pi, 10), 
			 np.linspace(np.pi, np.pi/2 , 10),
			 np.linspace(np.pi/2, 0,  10),
			 np.linspace(0, -np.pi/2,  10)
			])
		x,y = self.center
		for t in angle:
			sqrtC = [(x + self.radius * np.cos(t_), 
				y + self.radius * np.sin(t_)) for t_ in t]
			x_ = [c_[0] for c_ in sqrtC]
			y_ = [c_[1] for c_ in sqrtC]
			_x_ = itp.interp1d(self.getLDiv(), x_)
			_y_ = itp.interp1d(self.getLDiv(), y_)
			res = np.append(res,[np.array([_x_,_y_])])
		return res

	def findNeighbors(self, canvas):
		"""
		Check at any point of the perimeter of this element if there is another element and therefore an intersection to create
		:param: the TKINTER Canvas
		:type canvas: TKINTER Element 
		:return: method return nothing
		:rtype: None
		"""
		
		tag = f"-{self.id}" #self.tag from element and self.id to make a personal tag
		# Reset intersections and neighbor 
		canvas.delete(tag)
		self.intersections = np.empty(0)
		self.neighbors = np.empty(0)


		# Go around the circle
		for angle in range(359):
			# Get the next point

			radian = math.radians(angle)
			point = np.array([self.center[0]+self.radius * math.cos(radian),
			 self.center[1]+self.radius * math.sin(radian)])


			# We find all element that are at this point
			find = np.array(canvas.find_overlapping(point[0]-1, point[1]-1, point[0]-1, point[1]-1))
			
			# We delete the current element from the list
			find = np.delete(find,np.where(find == self.id))

			# We delete the circles that represents intersections
			for circle in canvas.find_withtag(self.tag):
				find = np.delete(find,np.where(find == circle))

			# Delete all the same multiple value at the same point
			find = np.unique(find)
			print(find)

			#Then if there is at least another one element
			if(len(find)>=1):
				for idElement in find:
					# We create an intersection at this point
					intersection = canvas.create_oval(int(point[0]-Setup.RADIUSINTER), int(point[1]-Setup.RADIUSINTER),
						int(point[0]+Setup.RADIUSINTER), int(point[1]+Setup.RADIUSINTER),
						fill="red", outline="red", width=1,tags=self.tag+" "+tag+f" -{idElement}")

					# Then we save the outcome
					self.addIntersection(intersection)
					self.addNeighbor(idElement)

	def whereToGather(self,pointA):
		"""
		Found where to place the pointA on top of the other element
		:param: pointA
		:type pointA: np.array([ x , y ])
		:return: the new coordonates
		:rtype: np.array([ x , y ])
		"""
		xC, yC = self.center
		xA, yA = pointA

		# There are eight ways to gather a circle

		# Four are on axes 

		# If the Y are the same
		if yA == yC:
			# But the X are different
			if xA < xC:
				return np.array([xC - self.radius, yC])
			else:
				return np.array([xC + self.radius, yC])
		# If the X are the same
		elif xA == xC:
			# But the Y are different
			if yA < yC:
				return np.array([xC, yC - self.radius])
			else:
				return np.array([xC, yC + self.radius])


		# And the four last are on each side of the circle

		# PS : I don't know why for the Right part of each side i have to use the negative values of the left part of each part
		# On the top side :
		if yA < yC:
			if xA < xC:
				# "Top - Left"
				return self.findPointB(180, 90, pointA)
			else:
				# "Top - Right"
				return self.findPointB(-180, -90, pointA)

		# On the Bottom Side
		elif yA > yC:
			if xA < xC:
				# "Bottom - Left"
				return self.findPointB(90, 0, pointA)
			else:
				# "Bottom - Right"
				return self.findPointB(-90, 0, pointA)

		# If nothing above this line was used, return the pointA 
		return pointA

	def findPointB(self, angle1, angle2,pointA):
		previous = current = 9999 # Initialize previous and current value at extremely high value 
						#to begin the while loop because their is not do while loop in python
		lengthAB = 0 # The length of pointA to pointB

		while current <= previous or angle1 <= angle2:
			previous = current # Change the previous element
			radian = math.radians(angle1)
			pointB = np.array([self.center[0]+self.radius * math.cos(radian),
			 self.center[1]+self.radius * math.sin(radian)])
			angle1+=1 # Increment the angle1, 1 by 1 
			current = int(math.hypot(pointB[0] - pointA[0], pointB[1] - pointA[1])) # Calculate the length A-B

		return pointB