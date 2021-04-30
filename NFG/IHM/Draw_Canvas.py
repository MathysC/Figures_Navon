from IHM.elements.ElementFactory import ElementFactory as Factory
from Logic.Setup import Setup

from IHM.elements.Line import Line

import tkinter as TK
import numpy as np


class Draw_Canvas:
    def __init__(self, mainWindow, nf,elementType="line"):
        self.NF = nf

        # Canvas de dessin
        self.draw_canvas = TK.Canvas(mainWindow, width=Setup.WIDTH, height=Setup.HEIGHT, bg="white")
        self.draw_canvas.grid(row=0, column=0)

        # Récupération des infos en fonctions du elementType de l'élément
        self.element = Factory.Create(elementType)
        # Un event au click
        self.draw_canvas.bind('<Button-1>', self.start)
        # Un event au release
        self.draw_canvas.bind('<ButtonRelease-1>', self.end)

    def start(self, event):
        self.element.start(event=event, draw_canvas=self.draw_canvas)
        # Un event au motion tant que le bouton est appuyé
        self.draw_canvas.bind('<B1-Motion>', self.motion)

    def motion(self, event):
        self.element.motion(event=event, draw_canvas=self.draw_canvas)

    def end(self, event):
        # On retire le bind inutile à la fin du trait
        self.draw_canvas.unbind('<B1-Motion>')
        self.element.end(event=event, NF=self.NF)
        # On recréer un prochain element
        self.element = Factory.Create(self.element.getType())
