import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


class NF:
	"""
	class Navon's Figure (NF) represent a Navon's Figure with
	"""
	def __init__(self, d=100, char='A'):
		"""
		Constructor of NF
		:param d:
		:param char:
		"""
		self.lines = np.array([])
		self.arcs = np.array([])
		self.d = d  # Densité
		self.L = 5
		self.char = char

	def getG(self):
		"""
		Function that calculates the sum of all last element of each line
		"""
		last = np.array([])
		for line in self.lines:
			last = np.append(last, np.array(line.getL()[-1]))
		return sum(last)

	def getN(self):
		"""
		Function that calculates N
		"""
		return int(self.d / 100 * self.getG() / self.L)

	@staticmethod
	def fig2img(fig):
		"""
		Function that transforms the plt.figure into an image
		"""
		import io
		buf = io.BytesIO()
		fig.savefig(buf)
		buf.seek(0)
		img = Image.open(buf)
		return img


	def final(self):
		n = self.getN()
		# Create the plt figure
		figure = plt.figure()
		# A loop for each type of element
		for line in self.lines:
			line.changeY() #Function that will be change/ remove in the future, the Y axe of the canvas and the figure are reversed

			# Calculation by M. BARD
			a = np.linspace(0, 1, n)
			_x_, _y_ = line.interpolate()
			x_, y_ = _x_(a), _y_(a)
			plt.plot(_x_(line.getLDiv()), _y_(line.getLDiv()), 'w-')
			for i in range(0, len(x_)):
				plt.text(x_[i], y_[i], self.char, horizontalalignment="center", verticalalignment="center")

			line.changeY() # reversed a second time the value of Y to avoid problem when we add more element

		# not implemented yet
		for arc in self.arcs:
			...

		#Only show the outcome	
		plt.axis('equal')
		plt.axis('off')
		# plt.savefig(f"test.png")
		# plt.show()
		im = self.fig2img(figure)
		im.show()
