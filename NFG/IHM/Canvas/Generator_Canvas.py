from IHM.elements.ElementFactory import ElementFactory as Factory
from IHM.Canvas.Ui_Canvas import Ui_Canvas # Abstract class
from Logic.Setup import Setup


from tkinter import *
from tkinter import ttk #i had to separate both importation in order to use ttk
from tkinter import font

from PIL import Image, ImageTk
import numpy as np

class Generator_Canvas(Ui_Canvas):
	def __init__(self,master,outcome,tobind):

		padx = 1 # Var to change the padx quickly for each element
		# The generator is place at the top right par of the interface 

		# The Frame that will contains everything except the outcomme
		self.gen_Frame = Frame(
			master,
			width=Setup.WIDTH/2-1, 
			height=Setup.HEIGHT,
			relief=RAISED)
		self.gen_Frame.grid(row=0, column=0)
		super().__init__(self.gen_Frame)

		self.fixframe = Frame(self.gen_Frame)
		self.fixframe.grid(row=0,column=0, sticky="nsw")

		# The Frame for create a lot of Navon's Figure
		self.FileGeneration = LabelFrame(self.fixframe, width=Setup.WIDTH, text="Mass Generation")
		self.FileGeneration.grid(row=0, column=1, sticky="nsw", padx=5)

		Button(self.FileGeneration, text="import as CSV", command=self.importCSV, padx=padx).grid(row=0, column=0)
		Button(self.FileGeneration, text="export as Images", command=self.exportMassIMG, padx=padx).grid(row=0, column=1, sticky="we")

		self.export = LabelFrame(self.fixframe, text="Export your generation")
		self.export.grid(row=0, column=2, sticky="nsw",padx=5)
		Button(self.export, text="export as CSV", command=self.exportCSV, padx=padx).grid(row=0, column=0)
		Button(self.export, text="export as Image", command=self.exportIMG, padx=padx).grid(row=0, column=1)


		# Frame for the template
		self.templateframe = LabelFrame(self.fixframe, text="Templates")
		self.templateframe.grid(row=0,column=0,sticky="nsw",padx=5)

		Label(self.templateframe, text = "Choose the global form",bg="white").grid(row=0, column=0,columnspan=2)

		comboForm = ttk.Combobox(self.templateframe,values=["A","B"],state="readonly")
		comboForm.grid(row=0, column=0, sticky="nsw")
		comboForm.current(0)
		comboForm.bind("<<ComboboxSelected>>",self.func)

	


		## Every tools used to create a Navon's Figure are in this frame
		self.tools = LabelFrame(self.gen_Frame, text="Options")
		self.tools.grid(row=1, column=0, columnspan=5, sticky="we")

		### Density
		Label(self.tools, text="Density :", padx=padx).grid(row=0, column=0)
		Spinbox(self.tools, from_=1, to=100, width=4).grid(row=0, column=1, padx=padx)

		### Size 
		Label(self.tools, text="Size :", padx=padx).grid(row=0, column=2)
		Spinbox(self.tools, from_=1, to=100, width=4).grid(row=0, column=3, padx=padx)

		### Font
		Label(self.tools, text="Font :", padx=padx).grid(row=0, column=4)
		self.cbfonts = ttk.Combobox(self.tools, values=font.families(), state="readonly", width=15) # ComboBox Fonts
		self.cbfonts.grid(row=0, column=5, padx=padx)
		self.cbfonts.bind("<<ComboboxSelected>>", self.changeFont)

		### Checkbox to choose between local character and local image
		self.cbvLocal = StringVar(value="Char") # ComboBox Variable for le Local Element
		Checkbutton(self.tools, text="Use a local Image", 
			var=self.cbvLocal, onvalue="Image", offvalue="Char",
			relief=RAISED, 
			command= self.changeLocalElement).grid(row=0, column=6)

		### Local Character (if used, the Local Image is disabled)
		self.labelChar = Label(self.tools, text="Local char :", padx=padx)
		self.entryChar = Entry(self.tools, width=2)
		self.labelChar.grid(row=0, column=7)
		self.entryChar.grid(row=0, column=8, padx=padx)

		### Local Image (if used, the Local Character is disabled)
		self.labelImg = Label(self.tools, text="Local Image :", padx=padx)
		self.entryImg = Button(self.tools, text="Search an Image")
		self.deleteImg = Button(self.tools, text="delete Image")

		self.getMainElement().bind(tobind[0],tobind[1])
		self.bindallframe(self.getMainElement(),tobind[0], tobind[1])

	def func(self,event=None):
		print("selected")

	def update(self):
		pass

	def final(self):
		pass

	def changeFont(self, event=None):
		font = self.cbDfonts.get()


	def changeLocalElement(self):
		"""
		Make appear and disappear the options of the local element from the draw canvas
		"""
		if self.cbvLocal.get() == 'Char': 	# Make appear Local Character Option
			self.labelImg.grid_forget() 
			self.entryImg.grid_forget()
			self.deleteImg.grid_forget()
			self.labelChar.grid(row=0, column=7)
			self.entryChar.grid(row=0, column=8, padx=1)

		else:								# Make appear Local Image Option
			self.labelImg.grid(row=0, column=9)
			self.entryImg.grid(row=0, column=10, padx=1)
			self.deleteImg.grid(row=0, column=11, padx=1)
			self.labelChar.grid_forget()
			self.entryChar.grid_forget()

	def importCSV(self):
		pass

	def exportCSV(self):
		pass

	def exportMassIMG(self):
		pass

	def exportIMG(self):
		pass


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