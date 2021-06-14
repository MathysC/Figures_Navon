from IHM.elements.ElementFactory import ElementFactory as Factory
from IHM.Canvas.Ui_Canvas import Ui_Canvas # Abstract class
from Logic.Setup import Setup


from tkinter import *
from PIL import Image, ImageTk
import numpy as np

class Generator_Canvas(Ui_Canvas):
	def __init__(self,master,outcome):
		self.generatorFrame = Canvas(
			master, bd=1,
			bg="white",
			height=Setup.HEIGHT,
			width=Setup.WIDTH/2, 
			relief=RAISED)
	
		super().__init__(self.generatorFrame)

	def update(self):
		pass

	def final(self):
		pass