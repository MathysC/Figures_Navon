from PIL import Image, ImageFont, ImageDraw
from tkinter import *
from PIL import Image, ImageTk
import math
from Logic.Setup import Setup
from Logic.NF import NF

from IHM.Draw_Canvas import Draw_Canvas


class Ui_MainWindow:
	"""
	class that implements the main window of the project
	"""
	def __init__(self):
		self.mainWindow = Tk()
		self.mainWindow.title("générateur de Navon")
		self.mainWindow.geometry("500x355")
		self.mainWindow.resizable(FALSE, FALSE)

		self.NF = NF()

		# Create the Draw part and the options
		self.draw = Draw_Canvas(self.mainWindow, self.NF)

		# Create the frame that contains the global buttons (preview etc)
		self.global_frame = LabelFrame(self.mainWindow,font=Setup.FONT,bd=1,bg="white", relief=RIDGE)
		self.global_frame.place(x=0,y=Setup.HEIGHT,width=Setup.WIDTH+70,height=50)
		
		# Button that lists all created element (ONLY FOR TEST PHASE)
		self.list_Button = Button(self.global_frame, height= 2,text="get the list", command=self.getlines)
		self.list_Button.grid(row=0, column=1)
		
		# Button that prints the NF
		self.print_Button = Button(self.global_frame, height=2, text="preview", command=self.final)
		self.print_Button.grid(row=0, column=2)


	def start(self):
		"""
		Function that start the project in the main
		"""
		self.mainWindow.mainloop()

	def getlines(self):
		"""
		(ONLY FOR TEST PHASE)
		Function to get the print of all lines
		"""
		for i in range(0,100):
			print("")
		print("-----------Line-----------")
		for line in self.NF.lines:
			print(f"{line} {line.getCoords()}")
		print("-----------Arc-----------")
		for arc in self.NF.arcs:
			print(f"{arc} {arc.getCoords()}")
		print("-----------Circle-----------")
		for circle in self.NF.circles:
			print(f"{circle} {circle.getCoords()}")



	def final(self):
		"""
		Function that (currently only ) preview the NF
		"""
		self.draw.update()
		self.NF.final()
