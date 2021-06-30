from IHM.Canvas.Ui_Canvas import Ui_Canvas # Abstract class
from Logic.Setup import Setup
from Elements.ElementFactory import ElementFactory as Factory
from Logic.NF import NF

import numpy as np
from tkinter import *
from tkinter import ttk #i had to separate both importation in order to use ttk
from tkinter import font
from tkinter import filedialog
import os
import csv

class Generator_Canvas(Ui_Canvas):
	def __init__(self,master,outcome,tobind):

		padx = 1 # Var to change the padx quickly for each element
		# The generator is place at the top right par of the interface 

		# The Frame that will contains everything except the outcomme
		self.gen_Frame = Frame(
			master,
			width=Setup.WIDTH/2, 
			height=Setup.HEIGHT,
			relief=RAISED)
		self.gen_Frame.grid(row=0, column=0)
		super().__init__(self.gen_Frame)

		# Frame to place everything correctly
		self.fixframe = Frame(self.gen_Frame)
		self.fixframe.grid(row=0,column=0, sticky="nsw")

	## Import and Export Options 	
		# The Frame for create a lot of Navon's Figure
		self.FileGeneration = LabelFrame(self.fixframe, width=Setup.WIDTH, text="Mass Generation")
		self.FileGeneration.grid(row=0, column=1, sticky="nsw", padx=5)

		Button(self.FileGeneration, text="import as CSV", command=self.importCSV, padx=padx).grid(row=0, column=0)
		Button(self.FileGeneration, text="export as Images", command=self.exportMassIMG, padx=padx).grid(row=0, column=1, sticky="we")

		# The frame for import export ONE NF
		self.export = LabelFrame(self.fixframe, text="Export your generation")
		self.export.grid(row=0, column=2, sticky="nsw",padx=5)
		Button(self.export, text="export as CSV", command=self.exportCSV, padx=padx).grid(row=0, column=0)
		Button(self.export, text="export as Image", command=self.exportIMG, padx=padx).grid(row=0, column=1)


	# Frame for the template
		self.templateframe = LabelFrame(self.fixframe, text="Templates")
		self.templateframe.grid(row=0,column=0,sticky="nsw",padx=5)

		Label(self.templateframe, text = "Choose the global form",bg="white").grid(row=0, column=0,columnspan=2)

		self.templateform = ttk.Combobox(self.templateframe,values=self.get_AllDATs(),state="readonly")
		self.templateform.grid(row=0, column=0, sticky="nsw")
		self.templateform.current(0)

	
	## Every tools used to create a Navon's Figure are in this frame
		self.tools = LabelFrame(self.gen_Frame, text="Options for preview")
		self.tools.grid(row=1, column=0, columnspan=5, sticky="we")

	### Button to choose between local character and local image
		self.currentElement= "char" # ComboBox Variable for le Local Element
		self.buttonChangeElement = Button(self.tools, text="Use a local Image",command= lambda: self.changeLocalElement(padx))
		self.buttonChangeElement.grid(row=0, column=0, columnspan=2, sticky="w")

	### Local Character (if used, the Local Image is disabled)
		self.char_var = StringVar(value="A")
		self.labelChar = Label(self.tools, text="Local char :", padx=padx)
		self.entryChar = Entry(self.tools, width=2, textvariable=self.char_var)
		self.char_var.trace("w", lambda *arg: self.character_limit())

	### Local Image (if used, the Local Character is disabled)
		self.labelImg = Label(self.tools, text="Local Image :", padx=padx)
		self.entryImg = Button(self.tools, text="Search an Image",height=1)

	### Font
		self.font_var = StringVar(value=self.get_AllFonts()[0])
		self.lbfont = Label(self.tools, text="Font :", padx=padx) # Grid managed in self.changeLocalElement
		self.cbfonts = ttk.Combobox(self.tools, values=self.get_AllFonts(), state="readonly", width=15,textvariable=self.font_var) # ComboBox Fonts # Grid managed in self.changeLocalElement
		self.cbfonts.current(0)
		self.cbfonts.bind("<<ComboboxSelected>>", lambda e: self.update())

	### Density
		self.density_var = StringVar(value="100")
		Label(self.tools, text="Density :", padx=padx).grid(row=1, column=0, sticky="w")
		Spinbox(self.tools, from_=1, to=100, width=4, textvariable=self.density_var, command = lambda: self.update()).grid(row=1, column=1, padx=padx, sticky="w")
		self.density_var.trace("w", lambda *arg: self.update())

	### Size 
		self.size_var = StringVar(value="16")
		Label(self.tools, text="Size :", padx=padx).grid(row=1, column=2, sticky="w")
		self.spChar = Spinbox(self.tools, from_=1, to=100, width=4, textvariable=self.size_var, command = lambda: self.update()) # Grid managed in self.changeLocalElement
		self.spImg = Spinbox(self.tools, from_=1, to=100, width=4) # Grid managed in self.changeLocalElement
		self.size_var.trace("w", lambda *arg: self.update())

	# The draw canvas (that does not appear on the screen)
		self.draw_canvas= Canvas(self.gen_Frame, 
			bg="white",
			height=int(Setup.HEIGHT),
			width=int(Setup.WIDTH/2))

	# Events
		self.getMainElement().bind(tobind[0],tobind[1])
		self.bindallframe(self.getMainElement(),tobind[0], tobind[1])

		self.templateform.bind("<<ComboboxSelected>>",lambda *arg: self.updateCanvas())

	## Start the app with 
		self.outcome = outcome
		self.changeLocalElement(padx)
		self.update() # With variables initialized

#___________________________________________________________________________________________________________________________
# Getter & Setter

	def getOutcome(self):
		return self.outcome

#___________________________________________________________________________________________________________________________
# Managing Options

	def get_AllFonts(self):
		fonts = []
		for font in os.listdir(Setup.PATHFONT):
			fonts.append(font[:-4])
		return fonts

	def get_AllDATs(self):
		DATs = []
		for dat in os.listdir(Setup.PATHDAT):
			DATs.append(dat[:-4])
		return DATs

	def character_limit(self):
		if len(self.char_var.get()) > 0:
			self.char_var.set(self.char_var.get()[-1])
		self.update()

	def changeLocalElement(self,padx):
		"""
		Make appear and disappear the options of the local element from the draw canvas
		"""
		if self.currentElement == 'char': 	# Make appear Local Character Option
			self.spImg.grid_forget()
			self.labelImg.grid_forget()
			self.entryImg.grid_forget()
			self.spChar.grid(row=1, column=3, padx=padx, sticky="w")
			self.labelChar.grid(row=0, column=2, columnspan=2, padx=padx, sticky="w")
			self.entryChar.grid(row=0, column=4, padx=padx, sticky="w")
			self.lbfont.grid(row=0, column=5, padx=padx, sticky="e")
			self.cbfonts.grid(row=0, column=6, padx=padx)
			self.buttonChangeElement.configure(text="Work in progress") # text="Use a local Image"
			self.currentElement = "image"
		else:								# Make appear Local Image Option
			self.currentElement = "char"
			self.buttonChangeElement.configure(state=DISABLED)

			return							
			self.spChar.grid_forget()
			self.cbfonts.grid_forget()
			self.lbfont.grid_forget()
			self.labelChar.grid_forget()
			self.entryChar.grid_forget()
			self.spImg.grid(row=1, column=3, padx=padx, sticky="w")
			self.labelImg.grid(row=0, column=2, columnspan=2, sticky="w")
			self.entryImg.grid(row=0, column=4, sticky="w")
			self.buttonChangeElement.configure(text="Use local Character")

	def update(self):
		"""
		Function that will update the options of the NF  
		"""
		self.outcome.getNF().setPolice(self.font_var.get())
		self.outcome.getNF().setChar(self.char_var.get())
		try:
		 # The code still work without the try except clause but it create an exception when we change value by typing it
			self.outcome.getNF().setDensity(int(self.density_var.get()))
			self.outcome.getNF().setSize(int(self.size_var.get()))
		except ValueError:
			pass
		self.outcome.update(self.draw_canvas)

	def updateCanvas(self):
			file = open(Setup.PATHDAT+self.templateform.get()+Setup.FORMATDAT,"r")

			self.draw_canvas.delete("all")
			self.outcome.getNF().setElements(np.array([]))
			self.outcome.clearCanvas()
			print(f"len Elements : {len(self.outcome.getNF().getElements())}")
			for line in file:
				print(f"{line=}")
				info = line[:-1].split(" - ") # [:-1] to remove the '\n' from the line
				element = Factory.Create(info[0])
				if info[0] == 'line':
					# A line is registered this way : "type" "coord"
					coords = [float(i) for i in info[1][1:-1].split(" ")]
					element.start(event=[coords[0],coords[1]],canvas=self.draw_canvas, draw_Canvas=self, NF=self.outcome.getNF())
					element.motion(event=[coords[2],coords[3]], canvas=self.draw_canvas, NF=self.outcome.getNF())
					element.end(event=[coords[2],coords[3]], canvas=self.draw_canvas, NF=self.outcome.getNF(), draw_canvas=self)
				elif info[0] == 'semiCircle':
					# A semiCircle is registered this way : "type" "center" "radius" "startAngle"
					center = [float(i) for i in info[1][1:-1].split(" ")]
					radius = int(info[2])
					startAngle = float(info[3])
					element.start(event=center,canvas=self.draw_canvas, draw_Canvas=self, NF=self.outcome.getNF())
					element.motion(event=center, canvas=self.draw_canvas, NF=self.outcome.getNF(), radius=radius, startAngle=startAngle)
					element.end(event=center, canvas=self.draw_canvas, NF=self.outcome.getNF(), draw_canvas=self)
				elif info[0] == 'circle':
					# A circle is registered this way : "type" "center" "radius"
					center = [float(i) for i in info[1][1:-1].split(" ")]
					radius = int(info[2])
					element.start(event=center,canvas=self.draw_canvas, draw_Canvas=self, NF=self.outcome.getNF())
					element.motion(event=center, canvas=self.draw_canvas, NF=self.outcome.getNF(), radius=radius)
					element.end(event=center, canvas=self.draw_canvas, NF=self.outcome.getNF(), draw_canvas=self)
				

#___________________________________________________________________________________________________________________________
# Managing Import / Export

	def importCSV(self):
		pass

	def exportCSV(self):
		pass

	def exportMassIMG(self):
		pass

	def exportIMG(self):
		file = filedialog.asksaveasfilename ( title = "Save as .." , \
			filetypes = [("PNG", ".png"), ("JPG", ".jpg")] , defaultextension = ".png", \
			initialdir= "Outcome", initialfile="NewImage")
		if not len(filepath) == 0:
			self.getOutcome().getImage().save(file)

#___________________________________________________________________________________________________________________________
# Managing Canvas

	def bindallframe(self,parent,event,func):
		for child in parent.winfo_children():
			self.bindallframe(child,event,func)
			child.bind(event,func)

	# https://stackoverflow.com/questions/24942760/is-there-a-way-to-gray-out-disable-a-tkinter-frame
	def disableChildren(self,parent):
	    for child in parent.winfo_children():
	        wtype = child.winfo_class()
	        if wtype not in ('Frame','Labelframe'):
	            child.configure(state='disable')
	        else:
	            self.disableChildren(child)

	def enableChildren(self,parent):
	    for child in parent.winfo_children():
	        wtype = child.winfo_class()
	        if wtype not in ('Frame','Labelframe'):
	            child.configure(state='normal')
	        else:
	            self.enableChildren(child)