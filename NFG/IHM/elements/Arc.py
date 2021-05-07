from IHM.elements.Element import Element
import numpy as np


class Arc(Element):
	"""
	Class that extends Element, implements the Arc
	"""
	def __init__(self,coords):
		super().__init__(
			np.array([coords[0], coords[2]]),
			np.array([coords[1], coords[3]]))
		self.id = None # implement in self.start, then used to move the line

	def getType(self):
		"""
		Getter of type 
		:return: "arc"
		:rtype: str
		"""
		return "arc"

	def start(self, **kwargs):
		"""
		Start drawing an arc
		:key event: event on draw_canvas
		:key draw_canvas: the canvas
		:return: this method return nothing
		:rtype: None
		"""
		event = kwargs.get('event')
		draw_canvas = kwargs.get('draw_canvas')

		# The line begin at the click
		self.setX(0, event.x)
		self.setX(1, event.x)
		self.setY(0, event.y)
		self.setY(1, event.y)

		self.id = draw_canvas.create_arc(
			event.x, event.y,
			event.x, event.y,
			fill='black', width=1,style="arc")

	def motion(self, **kwargs):
		"""
		Change the position of the second point of the line at the cursor
		:key event: event on draw_canvas
		:key draw_canvas: the canvas
		:return: this method return nothing
		:rtype: None
		"""
		event = kwargs.get('event')
		draw_canvas = kwargs.get('draw_canvas')

		self.setX(1, event.x)
		self.setY(1, event.y)

		draw_canvas.coords(self.id,
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
		NF.lines = np.append(NF.arcs, np.array(self))
