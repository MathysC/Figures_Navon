from PIL import Image, ImageTk, ImageFont, ImageDraw
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


		# Menus
		mainMenu = Menu(self.mainWindow)
		self.mainWindow.config(menu=mainMenu)
		fileMenu = Menu(master=mainMenu,tearoff=0)
		mainMenu.add_cascade(label = "File", menu = fileMenu)
		saveMenu = Menu(master=fileMenu,tearoff=0)
		fileMenu.add_cascade(label = "Save As ... ", menu=saveMenu)
		fileMenu.add_separator()
		fileMenu.add_command(label = "Quit", command=self.mainWindow.quit)


		# The mainWindow is composed of 3 big parts :

		## Draw functions
		self.left_Canvas = LabelFrame(master=self.mainWindow, width=Setup.WIDTH/2, text="Draw your own Navon's Figure")
		self.left_Canvas.grid(row=0, column=0, rowspan=2, sticky="nswe")
		
		## Generator functions
		self.right_Canvas = LabelFrame(master=self.mainWindow, width=Setup.WIDTH/2, text="Generate your own Navon's Figure" )
		self.right_Canvas.grid(row=0, column=1, sticky="nswe")

		## Outcomes 
		self.outcome_Canvas = LabelFrame(master=self.mainWindow, width= Setup.WIDTH/4, text="Outcome")
		self.outcome_Canvas.grid(row=1, column=1, sticky="swe")

		### And there are 2 outcomes, the Draw one and the Generator one
		self.draw_outcome = Outcome_Canvas(self.outcome_Canvas) # The Canvas use in the right part for the draw canvas
		self.gen_outcome = Outcome_Canvas(self.outcome_Canvas) # The Canvas use in the right part for the generator canvas 


		self.draw = Draw_Canvas(master=self.left_Canvas, outcome=self.draw_outcome)
		self.draw.getMainElement().grid(row=1, column=0)


		# The right part is composed of the Generator and the outcomes of Draw Canvas and the Generator
		## Generator
		self.generator = Generator_Canvas(self.right_Canvas, self.gen_outcome)

		self.generatorByFile= LabelFrame(self.right_Canvas, text="Import a list of Navon's Figure to Generate")
		self.generatorByFile.grid(row=0, column=0)

		Button(self.generatorByFile, text="import as CSV", command=self.importCSV, padx=self.padx).grid(row=0, column=0)
		Entry(self.generatorByFile, width=50).grid(row=0, column=2, padx=self.padx)
		Button(self.generatorByFile, text="export as Images", command=self.exportCSV, padx=self.padx).grid(row=0, column=3, sticky="we")


		## Every Tools used to create a Navon's Figure in Generator Canvas
		self.toolsGen = LabelFrame(self.right_Canvas, text="Options")
		self.toolsGen.grid(row=1, column=0, columnspan=5, sticky="we")

		### Density
		Label(self.toolsGen, text="Density :", padx=self.padx).grid(row=0, column=0)
		Spinbox(self.toolsGen, from_=1, to=100, width=4).grid(row=0, column=1, padx=self.padx)

		### Size 
		Label(self.toolsGen, text="Size :", padx=self.padx).grid(row=0, column=2)
		Spinbox(self.toolsGen, from_=1, to=100, width=4).grid(row=0, column=3, padx=self.padx)

		### Font
		Label(self.toolsGen, text="Font :", padx=self.padx).grid(row=0, column=4)
		self.cbGfonts = ttk.Combobox(self.toolsGen, values=font.families(), state="readonly", width=15)
		self.cbGfonts.grid(row=0, column=5, padx=self.padx)
		self.cbGfonts.bind("<<ComboboxSelected>>", self.changeFont)

		### Checkbox to choose between local character and local image
		self.cbvDLocal = StringVar(value="Char")
		Checkbutton(self.toolsGen, text="Use a local Image", 
			var=self.cbvDLocal, onvalue="Image", offvalue="Char", 
			command= self.changeLocalDraw).grid(row=0, column=6)

		### Local Character (if used, the Local Image is disabled)
		self.labelDChar = Label(self.toolsGen, text="Local char :", padx=self.padx)
		self.entryDChar = Entry(self.toolsGen, width=2)
		self.labelDChar.grid(row=0, column=7)
		self.entryDChar.grid(row=0, column=8, padx=self.padx)


		### Local Image (if used, the Local Character is disabled)
		self.labelDImg = Label(self.toolsGen, text="Local Image :", padx=self.padx)
		self.entryDImg = Button(self.toolsGen, text="Search an Image")
		self.deleteDImg = Button(self.toolsGen, text="delete Image")

		# Bind the Enter touch with the final function
		self.mainWindow.bind('<Return>', self.final)

		# Show the draw_canvas
		self.changeCanvas()




	def changeFont(self, event=None):
		font = self.cbDfonts.get()


	def changeLocalDraw(self):
		pass

	def importCSV(self):
		pass

	def exportCSV(self):
		pass


	def changeCanvas(self, event=None):
		return
		"""
		Make appear and disappear the canvas of the application
		"""
		if self.cboxvalue.get() == 'draw': 	# Make appear DRAW CANVAS
			self.generator.getMainElement().grid_forget() # Make invisible the generator canvas
			self.gen_outcome.getMainElement().grid_forget() # Make invisible its outcome canvas
			self.draw.getMainElement().grid(row=2, column=0, columnspan=2, sticky="nsw") # Make visible the draw canvas
			self.draw_outcome.getMainElement().grid(row=0, column=0, sticky="w", rowspan=2) # Make visibile it's outcome canvas

		else:								# Make appear GENERATOR CANVAS
			self.draw.getMainElement().grid_forget() # Make invisible the draw canvas
			self.draw_outcome.getMainElement().grid_forget() # Make invisible its outcome canvas
			self.generator.getMainElement().grid(row=2, column=0, columnspan=2, sticky="nsw") # Make visible the generator canvas
			self.generator.getMainElement().grid_propagate(0) # We call this function every time the generator is displayed otherwise the element inside will be lost
			self.gen_outcome.getMainElement().grid(row=0, column=0, sticky="w", rowspan=2) # Make visibile it's outcome canvas

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

	def final(self, event=None):
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
		
