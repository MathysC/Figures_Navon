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
		self.findNeighbours(canvas=kwargs.get('canvas'))

	def end(self, **kwargs):
		"""
		Add the line at the NF's array of lines
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


	def findNeighbours(self, **kwargs):
		"""
		Checks at any point of the line if there is another element
		"""

		canvas = kwargs.get('canvas')
		tag = self.tag+str(self.id) #self.tag from element and self.id to make a personal tag
		radius = 2

		canvas.delete(tag)
			
		self.interCircles = np.array([])
		self.neighbours = np.array([])
		# Calculation of th before the loop to avoid useless repetition 
		# https://stackoverflow.com/questions/22190193/finding-coordinates-of-a-point-on-a-line
		th = math.atan2(self.getY(1) - self.getY(0), self.getX(1) - self.getX(0))
		
		for i in range(0,int(math.hypot(self.getX(0)- self.getX(1), self.getY(0)- self.getY(1))),1):
			# Get the next point
			point = np.array([self.getX(0) + i * math.cos(th),
			 self.getY(0) + i * math.sin(th)])

			# We find all element that are at this point
			find = np.array(canvas.find_overlapping(point[0], point[1], point[0], point[1]))
			
			# We delete the current element from the list
			find = np.delete(find,np.where(find == self.id))
			
			# We delete the circles that represents intersections
			for circle in canvas.find_withtag(tag):
				find = np.delete(find,np.where(find == circle))
			
			#Then if there is at least another one element
			if(len(find)>=1):
				#We create another circle at this point
				circle = canvas.create_oval(int(point[0]-radius), int(point[1]-radius),
					int(point[0]+radius), int(point[1]+radius),
					fill="red", outline="red", width=1,tags=tag)
				self.interCircles = np.append(self.interCircles,circle)

			# Then we save the outcome
			self.neighbours = np.append(self.neighbours,find)


