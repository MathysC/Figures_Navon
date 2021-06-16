from PIL import Image,ImageTk, ImageFont, ImageDraw
from tkinter import *
from tkinter import ttk #i had to separate both importation in order to use ttk
from tkinter import font
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

		# Prepare variable for the HMI		
		bgLeft = bgRight ='white'
		self.padx = 3
		self.mainWindow.title("NFG - Navon's Figure Generator")
		self.mainWindow.geometry(f"{Setup.WIDTH}x{Setup.HEIGHT}")
		self.mainWindow.state('zoomed') # Start the program with the window at its maximum size (not a fullscreen though)
		#self.mainWindow.configure(bg=bgLeft)


		# The mainWindow is composed of 3 big parts :

		## Draw functions
		self.left_Canvas = LabelFrame(master=self.mainWindow, width=Setup.WIDTH/2, text="Draw your own Navon's Figure")
		self.left_Canvas.grid(row=0,column=0,rowspan=2)
		
		## Generator functions
		self.right_Canvas = LabelFrame(master=self.mainWindow, width=Setup.WIDTH/2, text="Generate your Navon's Figure" )
		self.right_Canvas.grid(row=0,column=1)

		## Outcomes 
		self.outcome_Canvas = LabelFrame(master=self.mainWindow, width= Setup.WIDTH/4, text="Outcome")
		self.outcome_Canvas.grid(row=1,column=1)

		### And there are 2 outcomes, the Draw one and the Generator one
		self.draw_outcome = Outcome_Canvas(self.outcome_Canvas) # The Canvas use in the right part for the draw canvas 
		self.gen_outcome = Outcome_Canvas(self.outcome_Canvas) # The Canvas use in the right part for the generator canvas 

		## Generator
		self.generator = Generator_Canvas(self.right_Canvas, self.gen_outcome)

		# The left part is split in 2 parts : The draw canvas and the options
		self.left_options = Frame(self.left_Canvas)
		self.left_options.grid(row=0,column=0,sticky="nswe")

		### Import and Export Options 
		self.serializationDraw = LabelFrame(self.left_options, text="Import / Export")
		self.serializationDraw.grid(row=0,column=0,columnspan=2,sticky="nswe")

		Button(self.serializationDraw, text="import draw", command=self.importDraw,padx=self.padx).grid(row=0,column=0)
		Entry(self.serializationDraw,width=50).grid(row=0, column=2, padx=self.padx)
		Button(self.serializationDraw, text="export draw", command=self.exportDraw,padx=self.padx).grid(row=0, column=3, sticky="we")

		## Every Tools used to create a Navon's Figure
		self.toolsDraw = LabelFrame(self.left_options, text="Options")
		self.toolsDraw.grid(row=1, column=0, columnspan=5, sticky="we")

		### Density
		Label(self.toolsDraw, text="Density :",padx=self.padx).grid(row=0, column=0)
		Spinbox(self.toolsDraw, from_=1, to=100, width=4).grid(row=0, column=1,padx=self.padx)

		### Size 
		Label(self.toolsDraw, text="Size :",padx=self.padx).grid(row=0, column=2)
		Spinbox(self.toolsDraw, from_=1, to=100, width=4).grid(row=0, column=3,padx=self.padx)

		### Font
		Label(self.toolsDraw, text="Font :",padx=self.padx).grid(row=0, column=4)
		self.cbfonts = ttk.Combobox(self.toolsDraw,values=font.families(), state="readonly",width=15)
		self.cbfonts.grid(row=0, column=5,padx=self.padx)
		self.cbfonts.bind("<<ComboboxSelected>>", self.changeFont)

		### Checkbox to choose between local character and local image
		self.cbvLocal = StringVar(value="Char")
		Checkbutton(self.toolsDraw, text="Use a local Image",
			var=self.cbvLocal, onvalue="Image", offvalue="Char", 
			command= self.changeLocalElement).grid(row=0,column=6)

		### Local Character (if used, the Local Image is disabled)
		self.labelChar = Label(self.toolsDraw, text="Local char :",padx=self.padx)
		self.entryChar = Entry(self.toolsDraw, width=2)
		self.labelChar.grid(row=0, column=7)
		self.entryChar.grid(row=0, column=8,padx=self.padx)


		### Local Image (if used, the Local Character is disabled)
		self.labelImg = Label(self.toolsDraw, text="Local Image :",padx=self.padx)
		self.entryImg = Button(self.toolsDraw,text="Search an Image")
		self.deleteImg = Button(self.toolsDraw,text="delete Image")

		self.draw = Draw_Canvas(master=self.left_Canvas,optionFrame=self.left_options, row=2, startColumn=0, outcome=self.draw_outcome)
		self.draw.getMainElement().grid(row=1,column=0)

		# Bind the Enter touch with the final function
		self.mainWindow.bind('<Return>',self.final)

		# Show the draw_canvas
		self.changeCanvas()


	def changeFont(self,event=None):
		font = self.cbfonts.get()
	def changeLocalElement(self):
		"""
		Make appear and disappear the canvas of the application
		"""
		if self.cbvLocal.get() == 'Char': 	# Make appear Local Character Option
			self.labelImg.grid_forget() 
			self.entryImg.grid_forget()
			self.deleteImg.grid_forget()
			self.labelChar.grid(row=0, column=7)
			self.entryChar.grid(row=0, column=8,padx=self.padx)

		else:								# Make appear Local Image Option
			self.labelImg.grid(row=0, column=9)
			self.entryImg.grid(row=0, column=10,padx=self.padx)
			self.deleteImg.grid(row=0, column=11,padx=self.padx)
			self.labelChar.grid_forget()
			self.entryChar.grid_forget()

	def importDraw(self):
		pass

	def exportDraw(self):
		pass

	def changeCanvas(self,event=None):
		return
		"""
		Make appear and disappear the canvas of the application
		"""
		if self.cboxvalue.get() == 'draw': 	# Make appear DRAW CANVAS
			self.generator.getMainElement().grid_forget() # Make invisible the generator canvas
			self.gen_outcome.getMainElement().grid_forget() # Make invisible its outcome canvas
			self.draw.getMainElement().grid(row=2,column=0,columnspan=2,sticky="nsw") # Make visible the draw canvas
			self.draw_outcome.getMainElement().grid(row=0,column=0,sticky="w",rowspan=2) # Make visibile it's outcome canvas

		else:								# Make appear GENERATOR CANVAS
			self.draw.getMainElement().grid_forget() # Make invisible the draw canvas
			self.draw_outcome.getMainElement().grid_forget() # Make invisible its outcome canvas
			self.generator.getMainElement().grid(row=2, column=0, columnspan=2, sticky="nsw") # Make visible the generator canvas
			self.generator.getMainElement().grid_propagate(0) # We call this function every time the generator is displayed otherwise the element inside will be lost
			self.gen_outcome.getMainElement().grid(row=0,column=0,sticky="w",rowspan=2) # Make visibile it's outcome canvas

	def limitEntry(self,limit,var):
		"""
		Limit an ttk.Entry widget 
		:param limit: the limit of the entry
		:type limit: int
		:param var: the variable associated to the Entry Widget
		:type var: tkinter.Variable
		"""
		print("lol")
		print(f"var : {var.get()}")
		if len(var.get()) > limit: 
			var.set(var.get()[:int(limit)])

	def start(self):
		"""
		Function that start the project in the main
		"""
		self.mainWindow.mainloop()

	def final(self,event=None):
		"""
		Function that (currently only ) preview the NF
		.. seealso:: Draw_Canvas.update()
		.. seealso:: Draw_Canvas.final()
		.. seealso:: Generator_Canvas.update()
		.. seealso:: Generator_Canvas.final()
		"""
		if self.cboxvalue.get() == 'draw':
			self.draw.update()
			self.draw.final()
			#self.NF.finalImage(self.canvas['draw'].draw_canvas)
		else:
			self.generator.update()
			self.generator.final()
		
