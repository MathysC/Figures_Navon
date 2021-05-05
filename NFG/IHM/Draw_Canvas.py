from IHM.elements.ElementFactory import ElementFactory as Factory
from Logic.Setup import Setup

from IHM.elements.Line import Line

from tkinter import *
import numpy as np

class Draw_Canvas:
	"""
	Class that implements the draw canvas and the options
	"""
	def __init__(self, mainWindow, nf,elementType="line"):
		self.NF = nf

		# The Canvas
		self.draw_canvas = Canvas(mainWindow, width=Setup.WIDTH, height=Setup.HEIGHT, bg="white",relief=RIDGE,bd=1)
		self.draw_canvas.place(x=70,y=0,width=Setup.WIDTH,height=Setup.HEIGHT)

		# The Frame with the options 
		self.option_frame = LabelFrame(mainWindow,text="Options",font=Setup.FONT,bd=1,bg="white")
		self.option_frame.place(x=0,y=0,width=70,height=Setup.HEIGHT) 

		# Options
		# Draw Line
		Button(self.option_frame, width=3, bg="white",text="line", command=lambda :self.changeElement('line')).grid(row=0,column=0)
		# Draw arc (CURRENTLY EMPTY)
		Button(self.option_frame, width=3, bg="white",text="arc", command=self.test).grid(row=0,column=1)

		# Eraser
		Button(self.option_frame,width=3,bg="white",text="eraser",command=lambda :self.changeElement('eraser')).grid(row=1,column=0)

		# Clear the canvas
		Button(self.option_frame,width=8,bg="white",text="clear",command=self.clear).grid(row=2,column=0,columnspan=2)

		# Font
		self.fontSb = Spinbox(self.option_frame,width=8,bg="white",text="fontSize",from_=8,to=80,textvariable=16,command=self.changeSize).grid(row=3,column=0,columnspan=2)


		# At the start, the user can draw lines
		self.element = Factory.Create('line')

		#Events 

		# Click event
		self.draw_canvas.bind('<Button-1>', self.start)
		# Motion event
		self.draw_canvas.bind('<B1-Motion>', self.motion)
		# Release event 
		self.draw_canvas.bind('<ButtonRelease-1>', self.end)


	def changeElement(self,elementType):
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
		self.NF.lines = np.array([])
		self.NF.arcs = np.array([])

	def changeSize(self):
		print(self.fontSb.get())
		self.NF.size = int(self.fontSb.get())

	#Events to draw / modify / erase
	def start(self, event):
		"""
		Call the function start of the current element
		:param: event:
		:type event: Event
		"""
		self.element.start(event=event, draw_canvas=self.draw_canvas)        

	def motion(self, event):
		"""
		Call the function motion of the current element
		:param: event
		:type event: Event
		"""
		self.element.motion(event=event, draw_canvas=self.draw_canvas)

	def end(self, event):
		"""
		Call the function end of the current element
		:param: event
		:type event: Event
		"""
		self.element.end(event=event,draw_canvas=self.draw_canvas, NF=self.NF)
		# We create the next element 
		self.element = Factory.Create(self.element.getType())

	def update(self):
		pass

	def test(self,event=None):
		print(f"canvas :{self.draw_canvas.find_all()}")
