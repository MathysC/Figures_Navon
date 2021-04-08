from Metier.FiguresNavon import FigureNavon


class ParserListeFigures:

    # CONSTRUCTEUR
    def __init__(self, nomFile):
        self.nomFichier = nomFile
        self.lettreGlobal = ""
        self.lettreLocal = ""
        self.tailleImageWidth = 0
        self.tailleImageHeight = 0
        self.marginX = 0
        self.marginY = 0
        self.sizeLettreLocal = 0
        self.densite = 0
        self.listeFigures = []

    # METHODES POUR PARSER LE FICHIER
    def recupererDonneesFichier(self):

        with open(self.nomFichier, "r") as fichier:
            lignes = fichier.readlines()
        for ligne in lignes:
            champs = ligne.split()
            if not (champs[0].startswith("#")):
                self.listeFigures.append(
                    FigureNavon(champs[0], champs[1], int(champs[2]), int(champs[3]), int(champs[4]), int(champs[5]),
                                int(champs[6]), int(champs[7]), int(champs[8]), float(champs[9])))

    ##################################GETTER
    def getNomfichier(self):
        return self.nomFichier

    def getLettreGlobal(self):
        return self.lettreGlobal

    def getLettreLocal(self):
        return self.lettreLocal

    def getTailleImageWidth(self):
        return self.tailleImageWidth

    def getTailleImageHeight(self):
        return self.tailleImageHeight

    def getMarginX(self):
        return self.marginX

    def getMarginY(self):
        return self.marginY

    def getSizeLettreLocal(self):
        return self.sizeLettreLocal

    def getDensite(self):
        return self.densite

    def getListeFigures(self):
        return self.listeFigures

    ############################SETTER
    def setNomFichier(self, nom):
        self.nomFichier = nom

    def setLettreGlobal(self, lG):
        self.lettreGlobal = lG

    def setLettreLocal(self, lL):
        self.nomFichier = lL

    def setTailleImageWidth(self, tailleX):
        self.tailleImageWidth = tailleX

    def setTailleImageHeight(self, tailleY):
        self.tailleImageHeight = tailleY

    def setMarginX(self, marge):
        self.marginX = marge

    def setMarginY(self, marge):
        self.marginY = marge

    def setSizeLettreLocal(self, size):
        self.sizeLettreLocal = size

    def setDensite(self, density):
        self.densite = density

    def setListeFigures(self, liste):
        self.listeFigures = liste


'''
monParseur = ParserListeFigures("C:/Users/Emilie Genton/Documents/GitHub/GenerateurFiguresNavon/Metier/text")
monParseur.recupererDonneesFichier()
'''
