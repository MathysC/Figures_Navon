from IHM.elements.Element import Element
from IHM.elements.Line import Line
from IHM.elements.SemiCircle import SemiCircle
from IHM.elements.Eraser import Eraser
from IHM.elements.Circle import Circle

class ElementFactory:
	"""
	Factory pattern in order to create different element for the canvas
	"""
	@staticmethod
	def Create(elementType) -> Element:
		"""
		Factory method

		Without 'match case' statement because python 3.10 is not recommended for production
		(wrote this comment : 28 April 2021)

		:param: elementType
		:type elementType: str
		:return: A element that match elementType or None
		:rtype: Element
		"""
		if elementType == "line":
			return Line()
		elif elementType == "semiCircle":
			return SemiCircle()
		elif elementType == "circle":
			return Circle()
		elif elementType == "eraser":
			return Eraser()
		else:
			return None
