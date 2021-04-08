class ElementGlobal:
    pass
    # ATTRIBUTS
    tailleGlobalX = 800
    tailleGlobalY = 800

    # CONSTRUCTEUR
    def __init__(self, tailleX, tailleY):
        self.tailleGlobalX = tailleX
        self.tailleGlobalY = tailleY

    ##############GETTER ET SETTER
    def setTailleGlobalX(self, newTailleX):
        self.tailleGlobalX = newTailleX

    def setTailleGlobalY(self, newTailleY):
        self.tailleGlobalY = newTailleY

    def getTailleGlobalX(self):
        return self.tailleGlobalX

    def getTailleGlobalY(self):
        return self.tailleGlobalY
