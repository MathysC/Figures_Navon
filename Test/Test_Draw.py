from PIL import Image, ImageFont, ImageDraw
import tkinter as TK
from tkinter import *
from PIL import Image, ImageTk
import math


class Setup:
    MINNBSQUARE = 10
    MAXNBSQUARE = 15
    WIDTH = 400
    HEIGHT = 250
    SIZESQUARE = 250 / MINNBSQUARE
    TABLESQUARE = {}
    CLICK = False
    line = {'x1': 0, 'y1': 0, 'x2': 0, 'y2': 0}
    lines = []


def draw_line(event):
    if not Setup.CLICK:
        Setup.line['x1'] = event.x
        Setup.line['y1'] = event.y
        Setup.CLICK = True

    else:
        Setup.line['x2'] = event.x
        Setup.line['y2'] = event.y
        Setup.lines.append(draw_canvas.create_line(Setup.line['x1'], Setup.line['y1'], Setup.line['x2'], Setup.line['y2'], fill='black',
                                width=1))
        Setup.CLICK = False


def draw_continuous_line(event):
    if not Setup.CLICK:
        Setup.line['x1'] = event.x
        Setup.line['y1'] = event.y
        Setup.CLICK = True
    else:
        Setup.line['x2'] = event.x
        Setup.line['y2'] = event.y
        draw_canvas.create_line(Setup.line['x1'], Setup.line['y1'], Setup.line['x2'], Setup.line['y2'], fill='black',
                                width=1)
        Setup.line['x1'] = event.x
        Setup.line['y1'] = event.y



# Fonctions pour MainWindow
def getlines():
    """
    Print all the lines created
    :return:
    """
    cls = lambda: print('\n' * 100)
    cls()
    print(f"nb : {len(Setup.lines)}")
    for line in Setup.lines:
        coord = draw_canvas.coords(line)
        line = {}
        line['x1'] = coord[0]
        line['y1'] = coord[1]
        line['x2'] = coord[2]
        line['y2'] = coord[3]
        del(coord)
        print(f"line : {line} | {getdistance(line)}")

def getdistance(line):
    """
    Calculate de length of a line
    :param line:
    :return:
    """
    return int(math.hypot(line['x1'] - line['x2'], line['y1'] - line['y2']))



def printNF():
    """
    Fonctionne avec une boucle partant du début à la fin de la ligne
    :return:
    """
    TAILLEFONT = 24
    ECART = TAILLEFONT+int(density_spinbox.get())
    LOCALCHAR = "A"
    BGCOLOR = "white"
    font = ImageFont.truetype("arial.ttf", TAILLEFONT)
    TAILLEIMAGE = [Setup.WIDTH,Setup.HEIGHT]
    im = Image.new('RGB', (TAILLEIMAGE[0]+TAILLEFONT, TAILLEIMAGE[1]+TAILLEFONT), color=BGCOLOR)
    draw = ImageDraw.Draw(im)
    for line in Setup.lines:
        coord = draw_canvas.coords(line)
        line = {}
        line['x1'] = coord[0]
        line['y1'] = coord[1]
        line['x2'] = coord[2]
        line['y2'] = coord[3]

        distance = getdistance(line)
        draw.line(xy=[(line['x1'],line['y1']+TAILLEFONT/2),
                      (line['x2']+TAILLEFONT/2,line['y2']+TAILLEFONT/2)],
                  fill='blue',width=TAILLEFONT)
        #Premier point de la ligne
        draw.text((line['x1'],line['y1']), LOCALCHAR,(0, 0, 0), font=font)
        for dist in range(0,distance-int(TAILLEFONT/2),ECART):
            # https://stackoverflow.com/questions/22190193/finding-coordinates-of-a-point-on-a-line
            th = math.atan2(line['y2']-line['y1'],line['x2']-line['x1'])
            point = [line['x1']+dist*math.cos(th), line['y1']+dist*math.sin(th)]
            draw.text((point[0],point[1]), LOCALCHAR,(0, 0, 0), font=font)
        #Deuxième point de la ligne
        #draw.line(xy=[(point[0],point[1]+TAILLEFONT/2),
        #              (line['x2']+TAILLEFONT/2,line['y2']+TAILLEFONT/2)],
        #                fill='blue',width=2)
        draw.text((line['x2'],line['y2']), LOCALCHAR,(0, 0, 0), font=font)
    im.show()

def printNF2():
    TAILLEFONT = 24
    ECART = TAILLEFONT+int(density_spinbox.get())
    LOCALCHAR = "A"
    BGCOLOR = "white"
    font = ImageFont.truetype("arial.ttf", TAILLEFONT)
    TAILLEIMAGE = [Setup.WIDTH,Setup.HEIGHT]
    im = Image.new('RGB', (TAILLEIMAGE[0]+TAILLEFONT, TAILLEIMAGE[1]+TAILLEFONT), color=BGCOLOR)
    draw = ImageDraw.Draw(im)
    for line in Setup.lines:
        coord = draw_canvas.coords(line)
        line = {}
        line['x1'] = coord[0]
        line['y1'] = coord[1]
        line['x2'] = coord[2]
        line['y2'] = coord[3]

        distance = getdistance(line)
        mid = int(distance/2)
        draw.line(xy=[(line['x1'],line['y1']+TAILLEFONT/2),
                      (line['x2']+TAILLEFONT/2,line['y2']+TAILLEFONT/2)],
                  fill='blue',width=TAILLEFONT)

        # Dessinage des différentes lettres locales

        # A partir du centre, mettre les lettres allant vers la fin et les lettres allant vers le début de la ligne

        # Calcul de th maintenant pour éviter la répétition d'un même calcul plusieurs fois
        th = math.atan2(line['y2'] - line['y1'], line['x2'] - line['x1'])
        # Lettre au milieu de la ligne
        center = [line['x1'] + mid * math.cos(th), line['y1'] + mid * math.sin(th)]
        draw.text((center[0], center[1]), LOCALCHAR, (0, 0, 0), font=font)
        # Milieu jusqu'au début de la ligne
        for dist in range(mid-ECART,0+ECART,-ECART):
            point = [line['x1'] + dist * math.cos(th), line['y1'] + dist * math.sin(th)]
            draw.text((point[0], point[1]), LOCALCHAR, (0, 0, 0), font=font)

        # Milieu jusqu'à la fin de la ligne
        for dist in range(mid+ECART,distance,ECART):
            point = [line['x1'] + dist * math.cos(th), line['y1'] + dist * math.sin(th)]
            draw.text((point[0], point[1]), LOCALCHAR, (0, 0, 0), font=font)

        # Au début de la ligne
        space = [line['x1'] + mid * math.cos(th), line['y1'] + mid * math.sin(th)]
        draw.line(xy=[(line['x1'], line['y1'] + TAILLEFONT / 2),
                      (space[0] + TAILLEFONT / 2, space[0] + TAILLEFONT / 2)],
                  fill='blue', width=TAILLEFONT)

        draw.text((line['x1'],line['y1']), LOCALCHAR,(0, 0, 0), font=font)

        # A la fin de la ligne
        draw.text((line['x2'], line['y2']), LOCALCHAR, (0, 0, 0), font=font)
    im.show()
def clear():
    Setup.lines.clear()
    draw_canvas.delete("all")

# fenetrePrincipale
mainWindow = TK.Tk()
mainWindow.title("générateur de Navon")
mainWindow.geometry("600x500")
mainWindow.resizable(FALSE, FALSE)

# Canvas de dessin
draw_canvas = TK.Canvas(mainWindow, width=Setup.WIDTH, height=Setup.HEIGHT, bg="white")
draw_canvas.grid(row=0, column=0)
draw_canvas.bind('<Button-1>', draw_line)

# Bouton permettant d'afficher en console les différentes lignes dessinées
list_Button = TK.Button(mainWindow,width=10, height=3, text="get the list", command=getlines)
list_Button.grid(row=0, column = 1)

# Bouton permettant d'obtenir la preview de la NF
print_Button = TK.Button(mainWindow,width=10, height=3, text="preview", command=printNF2)
print_Button.grid(row=0, column = 2)

# Bouton permettant de vider la liste des lignes et la zone de dessin
clear_Button = TK.Button(mainWindow,width=10, height=3, text="clear", command=clear)
clear_Button.grid(row=1, column = 2)

#
density_spinbox = TK.Spinbox(master=mainWindow,width=10,from_=1, to=50)
density_spinbox.grid(row=1, column = 1)

if __name__ == '__main__':
    mainWindow.mainloop()
