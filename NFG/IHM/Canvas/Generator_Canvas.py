from IHM.elements.ElementFactory import ElementFactory as Factory
from IHM.Canvas.Ui_Canvas import Ui_Canvas # Abstract class
from Logic.Setup import Setup


from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np

class Generator_Canvas(Ui_Canvas):
	def __init__(self,master,outcome):
		self.generatorFrame = Frame(
			master, bd=1,
			bg="white",
			height=Setup.HEIGHT,
			width=Setup.WIDTH/2, 
			relief=RAISED)
		self.generatorFrame.grid_propagate(0)
		Label(self.generatorFrame, text = "Choose the global form",bg="white").grid(row=0, column=0,columnspan=2)

		comboForm = ttk.Combobox(self.generatorFrame,values=["A","B"],state="readonly")
		comboForm.grid(row=0, column=3)
		comboForm.current(1)
		comboForm.bind("<<ComboboxSelected>>",self.func)
		super().__init__(self.generatorFrame)


	def func(self,event=None):
		print("selected")

	def update(self):
		pass

	def final(self):
		pass