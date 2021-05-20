from abc import ABC, abstractmethod
from Logic.Setup import Setup
import numpy as np


class Element(ABC):
	"""
	abstract class for elements
	"""
	def __init__(self, Xs=np.zeros(2), Ys=np.zeros(2)):
		"""
		Constructor of Element
		:param: Xs
		:type Xs: np.array
		:param: Ys:
		:type Xs: np.array
		"""
		self.x = np.copy(Xs)
		self.y = np.copy(Ys)
		self.id = None
		
	def getId(self):
		"""
		Getter of id
		:return: an id
		:rtype: int
		"""
		return self.id

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
		coord = np.array([])
		for i in range(0,len(self.x)):
			coord = np.append(coord,self.getX(i))
			coord = np.append(coord,self.getY(i))
		return coord

	# Calculation by M. BARD
	@abstractmethod
	def getL(self):
		pass

	def getLDiv(self):
		"""
		Function that calculates each value of the L array div by its last element
		"""
		return self.getL() / self.getL()[-1]

	@abstractmethod
	def interpolate(self):
		pass


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
