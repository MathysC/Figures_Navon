from PIL import Image, ImageTk, ImageFont, ImageDraw
from tkinter import *
from tkinter import ttk  # i had to separate both importation in order to use ttk
from tkinter import font
import math
from Logic.Setup import Setup
import numpy as np
from IHM.Canvas.Draw_Canvas import Draw_Canvas
from IHM.Canvas.Generator_Canvas import Generator_Canvas
from IHM.Canvas.Outcome_Canvas import Outcome_Canvas


class Ui_MainWindow:
	"""
	class that implements the main window of the project
	"""

	def __init__(self):
		self.mainWindow = Tk()
		# Prepare the Setup
		# We must prepare those variable at this moment because we can get information about the user's screen only by this way
		Setup.WIDTH = self.mainWindow.winfo_screenwidth() - 80
		Setup.HEIGHT = self.mainWindow.winfo_screenheight() - 80

		# Prepare variable for the HMI		
		bgLeft = bgRight = 'white'
		self.padx = 3
		self.mainWindow.title("NFG - Navon's Figure Generator")
		self.mainWindow.geometry(f"{Setup.WIDTH}x{Setup.HEIGHT}")
		self.mainWindow.state(
			'zoomed')  # Start the program with the window at its maximum size (not a fullscreen though)
		# self.mainWindow.configure(bg=bgLeft)

		# The mainWindow is composed of 3 big parts :

		## Draw functions
		self.left_Canvas = LabelFrame(master=self.mainWindow, width=Setup.WIDTH / 2, text="Draw your own global form")
		self.left_Canvas.grid(row=0, column=0, rowspan=2, sticky="nswe")

		self.left_Canvas.bind("<Button-3>", lambda e: self.changeFocus("draw"))

		## Generator functions
		self.right_Canvas = LabelFrame(master=self.mainWindow, width=Setup.WIDTH / 2,
		                               text="Generate your own Navon's Figure")
		self.right_Canvas.grid(row=0, column=1, sticky="nswe")

		self.right_Canvas.bind("<Button-3>", lambda e: self.changeFocus("generator"))

		## Outcomes
		self.outcome_Canvas = LabelFrame(master=self.mainWindow, width=Setup.WIDTH / 4, text="Outcome")
		self.outcome_Canvas.grid(row=1, column=1, sticky="swe")

		### And there are 2 outcomes, the Draw one and the Generator one
		self.draw_outcome = Outcome_Canvas(self.outcome_Canvas)  # The Canvas use in the right part for the draw canvas
		self.gen_outcome = Outcome_Canvas(
			self.outcome_Canvas)  # The Canvas use in the right part for the generator canvas

		self.draw = Draw_Canvas(master=self.left_Canvas, outcome=self.draw_outcome,
		                        tobind=np.array(["<Button-3>", lambda e: self.changeFocus('draw')]))

		self.draw.getMainElement().grid(row=1, column=0)

		# The right part is composed of the Generator and the outcomes of Draw Canvas and the Generator
		## Generator
		self.generator = Generator_Canvas(self.right_Canvas, self.gen_outcome,
		                                  tobind=np.array(["<Button-3>", lambda e: self.changeFocus('generator')]))

		## 
		# Start the app with the focus on the draw canvas
		self.changeFocus("draw")

		self.currentCanvas = "draw"

	def changeFocus(self, frame):
		"""
		Make appear and disappear the canvas of the application
		"""
		if frame == 'draw':
			self.draw.enableChildren(self.draw.getMainElement())
			self.generator.disableChildren(self.generator.getMainElement())
			self.draw_outcome.getMainElement().grid(row=0, column=0, sticky="w",
			                                        rowspan=2)  # Make visibile it's outcome canvas
			self.gen_outcome.getMainElement().grid_forget()
			self.draw.bindCanvas()
			self.currentCanvas = "draw"

		else:
			self.draw.disableChildren(self.draw.getMainElement())
			self.generator.enableChildren(self.generator.getMainElement())
			self.gen_outcome.getMainElement().grid(row=0, column=0, sticky="w",
			                                       rowspan=2)  # Make visibile it's outcome canvas
			self.draw_outcome.getMainElement().grid_forget()
			self.draw.unbindCanvas()
			self.currentCanvas = "generator"

	def limitEntry(self, limit, var):
		"""
		Limit an ttk.Entry widget 
		:param limit: the limit of the entry
		:type limit: int
		:param var: the variable associated to the Entry Widget
		:type var: tkinter.Variable
		"""
		print(f"var : {var.get()}")
		if len(var.get()) > limit:
			var.set(var.get()[:int(limit)])

	def start(self):
		"""
		Function that start the project in the main
		"""
		self.mainWindow.mainloop()
