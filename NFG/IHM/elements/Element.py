from abc import ABC, abstractmethod
from Logic.Setup import Setup
import numpy as np
import scipy.interpolate as itp


class Element(ABC):
    """
    abstract class for elements
    """
    def __init__(self, Xs, Ys):
        """
        Constructor of Element
        :param: Xs
        :type Xs: np.array
        :param: Ys:
        :type Xs: np.array
        """
        self.x = np.copy(Xs)
        self.y = np.copy(Ys)

    def getX(self, i):
        """
        Getter of one value of X
        :param: i
        :type i: int
        """
        return self.x[i]

    def setX(self, i, value):
        """
        Setter of one value of X
        :param: i
        :type i: int
        :param: value
        :type value: int
        """
        self.x[i] = value

    def getY(self, i):
        """
        Getter of one value of Y
        :param: i
        :type i: int
        """
        return self.y[i]

    def setY(self, i, value):
        """
        Setter of one value of Y
        :param: i
        :type i: int
        :param: value
        :type value: int
        """
        self.y[i] = value

    def getCoords(self):
        """
        Getter of Coords
        """
        return np.array([self.getX(0), self.getY(0), self.getX(1), self.getY(1)])

    def changeY(self):
        """
        Function that will be change / remove in the future
        Change the Y value by its opposite
        """
        self.setY(0, Setup.WIDTH - self.getY(0))
        self.setY(1, Setup.WIDTH - self.getY(1))


    # Calculation by M. BARD
    def getL(self):
        """
        Function that calculates L
        """
        return np.cumsum(
            np.sqrt(
                np.ediff1d(self.x, to_begin=0) ** 2
                + np.ediff1d(self.y, to_begin=0) ** 2))

    def getLDiv(self):
        """
        Function that calculates each value of the L array div by its last element
        """
        return self.getL() / self.getL()[-1]

    def interpolate(self):
        """
        Function taht calcultates the interpolation of X and Y of the element
        """
        _x_ = itp.interp1d(self.getLDiv(), self.x)
        _y_ = itp.interp1d(self.getLDiv(), self.y)
        return _x_, _y_


    @abstractmethod
    def getType(self):
        pass

    @abstractmethod
    def start(self, **kwargs):
        pass

    @abstractmethod
    def motion(self, **kwargs):
        pass

    @abstractmethod
    def end(self, **kwargs):
        pass
