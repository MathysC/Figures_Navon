import tkinter as TK
from tkinter import *
from PIL import Image, ImageTk


# Var global de test
class Setup:
    MINNBSQUARE = 5
    MAXNBSQUARE = 10
    WIDTH = 50 * MINNBSQUARE
    HEIGHT = 50 * MINNBSQUARE
    SIZESQUARE = 250 / MINNBSQUARE
    TABLESQUARE = {}

    @staticmethod
    def calculSize(num) -> int:
        return 250 / num


# Class pour les cases de la grille

class Square:
    # Création du canvas rectangle à l'init
    def __init__(self, can, start_x, start_y, size):
        self.can = can
        self.state = False
        self.id = self.can.create_rectangle((start_x, start_y,
                                             start_x + size, start_y + size), fill="white")
        # Affecter le clique gauche à la fonction set_color
        self.can.tag_bind(self.id, "<ButtonPress-1>", self.set_color)

    # changement de couleur à chaque clique
    def set_color(self, event=None):
        if not self.state:
            color = "black"
        else:
            color = "white"
        self.can.itemconfigure(self.id, fill=color)
        self.state = not self.state

    # mettre la couleur blanche au carré
    def cleanSquare(self):
        self.can.itemconfigure(self.id, fill="white")
        self.state = False


class Scale:
    def __init__(self, canvas, _from_, _to, _length, _orient=TK.HORIZONTAL):
        self.can = canvas
        self.slider = TK.Scale(mainWindow, from_=_from_, to=_to, length=_length, orient=_orient, resolution=1,
                               tickinterval=1)
        # Affecter le clique gauche à la fonction set_color
        self.slider.bind("<ButtonRelease-1>", self.updateValue)

    def updateValue(self, event):
        self.can.delete("all")
        Setup.TABLESQUARE.clear()
        Setup.TABLESQUARE = CreateGrid(self.can, self.slider.get(), 5, 250 / self.slider.get())


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
            table[width, height] = Square(_canvas, width * Setup.calculSize(_width),
                                          height * Setup.calculSize(__height),
                                          _size)
            height += 1
        width += 1
        height = 0
    return table


def matrix():
    # Matrice avec laquelle nous travaillons
    tabmatrix = {}
    # Cette Matrice récupère les états de chaque case
    for tab in Setup.TABLESQUARE.keys():
        tabmatrix[tab[0], tab[1]] = Setup.TABLESQUARE[tab].state
    # Afficher les résultats de la matrice

    res = []
    # Il faut faire la boucle en partant du deuxième élément afin d'obtenir la matrice ligne par ligne
    for k2 in range(0, max(tabmatrix.keys())[0] + 1):
        temp = []
        for k in range(0, max(tabmatrix.keys())[1] + 1):
            temp.append(1 if tabmatrix[k, k2] else 0)
        res.append(temp)

    for row in res:
        print(row)


# fenetrePrincipale
mainWindow = TK.Tk()
mainWindow.title("générateur de Navon")
mainWindow.geometry("1000x500")

grid_canvas = TK.Canvas(mainWindow, width=Setup.WIDTH, height=Setup.HEIGHT, bg="white")
grid_canvas.grid(row=0, column=0)

Setup.TABLESQUARE = CreateGrid(grid_canvas, Setup.MINNBSQUARE, Setup.MINNBSQUARE, Setup.SIZESQUARE)

# Bouton afin de clean le tout
b1 = TK.Button(mainWindow, width=20, height=10, text="clean", command=clean)
b1.grid(row=0, column=1)

# Bouton afin de connaître la nouvelle matrice créée
b2 = TK.Button(mainWindow, width=20, height=10, text="Matrice", command=matrix)
b2.grid(row=1, column=1)

# Scale X afin de changer le nombre de case sur l'axe des abscisses
X_Scale = Scale(grid_canvas, Setup.MINNBSQUARE, Setup.MAXNBSQUARE, 200)
X_Scale.slider.grid(row=1, column=0)

if __name__ == '__main__':
    mainWindow.mainloop()
