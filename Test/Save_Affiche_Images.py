from PIL import Image, ImageFont, ImageDraw
import tkinter as TK
from tkinter import *
from PIL import Image, ImageTk

# Creation de l'image
im = Image.new('RGB', (500, 500), color='white')
draw = ImageDraw.Draw(im)

# Creation de la police
# arial.ttf est un fichier téléchargé
TAILLEFONT = 80
font = ImageFont.truetype("arial.ttf", TAILLEFONT)

# Ecriture de l'image
# draw.text(x,y),"string", (R,G,B), font)
draw.text((0, 150), "A", (0, 0, 0), font=font)
draw.text((0, 150 + TAILLEFONT), "A", (0, 0, 0), font=font)

# Save de l'image
# im.save("test.PNG")


# MainWindow
# fenetrePrincipale
mainWindow = TK.Tk()
mainWindow.title("générateur de Navon")
mainWindow.geometry("1000x500")

# Affichage de l'image dans la mainWindow
img = ImageTk.PhotoImage(im)
image_canvas = TK.Canvas(mainWindow, width=im.size[0] + TAILLEFONT, height=im.size[0] + TAILLEFONT)
image_canvas.create_image(TAILLEFONT, TAILLEFONT, anchor=TK.NW, image=img)
image_canvas.pack()

if __name__ == '__main__':
    mainWindow.mainloop()

