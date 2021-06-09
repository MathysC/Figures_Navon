from IHM.elements.ElementFactory import ElementFactory as Factory
from Logic.Setup import Setup

from IHM.elements.Line import Line
from IHM.elements.SemiCircle import SemiCircle

from tkinter import *
import numpy as np


class Draw_Canvas:
	"""
	Class that implements the draw canvas and the options
	"""

	def __init__(self, mainWindow, nf, elementType="line"):
		self.NF = nf

		# The Canvas
		self.draw_canvas = Canvas(mainWindow, width=Setup.WIDTH, height=Setup.HEIGHT, bg="white", relief=RIDGE, bd=1)
		self.draw_canvas.place(x=70, y=0, width=Setup.WIDTH, height=Setup.HEIGHT)

		# The Frame with the options
		self.option_frame = LabelFrame(mainWindow, text="Options", font=Setup.FONT, bd=1, bg="white")
		self.option_frame.place(x=0, y=0, width=70, height=Setup.HEIGHT)

		# Options
		# Draw Line
		Button(self.option_frame, width=3, bg="white", text="line", command=lambda: self.changeElement('line')).grid(row=0, column=0)
		# Draw SemiCircle
		Button(self.option_frame, width=3, bg="white", text="semiCircle", command=lambda: self.changeElement('semiCircle')).grid(row=0, column=1)
		# Draw Circle
		Button(self.option_frame,width=3, bg="white", text="circle", command=lambda: self.changeElement('circle')).grid(row=1,column=0)
		# Eraser
		Button(self.option_frame, width=3, bg="white", text="eraser", command=lambda: self.changeElement('eraser')).grid(row=1, column=1)

		# Clear the canvas
		Button(self.option_frame, width=8, bg="white", text="clear", command=self.clear).grid(row=2, column=0, columnspan=2)

		# Font
		Label(self.option_frame, width=8, bg="white", text="font").grid(row=3, column=0, columnspan=2)
		self.fontSb = Spinbox(self.option_frame, width=8, bg="white", from_=8, to=80, textvariable=DoubleVar(value=16))
		self.fontSb.grid(row=4, column=0, columnspan=2)

		# Density
		Label(self.option_frame, width=8, bg="white", text="density").grid(row=5, column=0, columnspan=2)
		self.densSb = Spinbox(self.option_frame, width=8, bg="white", from_=10, to=100, increment=10, textvariable=DoubleVar(value=100))
		self.densSb.grid(row=6, column=0, columnspan=2)

		# At the start, the user can draw lines
		self.element = Factory.Create(elementType=elementType)

		# Events

		# Click event
		self.draw_canvas.bind('<Button-1>', self.start)
		# Motion event
		self.draw_canvas.bind('<B1-Motion>', self.motion)
		# Release event
		self.draw_canvas.bind('<ButtonRelease-1>', self.end)


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

	# Events to draw / modify / erase
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
		self.NF.size = int(self.fontSb.get())
		self.NF.d = int(self.densSb.get())
