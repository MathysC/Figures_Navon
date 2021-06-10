from PIL import Image, ImageFont, ImageDraw
from tkinter import *
from PIL import Image, ImageTk
import math
from Logic.Setup import Setup
from Logic.NF import NF

from IHM.Canvas.Draw_Canvas import Draw_Canvas


class Ui_MainWindow:
	"""
	class that implements the main window of the project
	"""
	def __init__(self):
		self.mainWindow = Tk()
		# Prepare the Setup
		Setup.WIDTH = self.mainWindow.winfo_screenwidth()-80
		Setup.HEIGHT = self.mainWindow.winfo_screenheight()-80
		
		self.mainWindow.title("NFG - Navon's Figure Generator")
		self.mainWindow.geometry(f"{Setup.WIDTH}x{Setup.HEIGHT}")
		self.mainWindow.state('zoomed')

		self.canvas = {}
		# Menus
		mainMenu = Menu(self.mainWindow)
		self.mainWindow.config(menu=mainMenu)
		fileMenu = Menu(master=mainMenu,tearoff=0)
		mainMenu.add_cascade(label = "File", menu = fileMenu)
		saveMenu = Menu(master=fileMenu,tearoff=0)
		fileMenu.add_cascade(label = "Save As ... ", menu=saveMenu)
		fileMenu.add_separator()
		fileMenu.add_command(label = "Quit", command=self.mainWindow.quit)

		self.options_frame = Frame(self.mainWindow,width = Setup.WIDTH,bd=2,bg="white")
		self.options_frame.grid(row=0,column=0,columnspan=2,sticky="nsew")

#		self.options_frame.grid(sticky='nsew')
		self.cboxvalue = StringVar()
		self.checkbox =Checkbutton(master=self.options_frame,text="Switch Canvas",bg="white",bd=1,var=self.cboxvalue,onvalue="draw",offvalue="generator")
		self.checkbox.grid(row=0,column=0)

		## Create the frame that contains the global buttons (preview etc)
		#self.global_frame = LabelFrame(self.mainWindow,font=Setup.FONT,bd=1,bg="white", relief=RIDGE)
		#self.global_frame.place(x=0,y=Setup.HEIGHT,width=Setup.WIDTH+70,height=50)
		#
		## Button that lists all created element (ONLY FOR TEST PHASE)
		#self.list_Button = Button(self.global_frame, height= 2,text="get the list", command=self.getlist)
		#self.list_Button.grid(row=0, column=2)
		#
		## Button that prints the NF
		#self.print_Button = Button(self.global_frame, height=2, text="preview", command=self.final)
		#self.print_Button.grid(row=0, column=1)


		self.res_canvas = Canvas(self.mainWindow,height=Setup.HEIGHT,width=Setup.WIDTH/2, bg="blue", relief=RIDGE, bd=1)
		self.res_canvas.grid(row=1,column=1,sticky="nse")

		self.canvas_frame = Frame(self.mainWindow,width = Setup.WIDTH,bd=2,bg="white")
		self.canvas_frame.grid(row=1,column=0,sticky="nsw")

		self.NF = NF()
		# Create the Draw part and the options
		self.canvas['draw'] = Draw_Canvas(self.canvas_frame, self.NF,self.options_frame)
		self.mainWindow.bind('<Return>',self.final)


	def changeCanvas(self,event=None):
		pass

	def start(self):
		"""
		Function that start the project in the main
		"""
		self.mainWindow.mainloop()

	def getlist(self):
		"""
		(ONLY FOR TEST PHASE)
		Function to get the print of all lines
		"""
		#for i in range(0,100):
		#	print("")
		for element in self.NF.elements:
			print(f"{element.getType()} {element.getId()} : {element.getCoords()}")
			for intersection in element.getIntersections():
				intersection = int(intersection)
				print(f" intersection [{intersection}] : coords : {self.canvas['draw'].draw_canvas.coords(intersection)} | tags : {self.canvas['draw'].draw_canvas.gettags(intersection)}")
			print(f"  neighbors : {element.getNeighbors()}")
	def final(self,event=None):
		"""
		Function that (currently only ) preview the NF
		"""
		self.canvas['draw'].update()
		self.NF.final(self.canvas['draw'].draw_canvas)
		#self.NF.finalImage(self.canvas['draw'].draw_canvas)
