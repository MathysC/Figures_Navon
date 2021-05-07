import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageFont, ImageDraw,ImageTk


class NF:
	"""
	class Navon's Figure (NF) represent a Navon's Figure with
	"""
	def __init__(self):
		"""
		Constructor of NF
		:param d:
		:param char:
		"""
		self.lines = np.array([])
		self.arcs = np.array([])
		self.d = None  # Densité
		self.char = 'A'
		self.color = (0,0,0)
		self.size = 16
		self.police = "arial.ttf"
	def getG(self):
		"""
		Function that calculates the sum of all last element of each line
		"""
		last = np.array([])
		for line in self.lines:
			last = np.append(last, np.array(line.getL()[-1]	))
		return sum(last)

	def getN(self,line):
		"""
		Function that calculates N
		"""
		g = self.getG()
		return int((self.d / 100 * g  / self.size) * line.getL()[-1] / g )


	def final(self):
		# Create the image
		im = Image.new('RGB', (400+self.size, 250+self.size), color='white')
		draw = ImageDraw.Draw(im)

		font = ImageFont.truetype(self.police, self.size)

		# A loop for each type of element
		for line in self.lines:
			
			
			# Calculation by M. BARD
			a = np.linspace(0, 1, self.getN(line))
			_x_, _y_ = line.interpolate()
			x_, y_ = _x_(a), _y_(a)

			# Add local char to each coords
			for i in range(0,len(x_)):
				draw.text((x_[i],y_[i]),self.char,self.color,font=font)

		# not implemented yet
		for arc in self.arcs:
			...

		#Only show the outcome	
		im.show()
		im.save("text.png")
