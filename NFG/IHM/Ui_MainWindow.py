from PIL import Image, ImageFont, ImageDraw
from tkinter import *
import tkinter.ttk
from PIL import Image, ImageTk
import math
from Logic.Setup import Setup

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
		Setup.WIDTH = self.mainWindow.winfo_screenwidth()-80
		Setup.HEIGHT = self.mainWindow.winfo_screenheight()-80
		
		self.mainWindow.title("NFG - Navon's Figure Generator")
		self.mainWindow.geometry(f"{Setup.WIDTH}x{Setup.HEIGHT}")
		self.mainWindow.state('zoomed') # Start the program with the window at its maximum size (not a fullscreen though)

		# Menus
		mainMenu = Menu(self.mainWindow)
		self.mainWindow.config(menu=mainMenu)
		fileMenu = Menu(master=mainMenu,tearoff=0)
		mainMenu.add_cascade(label = "File", menu = fileMenu)
		saveMenu = Menu(master=fileMenu,tearoff=0)
		fileMenu.add_cascade(label = "Save As ... ", menu=saveMenu)
		fileMenu.add_separator()
		fileMenu.add_command(label = "Quit", command=self.mainWindow.quit)

		# We create Frames and Canvas
		bg = "white"
		# Right part of the window, where differents options are (font, size, image etc) and the current outcome of the Navon's Figure
		self.options_RightCanvas = Frame(self.mainWindow,width = Setup.WIDTH/2, bg=bg, bd=1, relief=RAISED) # The option frame at the top right
		self.options_RightCanvas.grid(row=0,column=1,sticky="nsew")


		self.right_Canvas = Frame(master=self.mainWindow,width = Setup.WIDTH/2, bg=bg) # The Canvas frame at the right bottom~
		self.right_Canvas.grid(row=1,column=1)

		self.draw_outcome = Outcome_Canvas(self.right_Canvas) # The Canvas use in the right part for the draw canvas 
		self.gen_outcome = Outcome_Canvas(self.right_Canvas) # The Canvas use in the right part for the generator canvas 


		# The Frame where the draw Canvas and the Generator canvas will be put
		self.left_Canvas = Frame(self.mainWindow,width = Setup.WIDTH/2,bg=bg) # The Canvas frame at the left bottom~
		self.left_Canvas.grid(row=1,column=0,sticky="nsw")


		# Options part where buttons for the Draw Canvas and the switch canvas will be put
		self.options_LeftCanvas = Frame(self.mainWindow,width = Setup.WIDTH/2, bg=bg, bd=1, relief=RAISED) # The option frame at the top left
		self.options_LeftCanvas.grid(row=0,column=0,sticky="nsew")

		# The switch between Draw Canvas and Generator Canvas
		self.cboxvalue = StringVar(value='draw') # To start the application with the draw canvas
		self.checkbox =Checkbutton(master=self.options_LeftCanvas,
			text="Use Draw Canvas",bg=bg,
			var=self.cboxvalue, onvalue='draw', offvalue='generator', 
			command=self.changeCanvas)
		self.checkbox.grid(row=0,column=0)

		self.draw = Draw_Canvas(self.left_Canvas,self.options_LeftCanvas,self.draw_outcome) # the Draw part and the options
		self.generator = Generator_Canvas(self.left_Canvas,self.gen_outcome) # The Generator part
	
		# Bind the Enter touch with the final function
		self.mainWindow.bind('<Return>',self.final)

		# Show the draw_canvas
		self.changeCanvas()

	def changeCanvas(self,event=None):
		"""
		Make appear and disappear the canvas of the application
		"""
		if self.cboxvalue.get() == 'draw':
			self.generator.getMainElement().grid_forget() # Make invisible the generator canvas
			self.gen_outcome.getMainElement().grid_forget() # Make invisible its outcome canvas
			self.draw.getMainElement().grid(row=2,column=0,columnspan=2,sticky="nsw") # Make visible the draw canvas
			self.draw_outcome.getMainElement().grid(row=0,column=0,sticky="w",rowspan=2) # Make visibile it's outcome canvas

		else:
			self.draw.getMainElement().grid_forget() # Make invisible the draw canvas
			self.draw_outcome.getMainElement().grid_forget() # Make invisible its outcome canvas
			self.generator.getMainElement().grid(row=2, column=0, columnspan=2, sticky="nsw") # Make visible the generator canvas
			self.gen_outcome.getMainElement().grid(row=0,column=0,sticky="w",rowspan=2) # Make visibile it's outcome canvas

	def start(self):
		"""
		Function that start the project in the main
		"""
		self.mainWindow.mainloop()

	def final(self,event=None):
		"""
		Function that (currently only ) preview the NF
		"""
		if self.cboxvalue.get() == 'draw':
			self.draw.update()
			self.draw.final()
			#self.NF.finalImage(self.canvas['draw'].draw_canvas)
		else:
			self.generator.update()
			self.generator.final()
		
