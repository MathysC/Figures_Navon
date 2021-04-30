from PIL import Image, ImageFont, ImageDraw
import tkinter as TK
from tkinter import *
from PIL import Image, ImageTk
import math
from Logic.Setup import Setup
from Logic.NF import NF

from IHM.Draw_Canvas import Draw_Canvas


class Ui_MainWindow:
    def __init__(self):
        # fenetrePrincipale
        self.mainWindow = TK.Tk()
        self.mainWindow.title("générateur de Navon")
        self.mainWindow.geometry("600x500")
        self.mainWindow.resizable(FALSE, FALSE)

        # Figure de Navon en cours de création
        self.NF = NF()
        # Canvas de Dessin
        self.draw = Draw_Canvas(self.mainWindow, self.NF)

        # Bouton permettant d'afficher en console les différentes lignes dessinées
        self.list_Button = TK.Button(self.mainWindow, width=10, height=3, text="get the list", command=self.getlines)
        self.list_Button.grid(row=0, column=1)

        # Bouton permettant d'obtenir la preview de la NF
        self.print_Button = TK.Button(self.mainWindow, width=10, height=3, text="preview", command=self.final)
        self.print_Button.grid(row=0, column=2)

        # Bouton permettant de vider la liste des lignes et la zone de dessin
        self.clear_Button = TK.Button(self.mainWindow, width=10, height=3, text="clear")  # ,command=clear
        self.clear_Button.grid(row=1, column=2)

        #
        self.density_spinbox = TK.Spinbox(master=self.mainWindow, width=10, from_=1, to=50)
        self.density_spinbox.grid(row=1, column=1)

    def start(self):
        self.mainWindow.mainloop()

    def getlines(self):
        for line in self.NF.lines:
            print(line.getCoords())

    def final(self):
        self.NF.final()
