from IHM.elements.Element import Element
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
		:return: "line"
		:rtype: str
		"""
		return "circle"

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

		# The circle begins at the click
		self.setX(0, event.x)
		self.setX(1, event.x)
		self.setY(0, event.y)
		self.setY(1, event.y)

		self.id = canvas.create_oval(
			event.x, event.y,
			event.x, event.y,
			width=1)

		self.center = np.array([event.x,event.y])

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

		self.radius = int(math.hypot(x - event.x, y - event.y))
		self.setX(0, x - self.radius)
		self.setY(0, y - self.radius)
		self.setX(1, x + self.radius)
		self.setY(1, y + self.radius)

		canvas.coords(self.id,
					  self.getX(0), self.getY(0),
					  self.getX(1), self.getY(1))

	def end(self, **kwargs):
		"""
		Add the line at the NF's array of circles
		:key NF: the Navon's Figure
		:type NF: NF
		:return: method return nothing
		:rtype:None
		"""
		NF = kwargs.get('NF')
		NF.elements = np.append(NF.elements, np.array(self))

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

	def findNeighbours(self, **kwargs):
		pass