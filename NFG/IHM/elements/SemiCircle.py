from IHM.elements.Element import Element
from Logic.Setup import Setup
import numpy as np
import math
import scipy.interpolate as itp


class SemiCircle(Element):
	"""
	Class that extends Element, implements the Semi-Circle
	"""

	def __init__(self):
		super().__init__()
		self.center = np.zeros(2)
		self.radius = 0
		self.angle = 0 # Starting angle in degree

	def getType(self) -> str:
		"""
		Getter of type 
		:return: "semiCircle"
		:rtype: str
		"""
		return "semiCircle"

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
		Start drawing a semiCircle
		:key event: event on canvas
		:key canvas: the canvas
		:return: this method return nothing
		:rtype: None
		"""
		event = kwargs.get('event')
		canvas = kwargs.get('canvas')

		# Set the center
		self.center = np.array([event.x,event.y])
		# Set the start of the semiCircle at the cursor
		self.setX(0, event.x)
		self.setX(1, event.x)
		self.setY(0, event.y)
		self.setY(1, event.y)

		self.id = canvas.create_arc(
			event.x, event.y,
			event.x, event.y,
			fill='black', width=1, style="arc")

	def motion(self, **kwargs):
		"""
		Change the position of the semiCircle
		:key event: event on canvas
		:type event: TKINTER EVENT
		:key canvas: the canvas
		:type canvas: TKINTER CANVAS
		:return: this method return nothing
		:rtype: None
		"""
		event = kwargs.get('event')
		canvas = kwargs.get('canvas')
		x, y = self.center

		# Calculates the radius of the SemiCircle
		self.radius = int(math.hypot(x - event.x, y - event.y))
		self.setX(0, x - self.radius)
		self.setY(0, y - self.radius)
		self.setX(1, x + self.radius)
		self.setY(1, y + self.radius)

		# To calculates the correct angle We need three points :
		
		# A the point at the cursor (event)
		A = np.array([event.x,event.y])
		# B the created point at the side of the center
		B = np.array([x+self.radius,y])
		# C the Center
		C = np.array([x,y]) # I make another variable to be clear with my calculation
		
		# Function only to make the next calculation
		def lengthSquare(X, Y) -> int: 
			"""
			Calculates the square length of two points
			"""
			xDiff = X[0] - Y[0] 
			yDiff = X[1] - Y[1] 
			return xDiff * xDiff + yDiff * yDiff 		

		BC = lengthSquare(B, C) 
		AC = lengthSquare(A, C) 
		AB = lengthSquare(A, B) 
	  
		# length of sides be sqrtA, sqrtB, sqrtC 
		sqrtA = math.sqrt(BC); 
		sqrtB = math.sqrt(AC); 
		sqrtC = math.sqrt(AB); 
	  
		# From Cosine law 
		# I keept alpha and betta if needed later
		#alpha = math.acos((AC + AB - BC) /
		#					 (2 * sqrtB * sqrtC)); 
		#betta = math.acos((BC + AB - AC) / 
		#					 (2 * sqrtA * sqrtC)); 
		gamma = math.acos((BC + AC - AB) / 
							 (2 * sqrtA * sqrtB));

		#The angle may have a different value depending on the cursor position relative to the center			
		self.angle = math.degrees(gamma) if (event.y < y) else math.degrees(-gamma)

		# Reshape the Arc
		canvas.coords(self.id,
			  self.getX(0), self.getY(0),
			  self.getX(1), self.getY(1))

		canvas.itemconfig(self.id,start=self.angle,extent=180)

		self.findNeighbors(canvas=canvas)

	def end(self, **kwargs):
		"""
		Add the semiCircle at the NF's array of semiCircles
		Add this semiCircle to the neighbor list of its neighbor itself

		:key NF: the Navon's Figure
		:type NF: NF
		:key canvas: the TKINTER Canvas
		:type canvas: TKINTER Element 
		:return: method return nothing
		:rtype: None
		"""
		# Save this element
		NF = kwargs.get('NF')
		NF.addElement(self)
		self.FinishToFindNeighbors(canvas=kwargs.get('canvas'),NF=NF)

	def getL(self):
		"""
		Function that calculates the sum (L) of the difference of square root of X and Y
		:return: the sum
		:rtype: numpy.ndarray
		"""
		# Both start and End Radians are negative for the position on the NF
		# Honestly i don't know why it didn't work with the both positive values
		start = -math.radians(self.angle)
		end = -math.radians(self.angle+180)
		t = np.linspace(start,end,10)

		sqrtC = [(0 + self.radius * np.cos(t_), 1 + self.radius * np.sin(t_)) for t_ in t]
		x = [c_[0] for c_ in sqrtC]
		y = [c_[1] for c_ in sqrtC]

		return np.cumsum(
			np.sqrt(
				np.ediff1d(x, to_begin=0) ** 2
				+ np.ediff1d(y, to_begin=0) ** 2))

	def interpolate(self):
		"""
		Function that calcultates the interpolation of X and Y of the element
		:return: an array of the interpolation
		:rtype: np.array
		"""
		x,y = self.center

		start = -math.radians(self.angle)
		end = -math.radians(self.angle+180)
		t = np.linspace(start,end,10)

		sqrtC = [(x + self.radius * np.cos(t_), 
			y + self.radius * np.sin(t_)) for t_ in t]
		x_ = [c_[0] for c_ in sqrtC]
		y_ = [c_[1] for c_ in sqrtC]
		_x_ = itp.interp1d(self.getLDiv(), x_)
		_y_ = itp.interp1d(self.getLDiv(), y_)

		return np.array([_x_,_y_])

	def findNeighbors(self, canvas):
		"""
		Check at any point of the semiCircle if there is another element and therefore an intersection to create
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


		# Check every angle of the semiCircle
		for angle in range(int(self.angle),int(self.angle+180)):
			# Get the next point
			radian = math.radians(-angle)
			point = np.array([self.center[0]+self.radius * math.cos(radian),
			 self.center[1]+self.radius * math.sin(radian)])


			# We find all element that are at this point
			find = np.array(canvas.find_overlapping(point[0]-1, point[1]-1, point[0]+1, point[1]+1))
			
			# We delete the current element from the list
			find = np.delete(find,np.where(find == self.id))

			# We delete the circles that represents intersections
			for circle in canvas.find_withtag(self.tag):
				find = np.delete(find,np.where(find == circle))

			# Delete all the same multiple value at the same point
			find = np.unique(find)

			#Then if there is at least another one element
			if(len(find)>=1):
				for idElement in find:
					# We create an intersection at this point
					intersection = canvas.create_oval(int(point[0]-Setup.RADIUSINTER), int(point[1]-Setup.RADIUSINTER),
						int(point[0]+Setup.RADIUSINTER), int(point[1]+Setup.RADIUSINTER),
						fill="red", outline="red", width=1,tags=self.tag+" "+tag+f" -{idElement}")

					# Then we save the outcome
					self.addIntersection(intersection)
					self.addNeighbor(find)

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

		# As the circle, we need to found on each part of the element the pointA is nearby
		# So we can use the same function for the two different element
		
		# PS : I don't know why for the Right part of each side i have to use the negative values of the left part of each part
		# On the top side :
		if yA < yC:
			if xA < xC:
				print("Top - Left")
				return self.findPointB(180, 90, pointA)
			else:
				print("Top - Right")
				return self.findPointB(-180, -90, pointA)

		# On the Bottom Side
		elif yA > yC:
			if xA < xC:
				print("Bottom - Left")
				return self.findPointB(90, 0, pointA)
			else:
				print("Bottom - Right")
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