import numpy as np
import matplotlib.pyplot as plt


class NF:
	def __init__(self, d=100, char='A'):
		self.lines = np.array([])
		self.arcs = np.array([])
		self.d = d  # Densité
		self.L = 4
		self.char = char

	def getG(self):
		last = np.array([])
		for line in self.lines:
			last = np.append(last, np.array(line.getL()[-1]))
		return sum(last)

	def getN(self):
		return int(self.d / 100 * self.getG() / self.L)

	def final(self):
		n = self.getN()
		# Création de la figure
		plt.figure()

		# En fonction de chaque ligne
		for line in self.lines:
			#line.scale(10)
			line.changeY()
			a = np.linspace(0, 1, n)
			_x_, _y_ = line.interpolate()
			x_, y_ = _x_(a), _y_(a)

			plt.plot(_x_(line.getLDiv()), _y_(line.getLDiv()), 'g-')

			for i in range(0, len(x_)):
				plt.text(x_[i], y_[i], self.char, horizontalalignment="center", verticalalignment="center")

			#On refait le changement de Y en fin car s'il y a remodification de la NF, la line ne sera pas dans le bon sens
			line.changeY()
		# En fonction de chaque arc
		for arc in self.arcs:
			...

		plt.axis('equal')
		plt.axis('off')
		plt.savefig(f"test.png")
		plt.show()