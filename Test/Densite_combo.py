
from PIL import Image, ImageFont, ImageDraw
import tkinter as TK
from tkinter import *
from PIL import Image, ImageTk


# Var global de test
class Setup:
    MINNBSQUARE = 10
    MAXNBSQUARE = 20
    WIDTH = 250
    HEIGHT = 250
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

def density():
    # matrix() mais veut pas fonctionner idk why
    NF = {}
    # Cette Matrice récupère les états de chaque case
    for tab in Setup.TABLESQUARE.keys():
        NF[tab[0], tab[1]] = Setup.TABLESQUARE[tab].state

    #Ajouter les espaces puis ajouter les sous cases
    # Espace

    # Initialisation
    maxX = max(NF.keys())[0] + 1
    maxY = max(NF.keys())[1] + 1
    newNF = {}
    curX, curY = 0, 0
    space = int(Space_Scale.get())
    for oldx in range(0, maxX):
        curY = 0  # Pour chaque Ligne remettre à 0 le nb de colonne
        for oldy in range(0, maxY):
            state = NF[oldx, oldy]  # On récupère la valeur de la case (NF)
            newNF[curX, curY] = state  # On attribut cette valeur à un nouvel emplacement dans
            # Il faut ensuite ajouter les espaces
            curY += 1
            for esp in range(0, space):
                newNF[curX, curY + esp] = False  # On ajoute un espace
            curY += space
        # Dès que toutes les colonnes sont faites, on ajoute les espaces sous la ligne
        for esp in range(1, space + 1):
            for y in range(0, max(newNF.keys())[1] + 1):
                newNF[curX + esp, y] = False
        curX += 1 + space


    # Suppression des espaces inutiles en fin de NF
    # Supprimer les dernières lignes des espaces ajoutés
    newX, newY = max(newNF.keys())
    for i in range(newX - space + 1, newX + 1):
        for j in range(0, newY + 1):
            del newNF[i, j]

    # Supprimer les dernières colonnes ajoutés
    newX, newY = max(newNF.keys())  # MaJ des max X et Y
    for i in range(0, newX + 1):  # Faire sur chaque ligne
        for j in range(newY - space + 1, newY + 1):  # Faire sur les dernières colonnes
            del newNF[i, j]

    # Sous cases
    # Initialisation
    temp = {}
    dens = int(Density_Scale.get())
    m1 = max(newNF.keys())[0] + 1
    m2 = max(newNF.keys())[1] + 1
    # On fait le tour de la matrice d'origine
    for oldx in range(0, m1):
        for oldy in range(0, m2):
            state = newNF[oldx, oldy]

            # On ajoute autant de fois que (dens) l'état de tabmatrix[k, k2]
            for newx in range(0,dens):
                for newy in range(0,dens):
                    x = newx + dens*oldx
                    y = newy + dens*oldy
                    temp[x,y] = state
    return temp

def show(tabmatrix):
    res = []
    # Il faut faire la boucle en partant du deuxième élément afin d'obtenir la matrice ligne par ligne
    for k2 in range(0, max(tabmatrix.keys())[0] + 1):
        temp = []
        for k in range(0, max(tabmatrix.keys())[1] + 1):
            temp.append(1 if tabmatrix[k, k2] else 0)
        res.append(temp)

    for row in res:
        print(row)

def impression():
    # appelle de la fonction permettant d'obtenir la NF correcte
    tabmatrix = density()
    # Creation de la police
    # arial.ttf est un fichier téléchargé
    TAILLEFONT = 24
    DEMI = TAILLEFONT / 2
    LOCALCHAR = "A"
    font = ImageFont.truetype("arial.ttf", TAILLEFONT)
    TAILLEIMAGE = [TAILLEFONT * (max(tabmatrix.keys())[0] + 2), TAILLEFONT * (max(tabmatrix.keys())[1] + 2)]
    # Creation de l'image en fonction de la matrice créée précédemment
    im = Image.new('RGB', (TAILLEIMAGE[0], TAILLEIMAGE[1]), color='white')
    draw = ImageDraw.Draw(im)

    # Ecriture de l'image
    for k2 in range(0, max(tabmatrix.keys())[0] + 1):
        for k in range(0, max(tabmatrix.keys())[1] + 1):
            draw.text((DEMI + TAILLEFONT * k, DEMI + TAILLEFONT * k2), LOCALCHAR if tabmatrix[k, k2] else " ",
                      (0, 0, 0), font=font)
    # Save de l'image
    im.show()
    #im.save("test.PNG")

# fenetrePrincipale
mainWindow = TK.Tk()
mainWindow.title("générateur de Navon")
mainWindow.geometry("450x600")
mainWindow.resizable(FALSE, FALSE)
grid_canvas = TK.Canvas(mainWindow, width=Setup.WIDTH, height=Setup.HEIGHT, bg="white")
grid_canvas.grid(row=0, column=0)

Setup.TABLESQUARE = CreateGrid(grid_canvas, Setup.MINNBSQUARE, Setup.MINNBSQUARE, Setup.SIZESQUARE)

# Bouton afin de clean le tout
b1 = TK.Button(mainWindow, width=20, height=10, text="clean", command=clean)
b1.grid(row=0, column=2)

# Bouton afin de créer une preview de la figure de Navon
b3 = TK.Button(mainWindow, width=20, height=10, text="Impression", command=impression)
b3.grid(row=2, column=2)

# Scale X afin de changer le nombre de case sur l'axe des abscisses
X_Scale = Scale(grid_canvas, Setup.MINNBSQUARE, Setup.MAXNBSQUARE, 200)
X_Scale.slider.grid(row=1, column=0)

# Scale Density afin de changer la densité de la figure de Navon Finale
Density_Scale = TK.Spinbox(mainWindow,from_=1, to=100)
Density_Scale.grid(row=2, column=0)

# Scale Density afin de changer la densité de la figure de Navon Finale
Space_Scale = TK.Spinbox(mainWindow, from_=0, to=100)
Space_Scale.grid(row=3, column=0)

if __name__ == '__main__':
    mainWindow.mainloop()
