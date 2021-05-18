from IHM.elements.Element import Element
import numpy as np

class Eraser(Element):
	"""
	Class that extends Element, implements the Eraser
	"""
	def __init__(self):
		super().__init__(np.zeros(2),np.zeros(2))
	def getType(self):
		"""
		Getter of type 
		"""
		return "eraser"

	def start(self, **kwargs):
		"""
		found the element that is clicked 
		:key event: event on canvas
		:type event: Event
		:key canvas: the canvas
		:type canvas: tkinter canvas
		:return: this method return nothing
		:rtype: None
		"""
		event = kwargs.get('event')
		canvas = kwargs.get('canvas')

		# Found the clicked element 
		# https://mail.python.org/pipermail/tutor/2012-November/092795.html

		# onClick is a list of elements found nearby the click on the canvas but only the first created among all will be used
		onClick = canvas.find_overlapping(event.x-1, event.y-1, event.x+1, event.y+1)
		# We get the first element from onClick if the list is not empty
		self.id = onClick[0] if onClick else None

	def motion(self, **kwargs):
		"""
		Not implemented function for this element
		"""
		pass


	def end(self, **kwargs):
		"""
		Remove the element if the release is on the same element as at the beginning
		:key event: event on canvas
		:type event: Event
		:key canvas: the canvas
		:type canvas: tkinter canvas
		:key NF: the Navon's Figure
		:type NF: NF
		:return: method return nothing
		:rtype:None
		"""
		event = kwargs.get('event')
		canvas = kwargs.get('canvas')
		NF = kwargs.get('NF')
		# onClick is a list of elements found nearby the click on the canvas but only the first created among all will be used
		onClick = canvas.find_overlapping(event.x-1, event.y-1, event.x+1, event.y+1)

		# If the mouse is on the same element
		if(onClick and self.id == onClick[0]):
			# Remove it from the NF
			if canvas.type(self.id) == "line":
				for line in NF.lines:
					if line.getId() == self.id:
						# https://www.kite.com/python/answers/how-to-delete-values-from-a-numpy-array-in-python#:~:text=from%20an%20array-,Use%20numpy.,that%20match%20the%20specified%20condition%20.	
						NF.lines = np.delete(NF.lines,np.where(NF.lines == line))

			elif canvas.type(self.id) == "arc":
				pass
			# Remove it from the canvas
			canvas.delete(self.id)
