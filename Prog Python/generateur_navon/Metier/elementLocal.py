class elementLocal:
    # ATTRIBUTS
    police = "time"
    taillePolice = 15

    # CONSTRUCTEUR
    def __init__(self, laPolice, taille):
        self.police = laPolice
        self.taillePolice = taille

    # GETTER ET SETTER
    def getPolice(self):
        return self.police

    def getTaillePolice(self):
        return self.taillePolice

    def setPolice(self,newPolice):
        self.police = newPolice

    def setTaillePolice(self,newTaille):
        self.taillePolice = newTaille
