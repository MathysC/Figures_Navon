from IHM.Canvas.Ui_Canvas import Ui_Canvas
from Logic.Setup import Setup
from Logic.NF import NF


from tkinter import *
from PIL import Image, ImageDraw, ImageTk
import numpy as np


class Outcome_Canvas(Ui_Canvas):
	def __init__(self, master):
		self.nf = NF()
		self.charIm = Image.new('RGB', (int(Setup.WIDTH/2), Setup.HEIGHT-130), color='white')
		self.draw = ImageDraw.Draw(self.charIm)
		# Due to how works the Python garbage collector, i have to save the current image in a variable 
		# https://stackoverflow.com/questions/3359717/cannot-display-an-image-in-tkinter
		self.AGC = None #Anti Garbage Collector 

		# The Outcome canvas where the user can see his or her current draw
		self.out_canvas = Canvas(master ,height=Setup.HEIGHT, width=int(Setup.WIDTH/2-10), bg="white")
		super().__init__(self.out_canvas)

	def getNF(self):
		return self.nf

	def setNF(self, newNF):
		self.nf = newNF


	def getImage(self):
		return self.charIm

	def update(self, canvas):
		"""
		Reupload the image on the canvas, with every element of the NF
		.. seealso:: NF.printAllElement(draw)
		"""

		# We delete the current image
		self.clearCanvas()
		self.nf.printAllElements(self.draw, canvas) # We print all element in the new draw
		self.AGC = ImageTk.PhotoImage(self.charIm) # Save the image to upload it on the canvas
		self.out_canvas.create_image(0,0,anchor="nw",image=self.AGC) # An we put back the image on the canvas

	def addElementToIm(self,element, canvas):
		"""
		Reupload the image on the canvas, with the newest element of the NF
		.. seealso:: NF.printElement
		"""
		self.out_canvas.delete(ALL) # We delete the Image from the Canvas
		self.nf.printElement(element=element,draw = self.draw, canvas=canvas) # We add the newest element to the image
		self.AGC = ImageTk.PhotoImage(self.charIm) # Save the image to upload it on the canvas
		self.out_canvas.create_image(0,0,anchor="nw",image=self.AGC) # An we put back the image on the canvas

	def clearCanvas(self):
		self.out_canvas.delete(ALL)# We delete the Image from the Canvas
		self.charIm = Image.new('RGB', (int(Setup.WIDTH/2), Setup.HEIGHT-130), color='white') # We create a new Image
		self.draw = ImageDraw.Draw(self.charIm)  # We create a new draw 
		self.AGC = ImageTk.PhotoImage(self.charIm) # Save the image to upload it on the canvas
		self.out_canvas.create_image(0,0,anchor="nw",image=self.AGC) # An we put back the image on the canvas
