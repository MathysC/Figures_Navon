
import tkinter
from tkinter import *
import tkinter.font as font
from tkinter.filedialog import *

import os
import sys

sys.path.append(os.path.abspath(".")+'\\Metier')

from FiguresNavon import *

#fenetrePrincipale
maFenetre = tkinter.Tk()
maFenetre.title("générateur de Navon")
maFenetre.geometry("800x800")

#typographie
f=font.Font(family="Verdana",size=15)
f_titre=font.Font(family="Verdana",size=20,weight="bold")

maFigureNavon = FigureNavon("A", "B", 512, 512, 400, 400, 10, 10, 18, 0.5)
listeEstChargee = False
filepathListeChargee = ""

#apercu les fichiers png
def generer():

    res_LettreGlobale=s_lGlobale.get()
    res_LettreLocale=s_lLocale.get()

    print("appel de FigureNavon:")

    maFigureNavon.setElementGlobal(res_LettreGlobale)
    maFigureNavon.setElementLocal(res_LettreLocale)
    maFigureNavon.setHeightLG(nb_HeightLG.get())
    maFigureNavon.setWidthLG(nb_widthLG.get())
    maFigureNavon.setTailleLL(nb_HeightLL.get())
    maFigureNavon.setDensite(nb_densite.get())
    maFigureNavon.setMargeX(nb_margeX.get())
    maFigureNavon.setMargeY(nb_margeY.get())
    maFigureNavon.setTailleX(nb_tailleX.get())
    maFigureNavon.setTailleY(nb_tailleY.get())
    figure = maFigureNavon.creerFigureNavon()
    maFigureNavon.preview(figure)

#---------------------------------------------------------sauvegarder fichier png
def sauvegarde():

    if maFigureNavon.getFichierCharge() == False:
        print("hey !")
        res_LettreGlobale = s_lGlobale.get()
        res_LettreLocale = s_lLocale.get()
        maFigureNavon.setElementGlobal(res_LettreGlobale)
        maFigureNavon.setElementLocal(res_LettreLocale)
        maFigureNavon.setHeightLG(nb_HeightLG.get())
        maFigureNavon.setWidthLG(nb_widthLG.get())
        maFigureNavon.setTailleLL(nb_HeightLL.get())
        maFigureNavon.setDensite(nb_densite.get())
        maFigureNavon.setMargeX(nb_margeX.get())
        maFigureNavon.setMargeY(nb_margeY.get())
        maFigureNavon.setTailleX(nb_tailleX.get())
        maFigureNavon.setTailleY(nb_tailleY.get())
        figure = maFigureNavon.creerFigureNavon()
        #récupére le chemin où l'on souvegarde l'image = peut ajouter des extensions ici
        filepath = tkinter.filedialog.asksaveasfilename(initialdir="/", title="Save as", defaultextension="*.*",
                                                        filetypes=(("png files", "*.png"),('jpeg files','*.jpg'),('all files','*.*')))
        print(filepath)
        maFigureNavon.sauvegarderFigure(figure, filepath)
    else:
        filepath = tkinter.filedialog.askdirectory(initialdir="/", title="Choose directory to save")
        maFigureNavon.genererToutesLesfiguresDUnFichier(maFigureNavon.getCheminFichierCharge(), filepath)

#------------------------------------------------------------Charger les données d'un fichier text
def charge():

    filepathListeChargee = askopenfilename(initialdir="/", title="Open as", defaultextension="*.*", filetypes=(("text files", "*.txt"), ("all files", "*.*")))

    maFigureNavon.chargerFigure(filepathListeChargee)
    maFigureNavon.setFichierCharge(True)
    s_CheminFichier.set(filepathListeChargee)


    # Liste des différentes combinaisons

    #test si liste vide ou non
    while (l_listeCombinaisons.size()>0):
        for i in range(l_listeCombinaisons.size()):
            print("JE SUPPRIME à L'INDEX ", i, " -> ", l_listeCombinaisons.get(i))
            l_listeCombinaisons.delete(i)



    i = 1
    for element in maFigureNavon.getListeFiguresNavon():
        print("ELEMENT")
        l_listeCombinaisons.insert(i, element.toString())

        if i==1:
            s_lGlobale.set(element.getElementGlobal())
            s_lLocale.set(element.getElementLocal())
            nb_tailleX.set(element.getTailleX())
            nb_tailleY.set(element.getTailleY())
            nb_HeightLG.set(element.getHeightLG())
            nb_HeightLG.set(element.getWidthLG())
            nb_densite.set(element.getDensite())
            nb_HeightLL.set(element.getTailleLL())
            nb_margeX.set(element.getMargeX())
            nb_margeY.set(element.getMargeY())
        i = i + 1

    l_listeCombinaisons.pack(side=BOTTOM)
    # bt = tkinter.Button(lf_chargerFichier, txt="get item") #command="updateSelection"
    # bt.pack()


#--------------------------------------------------------------------- TITRE
f_titre= tkinter.Frame(maFenetre, borderwidth=2, relief=GROOVE)
f_titre.pack(side=TOP,padx=1,pady=30)
Label(f_titre,text="------ Navon Generator  ------",font=f_titre).pack(padx=10,pady=10)


#--------------------------------------------------------------------- PARAMETRE DES LETTRES
#------------------------------------------------------FORME LETTRES
lf_formeLettres= tkinter.LabelFrame(maFenetre, text="Settings",padx=5,pady=1)
lf_formeLettres.pack(fill="both",padx="10",pady="10",ipady="20",ipadx="10")

f_formeLettres = tkinter.Frame(lf_formeLettres,width=300, height=300,bd=10)

    #Label lettre Globale et champs de saisie
s_lGlobale=tkinter.StringVar()
s_lGlobale.set("A")
Label(f_formeLettres,text="Global Letter : ").pack(side=LEFT)
champ_lettreGlobale = tkinter.Entry(f_formeLettres,textvariable=s_lGlobale, bg="white", width="10")
champ_lettreGlobale.pack(side=LEFT)

    #Label lettre locale et champ de saisie
s_lLocale=tkinter.StringVar()
s_lLocale.set("B")
Label(f_formeLettres,text="Local Letter : ").pack(side=LEFT)
champ_lettreLocale = tkinter.Entry(f_formeLettres,textvariable=s_lLocale, bg="white", width="10")
champ_lettreLocale.pack(side=LEFT)

f_formeLettres.pack()

# ------------------------------------------------------taille image

f_tailleImage= tkinter.Frame(lf_formeLettres, width=300, height=300, bd=10)

nb_tailleX = tkinter.IntVar()
nb_tailleX.set(512)
Label(f_tailleImage, text="Picture size X :").pack(side=LEFT)
champ_tailleX = tkinter.Entry(f_tailleImage, textvariable=nb_tailleX, bg="white", width="10")
champ_tailleX.pack(side=LEFT)
Label(f_tailleImage, text=" px").pack(side=LEFT)

nb_tailleY = tkinter.IntVar()
nb_tailleY.set(512)
Label(f_tailleImage, text=" -  Y :").pack(side=LEFT)
champ_tailleY = tkinter.Entry(f_tailleImage, textvariable=nb_tailleY, bg="white", width="10")
champ_tailleY.pack(side=LEFT)
Label(f_tailleImage, text=" px").pack(side=LEFT)

f_tailleImage.pack()
#------------------------------------------------------HAUTEUR ET LARGEUR LETTRE GLOBALE

f_tailleLG = tkinter.Frame(lf_formeLettres,width=300, height=300, bd=10)
   
nb_HeightLG = tkinter.IntVar()
nb_HeightLG.set(400)
Label(f_tailleLG,text="Size Global Letter - Height :").pack(side=LEFT)
champ_tailleGX = tkinter.Entry(f_tailleLG,textvariable=nb_HeightLG, bg="white", width="10")
champ_tailleGX.pack(side=LEFT)
Label(f_tailleLG,text=" px").pack(side=LEFT)


nb_widthLG = tkinter.IntVar()
nb_widthLG.set(400)
Label(f_tailleLG,text=" - Width :").pack(side=LEFT)
champ_WidthLG = tkinter.Entry(f_tailleLG,textvariable=nb_widthLG, bg="white", width="10")
champ_WidthLG.pack(side=LEFT)
Label(f_tailleLG,text=" px").pack(side=LEFT)

f_tailleLG.pack()

# ------------------------------------------------------Marge X Y

f_marge = tkinter.Frame(lf_formeLettres, width=300, height=300, bd=10)

nb_margeX = tkinter.IntVar()
nb_margeX.set(10)
Label(f_marge, text="Margin X :").pack(side=LEFT)
champ_margeX = tkinter.Entry(f_marge, textvariable=nb_margeX, bg="white", width="10")
champ_margeX.pack(side=LEFT)
Label(f_marge, text=" px").pack(side=LEFT)

nb_margeY = tkinter.IntVar()
nb_margeY.set(10)
Label(f_marge, text=" -  Y :").pack(side=LEFT)
champ_margeY = tkinter.Entry(f_marge, textvariable=nb_margeY, bg="white", width="10")
champ_margeY.pack(side=LEFT)
Label(f_marge, text=" px").pack(side=LEFT)

f_marge.pack()



#------------------------------------------------------HAUTEUR ET LARGEUR LETTRE LOCALE
f_tailleLL = tkinter.Frame(lf_formeLettres,width=300, height=300, bd=10)

nb_HeightLL = tkinter.IntVar()
nb_HeightLL.set(18)
Label(f_tailleLL,text="Size Police :").pack(side=LEFT)
champ_HeightLL = tkinter.Entry(f_tailleLL,textvariable=nb_HeightLL, bg="white", width="10")
champ_HeightLL.pack(side=LEFT)
Label(f_tailleLL,text=" pts").pack(side=LEFT)

f_tailleLL.pack()

#------------------------------------------------------DENSITE
f_densite = tkinter.Frame(lf_formeLettres,width=300, height=300, bd=10)

nb_densite = tkinter.DoubleVar()
nb_densite.set(0.5)
Label(f_densite,text="Density : ").pack(side=LEFT)
champ_densite = tkinter.Entry(f_densite,textvariable=nb_densite, bg="white", width="10")
champ_densite.pack(side=LEFT)

f_densite.pack()
Label(f_densite,text=" (between 0 and 1)").pack(side=LEFT)


#--------------------------------------------------------------------- BOUTON APERCU
f_BOUTON = tkinter.Frame(lf_formeLettres,width=300, height=300, bd=10)

bt_Apercu=tkinter.Button(f_BOUTON, relief=RAISED, bg="#32CD32", fg="WHITE",text="Preview",command=generer)
bt_Apercu['font']=f
bt_Apercu.pack()


f_BOUTON.pack()

#--------------------------------------------------------------------- BOUTON OUVRIR FICHIER PRE-EXISTANT
lf_chargerFichier= tkinter.LabelFrame(maFenetre, text="Load Setting File", padx=5,pady=1)
lf_chargerFichier.pack(fill="both",padx="10",pady="5",ipady="2",ipadx="10")

lf_nomFichier = tkinter.Frame(lf_chargerFichier,width=300, height=300, bd=10)
lf_listeFichier = tkinter.Frame(lf_chargerFichier,width=300, height=300)

    #bouton charger fichier
bt_Charge = tkinter.Button(lf_chargerFichier, relief=RAISED, bg="#32CD32", fg="WHITE",text="Load",command=charge)
bt_Charge['font']=f

    #texte et affichage de l'adresse
Label(lf_nomFichier,text="File load : ").pack(side=LEFT)
s_CheminFichier=tkinter.StringVar()
s_CheminFichier.set("")
Label(lf_nomFichier,textvariable=s_CheminFichier).pack(side=LEFT)

    #Liste des différentes combinaisons
l_listeCombinaisons = tkinter.Listbox(lf_listeFichier, listvariable=maFigureNavon.getListeFiguresNavon(),
                                      activestyle='underline', height=3, width=100, selectmode='single')

i=1
for element in maFigureNavon.getListeFiguresNavon():
    l_listeCombinaisons.insert(i,element)
    i=i+1


bt_Charge.pack()
l_listeCombinaisons.pack()
lf_nomFichier.pack()
lf_listeFichier.pack()



selected_item = StringVar()


def updateSelection():
    line = l_listeCombinaisons.curselection()[i]
    element = l_listeCombinaisons.get(line)

    s_lGlobale.set(element.getElementGlobal())
    s_lLocale.set(element.getElementLocal())
    #nb_tailleX.set(element.getTailleX())
    #nb_tailleY.set(element.getTailleY())
    nb_HeightLG.set(element.getHeightLG())
    nb_HeightLG.set(element.getWidthLG())
    nb_densite.set(element.getDensite())
    nb_HeightLL.set(element.getTailleLL())
    nb_margeX.set(element.getMargeX())
    nb_margeY.set(element.getMargeY())




#--------------------------------------------------------------------- BOUTON GENERER LE FICHIER
lf_sauvegardeForme= tkinter.LabelFrame(maFenetre, text="Save",padx=5,pady=1)
lf_sauvegardeForme.pack(fill="both",padx="10",pady="10",ipady="5",ipadx="10")


    #Bouton générer
bt_Generer = tkinter.Button(lf_sauvegardeForme, relief=RAISED, bg="#32CD32", fg="WHITE",text="Generate",command=sauvegarde)
bt_Generer['font']=f
bt_Generer.pack()


#--------------------------------------------------------------------- GENERATION FENETRE

    #CREATION FENETRE
def lancerAppli():
    maFenetre.mainloop()


