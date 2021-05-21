from IHM.elements.Element import Element
import numpy as np
import math
import scipy.interpolate as itp


class Arc(Element):
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
		Change the position of the second point of the line at the cursor
		:key event: event on canvas
		:key canvas: the canvas
		:return: this method return nothing
		:rtype: None
		"""
		event = kwargs.get('event')
		canvas = kwargs.get('canvas')

		x, y = self.center
		pointA = np.array([event.x,event.y]) 
		self.radius = int(math.hypot(x - pointA[0], y - pointA[1]))
		self.setX(0, x - self.radius)
		self.setY(0, y - self.radius)
		self.setX(1, x + self.radius)
		self.setY(1, y + self.radius)


		# Calculates the correct angle
		# We create a temp point, that will represents a 
		#	rectangle triangle between event, temp and center
		temp = np.array([x,pointA[1]])
		try:
			def lengthSquare(X, Y): 
			    xDiff = X[0] - Y[0] 
			    yDiff = X[1] - Y[1] 
			    return xDiff * xDiff + yDiff * yDiff 

			AB = lengthSquare(pointA,temp)
			BC = lengthSquare(temp,self.center)
			CA = lengthSquare(self.center,pointA)

			A = math.sqrt(AB)
			B = math.sqrt(BC)
			C = math.sqrt(CA)

			self.angle = int(math.acos((AB+CA-BC) / (2*A*C)) * 180 / math.pi)
		except ValueError:
			self.angle = 0

		canvas.coords(self.id,
					  self.getX(0), self.getY(0),
					  self.getX(1), self.getY(1))
		#print(f"center : x : {self.center[0]} | y : {self.center[1]}")
		#print(f"event  : x : {event.x} | y : {event.y}")

		angle = -self.angle if(event.x>self.center[0]) else self.angle 

		canvas.itemconfig(self.id,start=angle,extent=180)

	def end(self, **kwargs):
		"""
		Add the arc at the NF's array of arcs
		:key NF: the Navon's Figure
		:type NF: NF
		:return: method return nothing
		:rtype:None
		"""
		event = kwargs.get('event')

		x, y = self.center
		temp = np.array([x,event.y])

		canvas = kwargs.get('canvas')

		line = canvas.create_line(
			x, y,
			temp[0],temp[1],
			fill='blue', width=1)	

		line2 = canvas.create_line(
			x,y,
			event.x,event.y,
			fill='blue',width=1)	

		# Save this element
		NF = kwargs.get('NF')
		NF.arcs = np.append(NF.arcs, np.array(self))

		# We create the next element 
		draw_Canvas = kwargs.get('draw_Canvas')
		draw_Canvas.changeElement(self.getType())


	def getL(self):
		"""
		Function that calculates L
		"""
		radian = self.angle * np.pi / 180
		t = np.linspace(-radian,-np.pi + radian,10)
		
		c = [(0 + self.radius * np.cos(t_), 1 + self.radius * np.sin(t_)) for t_ in t]
		x = [c_[0] for c_ in c]
		y = [c_[1] for c_ in c]
		return np.cumsum(
			np.sqrt(
				np.ediff1d(x, to_begin=0) ** 2
				+ np.ediff1d(y, to_begin=0) ** 2))

	def interpolate(self):
		x,y = self.center
		radian = self.angle * np.pi / 180
		t = np.linspace(-radian,-np.pi + radian,10)
		c = [(x + self.radius * np.cos(t_), 
			y + self.radius * np.sin(t_)) for t_ in t]
		x_ = [c_[0] for c_ in c]
		y_ = [c_[1] for c_ in c]
		_x_ = itp.interp1d(self.getLDiv(), x_)
		_y_ = itp.interp1d(self.getLDiv(), y_)

		return np.array([_x_,_y_])