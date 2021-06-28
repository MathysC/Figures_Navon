import numpy as np
from PIL import Image, ImageFont, ImageDraw
from Logic.Setup import Setup
from Elements.Element import Element
from Elements import Line
import math


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
		self.density = 100  # Densité
		self.char = 'A'
		self.color = (0, 0, 0)
		self.size = 16
		self.police = "arial.ttf"

#___________________________________________________________________________________________________________________________
# Getter & Setter

	def getDensity(self) -> int:
		"""
		Getter of density
		:return: the density
		:rtype: int
		"""
		return self.density

	def setDensity(self, newD):
		"""
		Setter of density
		:param: newD
		:type newD: int
		"""
		self.density = newD

	def getChar(self) -> str:
		"""
		Getter of char
		:return: the char
		:rtype: str
		"""
		return self.char

	def setChar(self, newC):
		"""
		Setter of Char
		:param: newC
		:type newD: str
		"""
		self.char = newC

	def getSize(self) -> int:
		"""
		Getter of size
		:return: the Size
		:rtype: int
		"""
		return self.size

	def setSize(self, newS):
		"""
		Setter of size
		:param: newS
		:type newD: int
		"""
		self.size = newS

	def getPolice(self) -> str:
		"""
		Getter of police
		:return: the police
		:rtype: str
		"""
		return self.police

	def setPolice(self, newP):
		"""
		Setter of police
		:param: newP
		:type newD: str
		"""
		self.police = newP

	def getElements(self):
		return self.elements

	def setElements(self, newList):
		self.elements = newList

	def getElementById(self, toFound) -> Element:
		"""
		Getter of a single Element
		:param: toFound
		:type toFound: int
		:return: the element whose toFound value is id or None if nothing found
		:rtype: Element
		"""
		for element in self.elements:
			if element.id == toFound:
				return element
		return None

	def addElement(self, element):
		"""
		add an Element to Elements list
		:param: element
		:type element: Element
		"""
		self.elements = np.append(self.elements, np.array(element))

	def removeElement(self, element):
		"""
		remove an Element from Elements list
		:param: element
		:type element: Element
		"""
		self.elements = np.delete(self.elements, np.where(self.elements == element))
#___________________________________________________________________________________________________________________________
# Calculations for the Generation of the Navon's Figure

	def getG(self):
		"""
		Function that calculates the sum of length of all Elements
		:return: the sum of the last element 
		.. seealso:: Element.getL()
		"""
		last = np.array([])
		for element in self.elements:
			last = np.append(last, np.array(element.getL()[-1]))
		return sum(last)

	def getN(self, element, size, density) -> int:
		"""
		Function that calculates N 
		(The percentage * the sum of all length (g) / size of the local element ) / the length of the element / g
		:param element: the current element
		:type element: Element
		:param size: the size of the local element
		:type size: int
		:param density: the density of the NF
		:type density: int
		.. seealso:: self.getG()
		.. seealso:: Element.getL()
		"""
		try:
			g = self.getG()
			res = int((density / 100 * g / size) * element.getL()[-1] / g)
		except ValueError:
			res = 0
		return res


#___________________________________________________________________________________________________________________________
# Function to make appear element on the image 

	def printElement(self, element, draw, canvas):
			space = np.linspace(0, 1, self.getN(element=element, size=self.size, density=self.density))
			interp = element.interpolate()
			font = ImageFont.truetype(self.police+"ttf", self.size)
			# Return spaced number from getN() interval
			interp = element.interpolate()
			for i in range(0, len(interp), 2):
				_x_, _y_ = interp[i:i + 2]
				x_, y_ = self.prepareCoords(canvas, element, _x_(space), _y_(space), self.size)

				# Add local char to each coords
				for i in range(0, len(x_)):
					draw.text((x_[i], y_[i]), self.char, self.color, font=font)


	def printAllElements(self, draw, canvas):
		for element in self.elements:
			self.printElement(element, draw, canvas)

	def final(self, canvas):

		# Create the image
		im = Image.new('RGB', (int(Setup.WIDTH / 2) + self.size, Setup.HEIGHT + self.size), color='white')
		draw = ImageDraw.Draw(im)

		font = ImageFont.truetype(self.police, self.size)

		for element in self.elements:
			# Return spaced number from getN() interval
			a = np.linspace(0, 1, self.getN(element=element, size=self.size, density=self.density))
			interp = element.interpolate()
			for i in range(0, len(interp), 2):
				_x_, _y_ = interp[i:i + 2]
				x_, y_ = self.prepareCoords(canvas, element, _x_(a), _y_(a), self.size)

				# Add local char to each coords
				for i in range(0, len(x_)):
					draw.text((x_[i], y_[i]), self.char, self.color, font=font)

		# Save the OutCome
		im.show()
		im.save("Outcome/Testautre.png")

	def finalImage(self, canvas):
		localIm = Image.open('lena.jpg')  # Get local image
		lengthDiag = math.sqrt(localIm.width ** 2 + localIm.height ** 2)  # Get the length of its diagonal

		# We create an imaginary diagonal with the localIm in order to have the NF of correct size
		# does not appear on the final result
		diagonal = Line()
		diagonal.x = np.array([0, Setup.WIDTH])
		diagonal.y = np.array([0, Setup.HEIGHT])
		# The density of the diagonal need to be at 100%
		# Or the final Outcome will be awful
		a = np.linspace(0, 1, self.getN(diagonal, 16, density=100))
		_x_, _y_ = diagonal.interpolate()
		x_, y_ = _x_(a), _y_(a)

		# Create the Image for the NF
		im = Image.new('RGB',
		               (Setup.WIDTH + int(localIm.width * len(x_) + localIm.width),
		                Setup.HEIGHT + int(localIm.height * len(y_) + localIm.width)),
		               color='white')

		# The NF isn't at the same size as the draw Canvas, so we have to calculate the Scale diff
		Scale = np.array([
			(int(im.width) / Setup.WIDTH),
			(int(im.height) / Setup.HEIGHT)])

		# A loop for each type of element
		for element in self.elements:

			# Scale up the current element
			if element.getType() == "circle" or element.getType() == "semiCircle":
				# From the Center for the circle and semiCircle
				element.setRadius(int(element.getRadius() * Scale[0]))
				x, y = element.getCenter()
				element.setCenter(np.array([x * Scale[0], y * Scale[1]]))
				element.setX(0, x - element.getRadius())
				element.setY(0, y - element.getRadius())
				element.setX(1, x + element.getRadius())
				element.setY(1, y + element.getRadius())
			else:
				# From extremities for the line
				element.setX(0, element.getX(0) * Scale[0])
				element.setY(0, element.getY(0) * Scale[1])
				element.setX(1, element.getX(1) * Scale[0])
				element.setY(1, element.getY(1) * Scale[1])

			# Calculation of the coords of each local image
			a = np.linspace(0, 1, self.getN(element, lengthDiag, self.density))
			interp = element.interpolate()
			for i in range(0, len(interp), 2):
				_x_, _y_ = interp[i:i + 2]
				x_, y_ = self.prepareCoords(canvas, element, _x_(a), _y_(a), lengthDiag * 2)

				# Add local image to each coords
				for i in range(0, len(x_)):
					im.paste(localIm,
					         (int(x_[i] + localIm.width),
					          int(y_[i] + localIm.height)))

			# Scale down the current element
			if element.getType() == "circle" or element.getType() == "semiCircle":
				# From the Center for the circle and semiCircle
				element.setRadius(int(element.getRadius() / Scale[0]))
				x, y = element.getCenter()
				element.setCenter(np.array([x / Scale[0], y / Scale[1]]))
				element.setX(0, x + element.getRadius())
				element.setY(0, y + element.getRadius())
				element.setX(1, x - element.getRadius())
				element.setY(1, y - element.getRadius())
			else:
				element.setX(0, element.getX(0) / Scale[0])
				element.setY(0, element.getY(0) / Scale[1])
				element.setX(1, element.getX(1) / Scale[0])
				element.setY(1, element.getY(1) / Scale[1])

		# Only show the outcome
		im.show()

	# im.save("Outcome/NewTestImage3.png")

	def prepareCoords(self, canvas, element, x_, y_, gap):
		"""
		Remove from the list of coordinates (where images / local characters will be placed) 
		every point that is ~~ almost identical to the intersection
		"""
		ToDelete = np.array([])
		inter = np.array([])  # Array to distinguish intersections created by this element

		# Found all intersection created by this element
		for intersection in element.getIntersections():
			intersection = int(intersection)
			# We check who created this intersection with the second tag ('intersection', '-self.id','-otherElement.id')
			if canvas.gettags(intersection)[1] == f"-{element.getId()}":
				inter = np.append(inter, intersection)
		# Then for each of those intersection, check if there is a point (x_,y_) to delete
		for intersection in inter:
			intersection = int(intersection)

			# Get the point of the intersection
			coords = np.array([
				(canvas.coords(intersection)[0] + canvas.coords(intersection)[2]) / 2,
				(canvas.coords(intersection)[1] + canvas.coords(intersection)[3]) / 2])

			for ite in range(0, len(x_)):
				distance = int(math.hypot(coords[0] - x_[ite], coords[1] - y_[ite]))
				if distance < self.size / 2:
					ToDelete = np.append(ToDelete, ite)

			x_ = np.delete(x_, ToDelete.astype(int))
			y_ = np.delete(y_, ToDelete.astype(int))

		return x_, y_
