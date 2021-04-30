from IHM.elements.Element import Element
from IHM.elements.Line import Line


class ElementFactory:
    """
    Factory pattern in order to create different element for the canvas
    """
    @staticmethod
    def Create(elementType) -> Element:
        """
        Factory method

        Without 'match case' statement because python 3.10 is not recommended for production
        (date 28 April 2021)

        :param elementType:
        :type elementType: str
        :return: A element that match elementType or None
        :rtype: Element
        """
        if elementType == "line":
            return Line([0, 0, 0, 0])
        elif elementType == "arc":
            ...
        elif elementType == "eraser":
            ...
        elif elementType == "mouse":
            ...
        else:
            return None
