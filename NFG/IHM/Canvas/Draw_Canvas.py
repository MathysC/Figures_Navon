from IHM.elements.ElementFactory import ElementFactory as Factory
from IHM.Canvas.Ui_Canvas import Ui_Canvas
from Logic.Setup import Setup


from tkinter import *
from PIL import Image, ImageTk
import numpy as np


class Draw_Canvas(Ui_Canvas):
	"""
	Class that implements the draw canvas and the options
	"""

	def __init__(self, master,optionFrame,outcome):

		# The Canvas
		self.draw_canvas = Canvas(master, 
			bg="white", bd=1,
			height=Setup.HEIGHT, 
			width=int(Setup.WIDTH/2), 
			relief=RAISED)
		super().__init__(mainElement=self.draw_canvas)

		# Insert several buttons in the top left frame 
		# Button to draw Line
		strImg = Setup.PATHIMG+"line"+Setup.ICONSIZE
		image = ImageTk.PhotoImage(Image.open(strImg))
		LineB = Button(optionFrame, bg="white", text="line", command=lambda: self.changeElement('line'),image=image)
		LineB.grid(row=0, column=1)
		LineB.image = image

		# Button to draw SemiCircle
		strImg = Setup.PATHIMG+"semiCircle"+Setup.ICONSIZE
		image = ImageTk.PhotoImage(Image.open(strImg))
		SemiCircleB =Button(optionFrame, bg="white", text="semiCircle", command=lambda: self.changeElement('semiCircle'),image=image)
		SemiCircleB.grid(row=0, column=2)
		SemiCircleB.image = image

		# Button to draw Circle
		strImg = Setup.PATHIMG+"circle"+Setup.ICONSIZE
		image = ImageTk.PhotoImage(Image.open(strImg))		
		CircleB = Button(optionFrame, bg="white", text="circle", command=lambda: self.changeElement('circle'),image=image)
		CircleB.grid(row=0,column=3)
		CircleB.image = image

		# Button to use the Eraser
		strImg = Setup.PATHIMG+"eraser"+Setup.ICONSIZE
		image = ImageTk.PhotoImage(Image.open(strImg))
		EraserB = Button(optionFrame, bg="white", text="eraser", command=lambda: self.changeElement('eraser'),image=image)
		EraserB.grid(row=0, column=4)
		EraserB.image = image

		# Button to clear the entire canvas
		Button(optionFrame, bg="white", text="clear",height=1,command=self.clear).grid(row=0, column=5)

		
		self.element = Factory.Create('line') # At the beginning, the user can draw lines

		# Events
		self.draw_canvas.bind('<Button-1>', self.start) # Click event
		self.draw_canvas.bind('<B1-Motion>', self.motion) # Motion event
		self.draw_canvas.bind('<ButtonRelease-1>', self.end) # Release event

		self.outcome = outcome # The Outcome Canvas

	def changeElement(self, elementType):
		"""
		change the element
		:param elementType: the type of the next element wanted
		:type elementType: str
		"""
		self.element = Factory.Create(elementType)

	def clear(self):
		"""
		Clear the canvas
		Clear the arrays of element
		"""
		self.draw_canvas.delete("all")
		self.outcome.getNF().setElements(np.array([]))
		self.outcome.clearCanvas()

	# Events to draw / modify / set
	def start(self, event):
		"""
		Call the function start of the current element
		:param event: the event 
		:type event: Event
		"""
		self.element.start(event=event, canvas=self.draw_canvas, draw_Canvas=self, NF=self.outcome.getNF())

	def motion(self, event):
		"""
		Call the function motion of the current element
		:param event: the event 
		:type event: Event
		"""
		self.element.motion(event=event, canvas=self.draw_canvas, NF=self.outcome.getNF())

	def end(self, event):
		"""
		Call the function end of the current element
		:param event: the event 
		:type event: Event
		"""
		self.element.end(event=event, canvas=self.draw_canvas, NF=self.outcome.getNF(), draw_canvas=self)

		# We create the next element 
		self.changeElement(self.element.getType())

	def update(self):
		"""
		Function that will update the options of the NF  
		"""
		self.outcome.getNF().size = 16# int(self.fontSb.get())
		self.outcome.getNF().d = 100#int(self.densSb.get())

	def final(self):
		self.outcome.getNF().final(self.draw_canvas)


	def getOutcome(self):
		return self.outcome