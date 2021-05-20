from IHM.elements.Element import Element
import numpy as np
import scipy.interpolate as itp


class Line(Element):
	"""
	Class that extends Element, implements the Line
	"""
	def __init__(self):
		super().__init__()

	def getType(self):
		"""
		Getter of type 
		:return: "line"
		:rtype: str
		"""
		return "line"

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

		# The line begin at the click
		self.setX(0, event.x)
		self.setX(1, event.x)
		self.setY(0, event.y)
		self.setY(1, event.y)

		self.id = canvas.create_line(
			event.x, event.y,
			event.x, event.y,
			fill='black', width=1)

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

		self.setX(1, event.x)
		self.setY(1, event.y)

		canvas.coords(self.id,
					  self.getX(0), self.getY(0),
					  self.getX(1), self.getY(1))

	def end(self, **kwargs):
		"""
		Add the line at the NF's array of lines
		:key NF: the Navon's Figure
		:type NF: NF
		:return: method return nothing
		:rtype:None
		"""
		NF = kwargs.get('NF')

		NF.lines = np.append(NF.lines, np.array(self))

		draw_Canvas = kwargs.get('draw_Canvas')

		# We create the next element 
		draw_Canvas.changeElement(self.getType())

	def getL(self):
		"""
		Function that calculates L
		"""
		return np.cumsum(
			np.sqrt(
				np.ediff1d(self.x, to_begin=0) ** 2
				+ np.ediff1d(self.y, to_begin=0) ** 2))

	def interpolate(self):
		"""
		Function that calcultates the interpolation of X and Y of the element
		"""
		_x_ = itp.interp1d(self.getLDiv(), self.x)
		_y_ = itp.interp1d(self.getLDiv(), self.y)
		return np.array([_x_, _y_])