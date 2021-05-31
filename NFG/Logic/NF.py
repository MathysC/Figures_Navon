import numpy as np
from PIL import Image, ImageFont, ImageDraw, ImageTk
from Logic.Setup import Setup
from IHM.elements.Element import Element
from IHM.elements.Line import Line
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

	def addElement(self,element):
		self.elements = np.append(self.elements,np.array(element))

	def removeElement(self,element):
		self.elements = np.delete(self.elements,np.where(self.elements == element))

	def getG(self):
		"""
		Function that calculates the sum of all last element of each line
		"""
		last = np.array([])
		for element in self.elements:
			last = np.append(last,np.array(element.getL()[-1]))
		return sum(last)


	def getN(self, element,size):
		"""
		Function that calculates N
		"""
		g = self.getG()
		return int((
						   self.d
						   / 100 *
					g / size) *
				   element.getL()[-1] / g)

	def final(self, canvas):
		# Create the image
		im = Image.new('RGB', (400 + self.size, 250 + self.size), color='white')
		draw = ImageDraw.Draw(im)

		font = ImageFont.truetype(self.police, self.size)

		for element in self.elements:
			a = np.linspace(0, 1, self.getN(element,self.size))
			interp = element.interpolate()
			for i in range(0,len(interp),2):
				_x_, _y_ = interp[i:i+2]
				x_, y_ = self.prepareCoords(canvas,element,_x_(a), _y_(a), self.size)
				

				# Add local char to each coords
				for i in range(0, len(x_)):
					draw.text((x_[i], y_[i]), self.char, self.color, font=font)

		# Save the OutCome
		im.show()
		im.save("Outcome/Testautre.png")

	def finalImage(self, canvas):
		# Get local image
		localIm = Image.open('lena.jpg')
		size =math.sqrt(localIm.width**2 + localIm.height**2)



		# A calculation with the diagonal of draw canvas to have the image of correct size
		# does not appear on the final result
		diagonal = Line()
		diagonal.x = np.array([0,Setup.WIDTH])
		diagonal.y = np.array([0,Setup.HEIGHT])
		tempDensity = 100
		self.d,tempDensity = tempDensity,self.d




		a = np.linspace(0, 1, self.getN(diagonal,size/2))
		_x_, _y_ = diagonal.interpolate()
		x_, y_=_x_(a), _y_(a)
		# Create the Image for the NF
		im = Image.new('RGB',
			(Setup.WIDTH + int(localIm.width * len(x_)),
			Setup.HEIGHT + int(localIm.height * len(y_))),
			color='white')
		# A loop for each type of element
		Scale = np.array([
		 (( Setup.WIDTH + int(localIm.width * len(x_)) ) / Setup.WIDTH )+localIm.width ,
		 (( Setup.HEIGHT + int(localIm.height * len(y_)) ) / Setup.HEIGHT) + localIm.height] )

		self.d = tempDensity

		for element in self.elements:
			# Scale up the coords of the element

			if element.getType() == "circle" or element.getType()=="semiCircle":
				# From the Center for the circle and semiCircle
				element.setRadius(int(element.getRadius()*Scale[0]))
				x,y = element.getCenter()
				element.setCenter(np.array([x*Scale[0], y*Scale[1]]))
				element.setX(0,x-element.getRadius())
				element.setY(0,y-element.getRadius())
				element.setX(1,x+element.getRadius())
				element.setY(1,y+element.getRadius())
			else:
				#From extremities for the line
				element.setX(0,element.getX(0)*Scale[0])
				element.setY(0,element.getY(0)*Scale[1])
				element.setX(1,element.getX(1)*Scale[0])
				element.setY(1,element.getY(1)*Scale[1])

			# Calculation by M. BARD
			a = np.linspace(0, 1, self.getN(element, size))
			interp = element.interpolate()
			for i in range(0,len(interp),2):
				# Check the intersections
				_x_, _y_ = interp[i:i+2]
				x_, y_ = self.prepareCoords(canvas,element,_x_(a), _y_(a),size/2)
				
				# Add local image to each coords
				for i in range(0, len(x_)):
					im.paste(localIm,
							 (int(x_[i] + localIm.width),
							  int(y_[i] + localIm.height)))

			if element.getType() == "circle" or element.getType()=="semiCircle":
				element.setRadius(int(element.getRadius()/Scale[0]))
				x,y = element.getCenter()
				element.setCenter(np.array([x/Scale[0], y/Scale[1]]))
				element.setX(0,x+element.getRadius())
				element.setY(0,y+element.getRadius())
				element.setX(1,x-element.getRadius())
				element.setY(1,y-element.getRadius())
			else:
				element.setX(0,element.getX(0)/Scale[0])
				element.setY(0,element.getY(0)/Scale[1])
				element.setX(1,element.getX(1)/Scale[0])
				element.setY(1,element.getY(1)/Scale[1])

			# Only show the outcome
		im.show()
		im.save("Outcome/NewTestImage2.png")

	def prepareCoords(self, canvas, element, x_, y_, size):
		"""
		Remove from the list of coordinates (where images / local characters will be placed) 
		every point that is ~~ almost identical to the intersection
		"""
		ToDeletex_ = np.array([])
		ToDeletey_ = np.array([])
		inter = np.array([]) # Array to distinguish intersections created by this element 


		# Found all intersection created by this element 
		for intersection in element.getIntersections():
			intersection = int(intersection)
			# We check who created this intersection with the second tag ('intersection', '-self.id','-otherElement.id')
			if canvas.gettags(intersection)[1] == f"-{element.getId()}" :
				inter = np.append(inter,intersection)
		# Then for each of those intersection, check if there is a point (x_,y_) to delete
		for intersection in inter:
			intersection = int(intersection)

			# Get the point of the intersection
			coords =np.array([
				canvas.coords(intersection)[0]+Setup.RADIUSINTER,
				canvas.coords(intersection)[1]+Setup.RADIUSINTER])

			for ite in range(0,len(x_)):
				distance = int(math.hypot(coords[0] - x_[ite], coords[1] - y_[ite]))
				if distance <= size:
					ToDeletex_ = np.append(ToDeletex_, x_[ite])
					ToDeletey_ = np.append(ToDeletey_, y_[ite])

			for x in ToDeletex_:
				x_ = np.delete(x_,np.where(x_ == x))
				
			for y in ToDeletey_:
				y_ = np.delete(y_,np.where(y_ == y))

		return x_,y_
