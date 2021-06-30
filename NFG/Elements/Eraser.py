from Elements.Element import Element
from Logic.Setup import Setup


class Eraser(Element):
	"""
	Class that extends Element, implements the Eraser
	"""
	def __init__(self):
		super().__init__()

#___________________________________________________________________________________________________________________________
# Getter & Setter

	def getType(self):
		"""
		Getter of type 
		:return: "eraser"
		:rtype: str
		"""
		return "eraser"

#___________________________________________________________________________________________________________________________
# Management of the element on the Draw Canvas

	def start(self, **kwargs):
		"""
		Not implemented function for this element
		"""
		pass

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
		# onClick is a list of Elements found nearby the click on the canvas but only the first created among all will be used
		# onClick is a list because find_overlapping return a list
		# https://mail.python.org/pipermail/tutor/2012-November/092795.html
		onClick = canvas.find_overlapping(event[0]-1, event[1]-1, event[0]+1, event[1]+1)

		# If the mouse is on the same element
		# Remove it from the NF
		if(onClick):
			# condition to avoid lines used for the grid
			if not Setup.TAGGRID in canvas.gettags(int(onClick[0])):
				element = NF.getElementById(onClick[0])
				# https://www.kite.com/python/answers/how-to-delete-values-from-a-numpy-array-in-python#:~:text=from%20an%20array-,Use%20numpy.,that%20match%20the%20specified%20condition%20.	
				NF.removeElement(element)
					

				# Remove all the constraints from this element
				tag = f"-{element.getId()}" 

				# Remove this element as a neighbor from its neighbors themself
				for neighbor in element.getNeighbors():
					otherElement = NF.getElementById(neighbor)
					otherElement.removeNeighbor(onClick[0])
					# And remove its intersections
					otherElement.removeIntersectionsByTag(tag,canvas=canvas)
				canvas.delete(tag)		
				# Remove it from the canvas
				canvas.delete(onClick[0])
				# And finally, remove this element
				del(element)

				draw_canvas = kwargs.get('draw_canvas')
				draw_canvas.outcome.update(canvas)				

#___________________________________________________________________________________________________________________________
# Management of the creation of element on the Navon's Figure

	def getL(self):
		"""
		Not implemented function for this element
		"""
		pass

	def interpolate(self):
		"""
		Not implemented function for this element
		"""
		pass

#___________________________________________________________________________________________________________________________
# Managing of Element Intersections

	def findNeighbors(self, **kwargs):
		"""
		Not implemented function for this element
		"""
		pass

	def whereToGather(self,pointA):
		"""
		Not implemented function for this element
		"""
		pass

#___________________________________________________________________________________________________________________________

	def toString(self):
		"""
		Not implemented function for this element
		"""
		pass
