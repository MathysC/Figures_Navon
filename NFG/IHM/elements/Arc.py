from IHM.elements.Element import Element
import numpy as np


class Arc(Element):
	"""
	Class that extends Element, implements the Arc
	"""

	def __init__(self):
		super().__init__(Xs=np.zeros(3), Ys=np.zeros(3))
		self.current = 0

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
		x = y = 0
		if (self.current == 0):
			self.setX(self.current, event.x)
			self.setY(self.current, event.y)

			self.id = canvas.create_line(
				event.x, event.y,
				event.x, event.y,
				fill='black', width=1, smooth=1)

		"""
		# The line begin at the click
		self.setX(0, event.x)
		self.setX(1, event.x)
		self.setY(0, event.y)
		self.setY(1, event.y)

		self.id = canvas.create_arc(
			event.x, event.y,
			event.x, event.y,
			width=1,style="arc",start="45")
		"""

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

		self.setX(2 - self.current, event.x)
		self.setY(2 - self.current, event.y)
		if (self.current == 0):
			canvas.coords(self.id,
						  self.getX(0), self.getY(0),
						  self.getX(2), self.getY(2))
		else:
			canvas.coords(self.id,
						  self.getX(0), self.getY(0),
						  self.getX(1), self.getY(1),
						  self.getX(2), self.getY(2))

	def end(self, **kwargs):
		"""
		Add the arc at the NF's array of arcs
		:key NF: the Navon's Figure
		:type NF: NF
		:return: method return nothing
		:rtype:None
		"""

		if (self.current == 0):
			self.current = 1
		else:
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
		t = np.linspace(-np.pi / 2, np.pi / 2, 10)
		r = np.sqrt(1.0)
		c = [(0 + r * np.cos(t_), 1 + r * np.sin(t_)) for t_ in t]
		x3 = [c_[0] for c_ in c]
		y3 = [c_[1] for c_ in c]
		return np.cumsum(
			np.sqrt(
				np.ediff1d(x3, to_begin=0) ** 2
				+ np.ediff1d(y3, to_begin=0) ** 2))