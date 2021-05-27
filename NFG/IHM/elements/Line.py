from IHM.elements.Element import Element
import numpy as np
import scipy.interpolate as itp
import math

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
		:type event: TKINTER EVENT
		:key canvas: the canvas
		:type canvas: TKINTER CANVAS
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
		self.findNeighbors(canvas=kwargs.get('canvas'))

	def end(self, **kwargs):
		"""
		Add the line to the list of Element
		Add this line to the neighbor list of its neighbor itself
		:key NF: the Navon's Figure
		:type NF: NF
		:key canvas: the TKINTER Canvas
		:type canvas: TKINTER Element 
		:return: method return nothing
		:rtype: None
		"""
		NF = kwargs.get('NF')
		NF.addElement(self)

		# We add this element to its neighbors
		self.FinishToFindNeighbors(canvas=kwargs.get('canvas'),NF=NF)

	def getL(self):
		"""
		Function that calculates the sum (L) of the difference of square root of X and Y
		:return: the sum
		:rtype: numpy.ndarray
		"""
		return np.cumsum(
			np.sqrt(
				np.ediff1d(self.x, to_begin=0) ** 2
				+ np.ediff1d(self.y, to_begin=0) ** 2))

	def interpolate(self):
		"""
		Function that calcultates the interpolation of X and Y of the element
		:return: an array of the interpolation
		:rtype: np.array
		"""
		_x_ = itp.interp1d(self.getLDiv(), self.x)
		_y_ = itp.interp1d(self.getLDiv(), self.y)
		return np.array([_x_, _y_])


	def findNeighbors(self, **kwargs):
		"""
		Check at any point of the line if there is another element and therefore an intersection to create
		:key NF: the Navon's Figure
		:type NF: NF
		:key canvas: the TKINTER Canvas
		:type canvas: TKINTER Element 
		:return: method return nothing
		:rtype: None
		"""
		canvas = kwargs.get('canvas')
		radius = 2 # Set the radius of the circle used to represent the intersection

		""" There are three tags for intersections :
			Intersection
			-{The ID of this element}
			-{The ID of the neighbor}
	 	 Those tags are wrote with an hyphen at the beginning otherwise it will be interpreted as an id an not a tag """
		tag = f"-{self.id}" 
		
		""" Reset self.intersections and self.neighbor 
			 Because this function is used and ONLY used in self.motion
			 We must clear those elements before trying add an intersection and a neighbour
			 Because the element is not the same for each motion"""
		canvas.delete(tag) 	
		self.intersections = np.empty(0)
		self.neighbors = np.empty(0)
	
		# Calculation of th before the loop to avoid useless repetition 
		# https://stackoverflow.com/questions/22190193/finding-coordinates-of-a-point-on-a-line
		th = math.atan2(self.getY(1) - self.getY(0), self.getX(1) - self.getX(0))
		
		# For each point of the line
		for i in range(0,int(math.hypot(self.getX(0)- self.getX(1), self.getY(0)- self.getY(1))),1):
			# Get the coords of the
			point = np.array([self.getX(0) + i * math.cos(th),
			 self.getY(0) + i * math.sin(th)])

			# We find all element that are at this point
			found = np.array(canvas.find_overlapping(point[0], point[1], point[0], point[1]))
			
			# We delete the current element from the list
			found = np.delete(found,np.where(found == self.id))

			# We delete the circles that represents intersections
			for circle in canvas.find_withtag(self.tag):
				found = np.delete(found,np.where(found == circle))
				
			#Then if there is at least another one element found
			if(len(found)>=1):
				for neighbor in found:
					# We create an intersection at this point
					intersection = canvas.create_oval(int(point[0]-radius), int(point[1]-radius),
						int(point[0]+radius), int(point[1]+radius),
						fill="red", outline="red", width=1,tags=self.tag+" "+tag+f" -{neighbor}")

					# Then we save the outcome
					self.addIntersection(intersection)
					self.addNeighbor(neighbor)
