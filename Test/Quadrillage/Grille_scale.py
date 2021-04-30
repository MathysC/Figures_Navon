import tkinter as TK
from tkinter import *
from PIL import Image, ImageTk


# Var global de test
class Setup:
    MINNBSQUARE = 5
    MAXNBSQUARE = 10
    WIDTH = 50*MINNBSQUARE
    HEIGHT = 50*MINNBSQUARE
    SIZESQUARE = 250/MINNBSQUARE
    TABLESQUARE = {}

    @staticmethod
    def calculSize(num) ->int:
        return 250/num
# Class pour les cases de la grille
class Square:
    # Création du canvas rectangle à l'init
    def __init__(self, can, start_x, start_y, size):
        self.can = can
        self.id = self.can.create_rectangle((start_x, start_y,
                                             start_x + size, start_y + size), fill="white")
        # Affecter le clique gauche à la fonction set_color
        self.can.tag_bind(self.id, "<ButtonPress-1>", self.set_color)

        self.color_change = False

    # changement de couleur à chaque clique
    def set_color(self, event=None):
        self.color_change = not self.color_change
        color = "white"
        if self.color_change:
            color = "black"
        self.can.itemconfigure(self.id, fill=color)

    # mettre la couleur blanche au carré
    def cleanSquare(self):
        self.can.itemconfigure(self.id, fill="white")
        if(self.color_change):
            self.color_change = not self.color_change

class Scale:
    def __init__(self,canvas, _from_, _to, _length, _orient=TK.HORIZONTAL):
        self.can = canvas
        self.slider = TK.Scale(mainWindow, from_=_from_, to=_to, length=_length, orient=_orient, resolution=1,
                               tickinterval=1)
        # Affecter le clique gauche à la fonction set_color
        self.slider.bind("<ButtonRelease-1>", self.updateValue)

    def updateValue(self, event):
        self.can.delete("all")
        print(self.slider.get())
        Setup.TABLESQUARE.clear()
        Setup.TABLESQUARE = CreateGrid(self.can,self.slider.get(),5,250/self.slider.get())

########################################################################################################################
########################################################################################################################

# Fonction blanchissant toute la grille
def clean():
    # blanchit toutes les cases une par une !!!!! A REFAIRE POUR BLANCHIR QUE CELLE NOIRCIE !!!!!!!!!!!!
    for tab in Setup.TABLESQUARE.values():
        tab.cleanSquare()

    # Creation de toutes les cases dans la grille placé dans le canvas


def CreateGrid(_canvas, _width, _height, _size) -> dict:
    height, width = 0, 0
    table = {}
    __width = Setup.WIDTH / Setup.calculSize(_width)
    __height = Setup.HEIGHT / Setup.calculSize(_width)
    # Pour X carré sur l'axe des abscisses
    while width < __width:
        # Pour Y carré sur l'axe des ordonnées
        while height < __height:
            table[width, height] = Square(_canvas, width * Setup.calculSize(_width), height * Setup.calculSize(__height),
                                          _size)
            height += 1
        width += 1
        height = 0
        print(f"width : {width}, height : {height}")
    return table

# fenetrePrincipale
mainWindow = TK.Tk()
mainWindow.title("générateur de Navon")
mainWindow.geometry("1000x500")

grid_canvas = TK.Canvas(mainWindow, width=Setup.WIDTH, height=Setup.HEIGHT, bg="white")
grid_canvas.grid(row=0, column=0)

Setup.TABLESQUARE = CreateGrid(grid_canvas,Setup.MINNBSQUARE,Setup.MINNBSQUARE,Setup.SIZESQUARE)

# Bouton afin de clean le tout
b1 = TK.Button(mainWindow, width=20, height=10, text="clean", command=clean)
b1.grid(row=0, column=1)






# Scale X afin de changer le nombre de case sur l'axe des abscisses
X_Scale = Scale(grid_canvas,Setup.MINNBSQUARE, Setup.MAXNBSQUARE, 200)
X_Scale.slider.grid(row=1, column=0)

if __name__ == '__main__':
    mainWindow.mainloop()
