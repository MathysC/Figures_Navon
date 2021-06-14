from abc import ABC, abstractmethod
from tkinter import *
from Logic.NF import NF

class Ui_Canvas(ABC):
	def __init__(self,mainElement):
		self.mainElement = mainElement 
		
	def getMainElement(self):
		return self.mainElement

	@abstractmethod
	def update(self):
		pass

	@abstractmethod
	def final(self):
		pass