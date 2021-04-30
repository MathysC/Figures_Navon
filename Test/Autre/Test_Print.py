from PIL import Image, ImageFont, ImageDraw
import tkinter as TK
from tkinter import *
from PIL import Image, ImageTk

tabmatrix = {}
tabmatrix[0,0] = True
tabmatrix[0,1] = True
tabmatrix[1,0] = False
tabmatrix[1,1] = False
tabmatrix[2,0] = True
tabmatrix[2,1] = True
x, y = max(tabmatrix.keys())

# arial.ttf est un fichier téléchargé
TAILLEFONT = 24
DEMI = TAILLEFONT / 2
LOCALCHAR = "A"
font = ImageFont.truetype("arial.ttf", TAILLEFONT)
TAILLEIMAGE = [TAILLEFONT * (x+1), TAILLEFONT * (y + 3)]
print(TAILLEIMAGE)
# Creation de l'image en fonction de la matrice créée précédemment
im = Image.new('RGB', (TAILLEIMAGE[0], TAILLEIMAGE[1]), color='white')
draw = ImageDraw.Draw(im)

# Ecriture de l'image
for k2 in range(x+1):
    for k in range(y+1):
        print(f"{DEMI + TAILLEFONT * k, DEMI + TAILLEFONT * k2/3} : {tabmatrix[k2,k]}")
        draw.text((DEMI + TAILLEFONT * k/3, DEMI + TAILLEFONT * k2), LOCALCHAR if tabmatrix[k2, k] else " ",
                  (0, 0, 0), font=font)
# Save de l'image
im.show()