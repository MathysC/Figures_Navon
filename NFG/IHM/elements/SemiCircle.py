from IHM.elements.Element import Element
import numpy as np
import math
import scipy.interpolate as itp


class SemiCircle(Element):
	"""
	Class that extends Element, implements the Arc
	"""

	def __init__(self):
		super().__init__()
		self.center = np.zeros(2)
		self.radius = 0
		self.angle = 0

	def getType(self) -> str:
		"""
		Getter of type 
		:return: "arc"
		:rtype: str
		"""
		return "arc"

	def start(self, **kwargs):
		"""
		Start drawing an arc
		:key event: event on canvas
		:key canvas: the canvas
		:return: this method return nothing
		:rtype: None
		"""
		event = kwargs.get('event')
		canvas = kwargs.get('canvas')
		self.setX(0, event.x)
		self.setX(1, event.x)
		self.setY(0, event.y)
		self.setY(1, event.y)


		self.id = canvas.create_arc(
			event.x, event.y,
			event.x, event.y,
			fill='black', width=1, style="arc")

		self.center = np.array([event.x,event.y])

	def motion(self, **kwargs):
		"""
		Change the position of the arc
		:key event: event on canvas
		:key canvas: the canvas
		:return: this method return nothing
		:rtype: None
		"""
		event = kwargs.get('event')
		canvas = kwargs.get('canvas')
		x, y = self.center

		# Calculates the radius of the Arc
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
		self.angle = int(gamma * 180 / math.pi) if (event.y < y) else int(-gamma * 180 / math.pi)

		# Reshape the Arc
		canvas.coords(self.id,
			  self.getX(0), self.getY(0),
			  self.getX(1), self.getY(1))

		canvas.itemconfig(self.id,start=self.angle,extent=180)

	def end(self, **kwargs):
		"""
		Add the arc at the NF's array of arcs
		:key NF: the Navon's Figure
		:type NF: NF
		:return: method return nothing
		:rtype:None
		"""
		# Save this element
		NF = kwargs.get('NF')
		NF.addElement(self)

	def getL(self):
		"""
		Function that calculates L
		Calculation from M BARD
		:return: array with the sum of difference between coordonates 
		:rtype: numpy.ndarray
		"""
		# Both start and End Radians are negative for the position on the NF
		# Honestly i don't know why it didn't work with the both positive values
		start = -(self.angle * 2*np.pi / 360)
		end = -((self.angle+180) * 2*np.pi / 360)
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
		Interpolation of the arc
		Calculation from M BARD
		:return: an array with all the Xs and Ys of local letters
		:rtype: numpy.array
		"""
		x,y = self.center

		start = self.angle * 2*np.pi / 360
		end = (self.angle+180) * 2*np.pi / 360
		t = np.linspace(-start,-end,10)

		sqrtC = [(x + self.radius * np.cos(t_), 
			y + self.radius * np.sin(t_)) for t_ in t]
		x_ = [c_[0] for c_ in sqrtC]
		y_ = [c_[1] for c_ in sqrtC]
		_x_ = itp.interp1d(self.getLDiv(), x_)
		_y_ = itp.interp1d(self.getLDiv(), y_)

		return np.array([_x_,_y_])


	def findNeighbours(self, **kwargs):
		pass