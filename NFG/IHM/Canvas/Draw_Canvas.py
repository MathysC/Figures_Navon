from Elements.ElementFactory import ElementFactory as Factory
from IHM.Canvas.Ui_Canvas import Ui_Canvas
from Logic.Setup import Setup
import os


from tkinter import *
from tkinter import ttk #i had to separate both importation in order to use ttk

from PIL import Image, ImageTk
import numpy as np


class Draw_Canvas(Ui_Canvas):
	"""
	Class that implements the draw canvas and the options
	"""

	def __init__(self,master,outcome,tobind):

		padx = 1 # Var to change the padx quickly for each element

		# The left part of the interface is split in 2 parts : The draw canvas and the options

		# The Frame that contains the draw canvas
		self.draw_frame = Frame(master, 
			bg="white",
			width=int(Setup.WIDTH/2), 
			height=int(Setup.HEIGHT/2), 
			relief=RAISED)
		super().__init__(mainElement=self.draw_frame)


		# All options for the Draw Canvas are in this frame
		self.options = Frame(master=self.draw_frame)
		self.options.grid(row=0, column=0, sticky="nswe")

		## Import and Export Options 
		self.serialization = LabelFrame(self.options, text="Import / Export") # serialization frame
		self.serialization.grid(row=0, column=0, sticky="nsw")

		Button(self.serialization, text="import .DAT", command=self.importDAT, padx=padx).grid(row=0, column=0)
		Button(self.serialization, text="export as .DAT", command=self.exportDAT, padx=padx).grid(row=0, column=1)
		Button(self.serialization, text="export as Image", command=self.exportIMG, padx=padx).grid(row=0, column=2)

		## Every tools used to create a Navon's Figure are in this frame
		self.tools = LabelFrame(self.options, text="Options for preview")
		self.tools.grid(row=1, column=0, columnspan=5, sticky="we")

		### Button to choose between local character and local image
		self.currentElement= "char" # ComboBox Variable for le Local Element
		self.buttonChangeElement = Button(self.tools, text="Use a local Image",command= lambda: self.changeLocalElement(padx))
		self.buttonChangeElement.grid(row=0, column=0, columnspan=2, sticky="w")

		### Local Character (if used, the Local Image is disabled)
		self.char_var = StringVar(value="A")
		self.labelChar = Label(self.tools, text="Local char :", padx=padx)
		self.entryChar = Entry(self.tools, width=2, textvariable=self.char_var)
		self.char_var.trace("w", lambda : self.character_limit())

		### Local Image (if used, the Local Character is disabled)
		self.labelImg = Label(self.tools, text="Local Image :", padx=padx)
		self.entryImg = Button(self.tools, text="Search an Image",height=1, command = None)

		### Font
		self.font_var = StringVar(value=self.get_AllFonts()[0])
		self.lbfont = Label(self.tools, text="Font :", padx=padx) # Grid managed in self.changeLocalElement
		self.cbfonts = ttk.Combobox(self.tools, values=self.get_AllFonts(), state="readonly", width=15,textvariable=self.font_var) # ComboBox Fonts # Grid managed in self.changeLocalElement
		self.cbfonts.current(0)

		### Density
		self.density_var = IntVar(value=100)
		Label(self.tools, text="Density :", padx=padx).grid(row=1, column=0, sticky="w")
		Spinbox(self.tools, from_=1, to=100, width=4, textvariable=self.density_var, command = lambda: self.update(self.draw_canvas)).grid(row=1, column=1, padx=padx, sticky="w")

		### Size 
		self.size_var = IntVar(value=16)
		Label(self.tools, text="Size :", padx=padx).grid(row=1, column=2, sticky="w")
		self.spChar = Spinbox(self.tools, from_=1, to=100, width=4, textvariable=self.size_var, command = lambda: self.update(self.draw_canvas)) # Grid managed in self.changeLocalElement
		self.spImg = Spinbox(self.tools, from_=1, to=100, width=4) # Grid managed in self.changeLocalElement
		

		## Every Paint Tools are in this frame	
		self.paint = LabelFrame(self.options,text="Tools")
		self.paint.grid(row=2,column=0,sticky="w")

		# Checkbox for a grid that help the user to draw
		self.gridval = StringVar(value="disappear") # To start the application without a grid on the canvas
		Checkbutton(self.paint, text="Grid", command=self.changeGrid,
			var=self.gridval, onvalue="appear", offvalue="disappear").grid(row=0,column=0)

		# Button to draw Line
		strImg = Setup.PATHIMG+"line"+Setup.ICONSIZE
		image = ImageTk.PhotoImage(Image.open(strImg))
		LineB = Button(self.paint, text="line", command=lambda: self.changeElement('line'),image=image,)
		LineB.grid(row=0, column=1,padx=padx)
		LineB.image = image

		# Button to draw SemiCircle
		strImg = Setup.PATHIMG+"semiCircle"+Setup.ICONSIZE
		image = ImageTk.PhotoImage(Image.open(strImg))
		SemiCircleB =Button(self.paint, text="semiCircle", command=lambda: self.changeElement('semiCircle'),image=image)
		SemiCircleB.grid(row=0, column=2,padx=padx)
		SemiCircleB.image = image

		# Button to draw Circle
		strImg = Setup.PATHIMG+"circle"+Setup.ICONSIZE
		image = ImageTk.PhotoImage(Image.open(strImg))		
		CircleB = Button(self.paint, text="circle", command=lambda: self.changeElement('circle'),image=image)
		CircleB.grid(row=0,column=3,padx=padx)
		CircleB.image = image

		# Button to use the Eraser
		strImg = Setup.PATHIMG+"eraser"+Setup.ICONSIZE
		image = ImageTk.PhotoImage(Image.open(strImg))
		EraserB = Button(self.paint, text="eraser", command=lambda: self.changeElement('eraser'),image=image)
		EraserB.grid(row=0, column=0+4,padx=padx)
		EraserB.image = image

		# Button to clear the entire canvas
		Button(self.paint, text="clear",height=1,command=self.clear).grid(row=0, column=0+5,padx=padx)

		# The draw canvas itself
		self.draw_canvas= Canvas(self.draw_frame, 
			bg="white",
			height=int(Setup.HEIGHT),
			width=int(Setup.WIDTH/2))
		self.draw_canvas.grid(row=1,column=0) # The draw canvas is the only element in the draw_frame


		self.element = Factory.Create('line') # At the beginning, the user can draw lines
		self.outcome = outcome # The Outcome Canvas

		# Events
		self.bindCanvas()
		self.getMainElement().bind(tobind[0],tobind[1]) # bind the main func of the MainWindow to the mainElement
		self.bindallframe(self.getMainElement(),tobind[0], tobind[1]) # and bind it to all element
		self.cbfonts.bind("<<ComboboxSelected>>", lambda e: self.update(self.draw_canvas))



		self.changeLocalElement(padx)
		self.update(self.draw_canvas)

#___________________________________________________________________________________________________________________________
# Getter & Setter

	def getOutcome(self):
		return self.outcome

#___________________________________________________________________________________________________________________________
# Managing Elements 

	# Events to draw / modify / set
	def start(self, event):
		"""
		Call the function start of the current element
		:param event: the event 
		:type event: Event
		"""
		self.element.start(event=event, canvas=self.draw_canvas, draw_Canvas=self, NF=self.outcome.getNF())

	def motion(self, event):
		"""
		Call the function motion of the current element
		:param event: the event 
		:type event: Event
		"""
		self.element.motion(event=event, canvas=self.draw_canvas, NF=self.outcome.getNF())

	def end(self, event):
		"""
		Call the function end of the current element
		:param event: the event 
		:type event: Event
		"""
		self.element.end(event=event, canvas=self.draw_canvas, NF=self.outcome.getNF(), draw_canvas=self)

		# We create the next element 
		self.changeElement(self.element.getType())

	def changeElement(self, elementType):
		"""
		change the element
		:param elementType: the type of the next element wanted
		:type elementType: str
		"""
		self.element = Factory.Create(elementType)

#___________________________________________________________________________________________________________________________
# Managing Options 

	def get_AllFonts(self):
		fonts = []
		for font in os.listdir('Fonts'):
			fonts.append(font[:-4])
		return fonts

	def character_limit(self):
		if len(self.char_var.get()) > 0:
			self.char_var.set(self.char_var.get()[-1])
		self.update(self.draw_canvas)

	def changeLocalElement(self,padx):
		"""
		Make appear and disappear the options of the local element from the draw canvas
		"""

		if self.currentElement == 'char': 	# Make appear Local Character Option
			self.currentElement = "image"
			self.spImg.grid_forget()
			self.labelImg.grid_forget()
			self.entryImg.grid_forget()
			self.spChar.grid(row=1, column=3, padx=padx, sticky="w")
			self.labelChar.grid(row=0, column=2, columnspan=2, padx=padx, sticky="w")
			self.entryChar.grid(row=0, column=4, padx=padx, sticky="w")
			self.lbfont.grid(row=0, column=5, padx=padx, sticky="e")
			self.cbfonts.grid(row=0, column=6, padx=padx)
			self.buttonChangeElement.configure(text="Work in progress") # text="Use a local Image"
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

	def update(self,canvas):
		"""
		Function that will update the options of the NF  
		"""
		self.outcome.getNF().setSize(self.size_var.get())
		self.outcome.getNF().setDensity(self.density_var.get())
		self.outcome.getNF().setPolice(self.font_var.get())
		self.outcome.getNF().setChar(self.char_var.get())
		self.outcome.update(canvas)


#___________________________________________________________________________________________________________________________
# Managing Import / Export

	def importDAT(self):
		pass

	def exportDAT(self):
		pass

	def exportIMG(self):
		pass



	def final(self):
		self.outcome.getNF().final(self.draw_canvas)

#___________________________________________________________________________________________________________________________
# Managing Canvas

	def bindallframe(self,parent,event,func):
		for child in parent.winfo_children():
			self.bindallframe(child,event,func)
			child.bind(event,func)

	def changeStageFrame(self,parent,state):
		for child in parent.winfo_children():
			self.changeStageFrame(child,state)
			child.configure(state=state)

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

	def bindCanvas(self):
		self.draw_canvas.bind('<Button-1>', self.start) # Click event
		self.draw_canvas.bind('<B1-Motion>', self.motion) # Motion event
		self.draw_canvas.bind('<ButtonRelease-1>', self.end) # Release event

	def unbindCanvas(self):
		self.draw_canvas.unbind('<Button-1>') # Click event
		self.draw_canvas.unbind('<B1-Motion>') # Motion event
		self.draw_canvas.unbind('<ButtonRelease-1>') # Release event

#___________________________________________________________________________________________________________________________
# Managing Draw Canvas

	def changeGrid(self):
		if self.gridval.get() == "disappear":
			self.draw_canvas.delete(Setup.TAGGRID)
		else:
			gap = 50
			for x in range(gap, Setup.WIDTH, gap):
				self.draw_canvas.create_line(x, 0, x, Setup.HEIGHT,fill='grey', width=1,tags=Setup.TAGGRID)
			for y in range(gap, Setup.HEIGHT, gap):
				self.draw_canvas.create_line(0, y, Setup.WIDTH, y,fill='grey', width=1,tags=Setup.TAGGRID)

	def clear(self):
		"""
		Clear the canvas
		Clear the arrays of element
		"""
		self.draw_canvas.delete("all")
		self.outcome.getNF().setElements(np.array([]))
		self.outcome.clearCanvas()
		self.changeGrid()

	def clear(self):
		"""
		Clear the canvas
		Clear the arrays of element
		"""
		self.draw_canvas.delete("all")
		self.outcome.getNF().setElements(np.array([]))
		self.outcome.clearCanvas()
		self.changeGrid()