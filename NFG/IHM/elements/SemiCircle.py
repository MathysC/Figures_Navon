from IHM.elements.Element import Element
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


	def findNeighbors(self, **kwargs):
		"""
		Check at any point of the semiCircle if there is another element and therefore an intersection to create
		:key NF: the Navon's Figure
		:type NF: NF
		:key canvas: the TKINTER Canvas
		:type canvas: TKINTER Element 
		:return: method return nothing
		:rtype: None
		"""
		canvas = kwargs.get('canvas')
		radius = 2 # Set the radius of the circle used to represent the intersection

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
			find = np.array(canvas.find_overlapping(point[0], point[1], point[0], point[1]))
			
			# We delete the current element from the list
			find = np.delete(find,np.where(find == self.id))

			# We delete the circles that represents intersections
			for circle in canvas.find_withtag(self.tag):
				find = np.delete(find,np.where(find == circle))

			#Then if there is at least another one element
			if(len(find)>=1):
				for idElement in find:
					# We create an intersection at this point
					intersection = canvas.create_oval(int(point[0]-radius), int(point[1]-radius),
						int(point[0]+radius), int(point[1]+radius),
						fill="red", outline="red", width=1,tags=self.tag+" "+tag+f" -{idElement}")

					# Then we save the outcome
					self.addIntersection(intersection)
					self.addNeighbor(find)
