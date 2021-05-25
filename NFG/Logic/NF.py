import numpy as np
from PIL import Image, ImageFont, ImageDraw, ImageTk
from Logic.Setup import Setup
from IHM.elements.Element import Element
from IHM.elements.Line import Line


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

		self.elements = np.array([])
		self.d = None  # Densité
		self.char = 'A'
		self.color = (0, 0, 0)
		self.size = 16
		self.police = "arial.ttf"

	def getElementById(self,toFound)-> Element:
		"""
		Getter of a single Element
		"""
		for element in self.elements:
			if element.id == toFound:
				return element
		return None


	def getG(self):
		"""
		Function that calculates the sum of all last element of each line
		"""
		last = np.array([])
		for element in self.elements:
			last = np.append(last,np.array(element.getL()[-1]))
		return sum(last)

	def getN(self, element):
		"""
		Function that calculates N
		"""
		g = self.getG()
		return int((
						   self.d
						   / 100 *
					g / self.size) *
				   element.getL()[-1] / g)

	def getDuress(self, current):
		templist = np.delete(self.lines, np.where(self.lines == current))
		print("----------------------------------------------------------------------------------------------")
		print(f"Current : {current.getCoords()} :")
		for l in templist:
			print(f" Intersect with : {l.getCoords()} | {self.findIntersection(current, l)}")


	def final(self):
		# Create the image
		im = Image.new('RGB', (400 + self.size, 250 + self.size), color='white')
		draw = ImageDraw.Draw(im)

		font = ImageFont.truetype(self.police, self.size)

		for element in self.elements:
			a = np.linspace(0, 1, self.getN(element))
			interp = element.interpolate()
			for i in range(0,len(interp),2):
				_x_, _y_ = interp[i],interp[i+1]
				x_, y_ = _x_(a), _y_(a)

				# Add local char to each coords
				for i in range(0, len(x_)):
					draw.text((x_[i], y_[i]), self.char, self.color, font=font)

		# Save the OutCome
		im.show()
		im.save("Outcome/Testautre.png")

	def finalImage(self):
		# Get local image
		localIm = Image.open('lena.jpg')

		# A calculation with the diagonal of draw canvas to have the image of correct size
		# does not appear on the final result
		diagonal = Line()
		diagonal.x = np.array([0,Setup.WIDTH])
		diagonal.y = np.array([0,Setup.HEIGHT])
		a = np.linspace(0, 1, self.getN(diagonal))
		_x_, _y_ = diagonal.interpolate()
		x_, y_ = _x_(a), _y_(a)

		# Create the Image for the NF
		im = Image.new('RGB',
					   (Setup.WIDTH + int(localIm.width * len(x_)),
						Setup.HEIGHT + int(localIm.height * len(y_))),
					   color='white')

		# A loop for each type of element
		for element in self.elements:

			# Calculation by M. BARD
			a = np.linspace(0, 1, self.getN(element))
			interp = element.interpolate()
			for i in range(0,len(interp),2):
				_x_, _y_ = interp[i],interp[i+1]
				x_, y_ = _x_(a), _y_(a)
				
				# Add local image to each coords
				for i in range(0, len(x_)):
					im.paste(localIm,
							 (int(x_[i] + localIm.width),
							  int(y_[i] + localIm.height)))

			# Only show the outcome
		im.show()
		im.save("Outcome/NewTestImage2.png")
