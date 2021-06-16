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

	def __init__(self, master,optionFrame,row,startColumn,outcome):

		# The Canvas
		self.draw_frame = Frame(master, 
			bg="white", bd=1,
			height=Setup.HEIGHT, 
			width=int(Setup.WIDTH/2), 
			relief=RAISED)
		super().__init__(mainElement=self.draw_frame)
		self.draw_canvas= Canvas(self.draw_frame, 
			bg="white",
			height=Setup.HEIGHT, 
			width=int(Setup.WIDTH/2))
		self.draw_canvas.grid(row=0,column=0)

		padx = 1 # Var to change the padx quickly for each element

		self.toolsFrame = LabelFrame(optionFrame,text="Tools")
		self.toolsFrame.grid(row=row,column=0,sticky="w")
		# Insert several buttons in the top left frame 
		# Button to draw Line
		strImg = Setup.PATHIMG+"line"+Setup.ICONSIZE
		image = ImageTk.PhotoImage(Image.open(strImg))
		LineB = Button(self.toolsFrame, text="line", command=lambda: self.changeElement('line'),image=image,)
		LineB.grid(row=row, column=startColumn,padx=padx)
		LineB.image = image

		# Button to draw SemiCircle
		strImg = Setup.PATHIMG+"semiCircle"+Setup.ICONSIZE
		image = ImageTk.PhotoImage(Image.open(strImg))
		SemiCircleB =Button(self.toolsFrame, text="semiCircle", command=lambda: self.changeElement('semiCircle'),image=image)
		SemiCircleB.grid(row=row, column=startColumn+1,padx=padx)
		SemiCircleB.image = image

		# Button to draw Circle
		strImg = Setup.PATHIMG+"circle"+Setup.ICONSIZE
		image = ImageTk.PhotoImage(Image.open(strImg))		
		CircleB = Button(self.toolsFrame, text="circle", command=lambda: self.changeElement('circle'),image=image)
		CircleB.grid(row=row,column=startColumn+2,padx=padx)
		CircleB.image = image

		# Button to use the Eraser
		strImg = Setup.PATHIMG+"eraser"+Setup.ICONSIZE
		image = ImageTk.PhotoImage(Image.open(strImg))
		EraserB = Button(self.toolsFrame, text="eraser", command=lambda: self.changeElement('eraser'),image=image)
		EraserB.grid(row=row, column=startColumn+3,padx=padx)
		EraserB.image = image

		# Button to clear the entire canvas
		Button(self.toolsFrame, text="clear",height=1,command=self.clear).grid(row=row, column=startColumn+4,padx=padx)

		self.gridval = StringVar(value="disappear") # To start the application with the draw canvas
		Checkbutton(self.toolsFrame, text="use a grid", command=self.changeGrid,
			var=self.gridval, onvalue="appear", offvalue="disappear").grid(row=row,column=startColumn+5)
		self.element = Factory.Create('line') # At the beginning, the user can draw lines

		# Events
		self.draw_canvas.bind('<Button-1>', self.start) # Click event
		self.draw_canvas.bind('<B1-Motion>', self.motion) # Motion event
		self.draw_canvas.bind('<ButtonRelease-1>', self.end) # Release event

		self.outcome = outcome # The Outcome Canvas

	def changeGrid(self):
		pass
		
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
