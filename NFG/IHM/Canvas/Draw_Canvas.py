from IHM.elements.ElementFactory import ElementFactory as Factory
from Logic.Setup import Setup

from IHM.elements.Line import Line
from IHM.elements.SemiCircle import SemiCircle

from tkinter import *
from PIL import Image, ImageFont, ImageDraw, ImageTk
import numpy as np


class Draw_Canvas:
	"""
	Class that implements the draw canvas and the options
	"""

	def __init__(self, master, nf,options_frame, elementType="line"):
		self.NF = nf

		## The Canvas
		self.draw_canvas = Canvas(master, bg="white",height=Setup.HEIGHT,width=Setup.WIDTH/2, relief=RIDGE, bd=1)
		self.draw_canvas.grid(row=1,column=0,sticky="nsw")
		#self.draw_canvas.place(x=70, y=0, width=Setup.WIDTH, height=Setup.HEIGHT)




		## The Frame with the options
		#self.option_frame = LabelFrame(master, text="Options", font=Setup.FONT, bd=1, bg="white")
		#self.option_frame.place(x=0, y=0, width=70, height=Setup.HEIGHT)

		self.addOptions(options_frame,1)

		## Font
		#Label(self.option_frame, width=8, bg="white", text="font").grid(row=3, column=0, columnspan=2)
		#self.fontSb = Spinbox(self.option_frame, width=8, bg="white", from_=8, to=80, textvariable=DoubleVar(value=16))
		#self.fontSb.grid(row=4, column=0, columnspan=2)
#
#		# Density
#		#Label(self.option_frame, width=8, bg="white", text="density").grid(row=5, column=0, columnspan=2)
#		#self.densSb = Spinbox(self.option_frame, width=8, bg="white", from_=10, to=100, increment=10, textvariable=DoubleVar(value=100))
		#self.densSb.grid(row=6, column=0, columnspan=2)

		# At the start, the user can draw lines
		self.element = Factory.Create(elementType=elementType)

		# Events
		# Click event
		self.draw_canvas.bind('<Button-1>', self.start)
		# Motion event
		self.draw_canvas.bind('<B1-Motion>', self.motion)
		# Release event
		self.draw_canvas.bind('<ButtonRelease-1>', self.end)


	def addOptions(self,labelFrame,startingColumn):
		"""
		test
		"""
		strImg = Setup.PATHIMG+"line"+Setup.ICONSIZE
		# Draw Line
		image = ImageTk.PhotoImage(Image.open(strImg))
		LineB = Button(labelFrame, bg="white", text="line", command=lambda: self.changeElement('line'),image=image)
		LineB.grid(row=0, column=startingColumn)
		LineB.image = image

		# Draw SemiCircle
		strImg = Setup.PATHIMG+"semiCircle"+Setup.ICONSIZE
		image = ImageTk.PhotoImage(Image.open(strImg))
		SemiCircleB =Button(labelFrame, bg="white", text="semiCircle", command=lambda: self.changeElement('semiCircle'),image=image)
		SemiCircleB.grid(row=0, column=startingColumn+1)
		SemiCircleB.image = image


		# Draw Circle
		strImg = Setup.PATHIMG+"circle"+Setup.ICONSIZE
		image = ImageTk.PhotoImage(Image.open(strImg))		
		CircleB = Button(labelFrame, bg="white", text="circle", command=lambda: self.changeElement('circle'),image=image)
		CircleB.grid(row=0,column=startingColumn+2)
		CircleB.image = image
		# Eraser
		strImg = Setup.PATHIMG+"eraser"+Setup.ICONSIZE
		image = ImageTk.PhotoImage(Image.open(strImg))
		EraserB = Button(labelFrame, bg="white", text="eraser", command=lambda: self.changeElement('eraser'),image=image)
		EraserB.grid(row=0, column=startingColumn+3)
		EraserB.image = image
		# Clear the canvas
		Button(labelFrame, bg="white", text="clear",height=1,command=self.clear).grid(row=0, column=startingColumn+4)

	def changeElement(self, elementType):
		"""
		change the element
		:param: elementType
		:type elementType: str
		"""
		self.element = Factory.Create(elementType)

	def clear(self):
		"""
		Clear the canvas
		Clear the arrays of element
		"""
		self.draw_canvas.delete("all")
		self.NF.elements = np.array([])

	# Events to draw / modify / set
	def start(self, event):
		"""
		Call the function start of the current element
		:param: event:
		:type event: Event
		"""
		self.element.start(event=event, canvas=self.draw_canvas, draw_Canvas=self, NF=self.NF)

	def motion(self, event):
		"""
		Call the function motion of the current element
		:param: event
		:type event: Event
		"""
		self.element.motion(event=event, canvas=self.draw_canvas, NF=self.NF)

	def end(self, event):
		"""
		Call the function end of the current element
		:param: event
		:type event: Event
		"""
		self.element.end(event=event, canvas=self.draw_canvas, NF=self.NF, draw_Canvas=self)
		# We create the next element 
		self.changeElement(self.element.getType())

	def update(self):
		"""
		Function that will update the options of the NF  
		"""
		self.NF.size = 16# int(self.fontSb.get())
		self.NF.d = 100#int(self.densSb.get())
