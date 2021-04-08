import json


class Parseur:
    # ATTRIBUTS
    elementGlobal = ""
    nomFichier = ""

    # CONSTRUCTEUR
    def __init__(self, nomFile, elementG):
        self.nomFichier = nomFile
        self.elementGlobal = elementG
        self.listeCoordonnees = []
        self.listeCurve = []

    # METHODES

    # permet de lire le fichier de description du symbole
    def lireFichier(self):
        print("Lecture en cours du fichier")

        # with open("../Templates/"+self.nomFichier, 'r') as fichier:
        with open("Templates/" + self.nomFichier, 'r') as fichier:
            data = json.load(fichier)

        self.recupererPoints(data)

        print(self.listeCoordonnees)

        # récupère les points de départ et d'arrivée des différentes droites qui composent l'élément global

    def recupererPoints(self, data):
        i = 0
        for x in data:
            i = i + 1

        for nb in range(0, i):
            if data[str(nb)]["Type"] == "line":
                self.listeCoordonnees.append(int(data['' + str(nb)]['Xa']))
                self.listeCoordonnees.append(int(data['' + str(nb)]['Ya']))
                self.listeCoordonnees.append(int(data['' + str(nb)]['Xb']))
                self.listeCoordonnees.append(int(data['' + str(nb)]['Yb']))
            if data[str(nb)]["Type"] == "curve":
                self.listeCurve.append(float(data['' + str(nb)]['X1']))
                self.listeCurve.append(float(data['' + str(nb)]['Y1']))
                self.listeCurve.append(float(data['' + str(nb)]['X2']))
                self.listeCurve.append(float(data['' + str(nb)]['Y2']))
                self.listeCurve.append(float(data['' + str(nb)]['angleDepart']))
                self.listeCurve.append(float(data['' + str(nb)]['angleArrive']))
                # https://matplotlib.org/3.1.0/api/_as_gen/matplotlib.patches.Arc.html

    def get(self, numero):
        return self.listeCoordonnees[numero]

    def getElementCurve(self, numero):
        return self.listeCurve[numero]

    ##############################GETTER
    def getNomFichier(self):
        return self.nomFichier

    def getListeCoordonnees(self):
        return self.listeCoordonnees

    def getListeCurve(self):
        return self.listeCurve
