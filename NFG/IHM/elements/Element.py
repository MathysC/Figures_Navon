from abc import ABC, abstractmethod
from Logic.Setup import Setup
import numpy as np
import scipy.interpolate as itp


class Element(ABC):
    def __init__(self, Xs, Ys):
        self.x = np.copy(Xs)
        self.y = np.copy(Ys)

    def getX(self, i):
        return self.x[i]

    def setX(self, i, value):
        self.x[i] = value

    def getY(self, i):
        return self.y[i]

    def setY(self, i, value):
        self.y[i] = value

    def getCoords(self):
        return np.array([self.getX(0), self.getY(0), self.getX(1), self.getY(1)])

    def changeY(self):
        self.setY(0, Setup.WIDTH - self.getY(0))
        self.setY(1, Setup.WIDTH - self.getY(1))

    @abstractmethod
    def getType(self):
        pass

    def getL(self):
        return np.cumsum(
            np.sqrt(
                np.ediff1d(self.x, to_begin=0) ** 2
                + np.ediff1d(self.y, to_begin=0) ** 2))

    def getLDiv(self):
        return self.getL() / self.getL()[-1]

    def interpolate(self):
        _x_ = itp.interp1d(self.getLDiv(), self.x)
        _y_ = itp.interp1d(self.getLDiv(), self.y)
        return _x_, _y_

    # Méthodes pour le canvas
    @abstractmethod
    def start(self, **kwargs):
        pass

    @abstractmethod
    def motion(self, **kwargs):
        pass

    @abstractmethod
    def end(self, **kwargs):
        pass
