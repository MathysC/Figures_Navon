from IHM.Canvas.Ui_Canvas import Ui_Canvas
from Logic.Setup import Setup
from Logic.NF import NF


from tkinter import *
from PIL import Image, ImageDraw, ImageTk
import numpy as np


class Outcome_Canvas(Ui_Canvas):
	def __init__(self, master):
		self.nf = NF()
		self.charIm = Image.new('RGB', (int(Setup.WIDTH/2), Setup.HEIGHT), color='white')
		self.draw = ImageDraw.Draw(self.charIm)
		self.AGC = None #Anti Garbage Collector
		self.PhotoIm = None
		# Frame where all parts of Outcome_Canvas will be put in
#		# The Frame where the draw Canvas and the Generator canvas will be put
#		self.canvas_frame = Frame(master,width = Setup.WIDTH,bd=2,bg="yellow")
#		self.canvas_frame.grid(row=1,column=0,sticky="nsw")
#
#		self.outcomeOptions_Frame = Frame(self.canvas_frame,width = Setup.WIDTH,bg="yellow")
#		self.outcomeOptions_Frame.grid(row=0, column=0, sticky="nsew")

		# The Outcome canvas where the user can see his or her current draw
		self.out_canvas = Canvas(master ,height=Setup.HEIGHT,width=int(Setup.WIDTH/2), bg="white")

		super().__init__(self.out_canvas)

	def getNF(self):
		return self.nf

	def setNF(self, newNF):
		self.nf = newNF

	def update(self):
		self.out_canvas.delete(ALL)
		self.nf.printAllElement(self.draw)
		self.out_canvas.create_image(self.charIm)

	def addElementToIm(self,element):
		self.out_canvas.delete(ALL)
		self.nf.printElement(element,self.draw)
		self.AGC = ImageTk.PhotoImage(self.charIm)
		print(f"{self.AGC=} \n{type(self.AGC)}")
		self.out_canvas.create_image(0,0,anchor="nw",image=self.AGC)

	def final(self):
		pass