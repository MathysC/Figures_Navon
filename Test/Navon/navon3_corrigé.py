import numpy
import scipy.interpolate
import matplotlib.pyplot
import tkinter as tk
from PIL import Image

def func():
	L = 0.4


	x1 = numpy.array([ 0,  0, 0])
	y1 = numpy.array([ 2,  1, 0])

	x2 = numpy.array([ 0,  0, 0])
	y2 = numpy.array([ 0, -1, -2])

	t = numpy.linspace(-numpy.pi / 2, numpy.pi / 2, 10)
	r = numpy.sqrt(1.0)
	c = [(0 + r * numpy.cos(t_), 1 + r * numpy.sin(t_)) for t_ in t]
	x3 = [c_[0] for c_ in c]
	y3 = [c_[1] for c_ in c]


	l1 = numpy.cumsum(numpy.sqrt(numpy.ediff1d(x1, to_begin = 0)**2 + numpy.ediff1d(y1, to_begin = 0)**2))
	l1_ = l1 / l1[-1]
	_x1_ = scipy.interpolate.interp1d(l1_, x1)
	_y1_ = scipy.interpolate.interp1d(l1_, y1)

	l2 = numpy.cumsum(numpy.sqrt(numpy.ediff1d(x2, to_begin=0)**2 + numpy.ediff1d(y2, to_begin=0)**2))
	l2_ = l2 / l2[-1]
	_x2_ = scipy.interpolate.interp1d(l2_, x2)
	_y2_ = scipy.interpolate.interp1d(l2_, y2)

	l3 = numpy.cumsum(numpy.sqrt(numpy.ediff1d(x3, to_begin=0)**2 + numpy.ediff1d(y3, to_begin=0)**2))
	l3_ = l3/ l3[-1]
	_x3_ = scipy.interpolate.interp1d(l3_, x3)
	_y3_ = scipy.interpolate.interp1d(l3_, y3)


	g = sum([l1[-1], l2[-1], l3[-1]])
	for d in [100, 80, 75, 50, 40, 33, 30, 25, 15] : #
		
		
		n = int(d / 100 * g / L)

		n1 = n # * l1[-1] / g (pourcentage que le trait représente dans la figure)
		n3 = n
		
		while (l3[-1] / n3) > (l1[-1] / n1) :
				n3 +=1
		
		a = numpy.linspace(0, 1, n1)
		x1_, y1_ = _x1_(a), _y1_(a)
		x2_, y2_ = _x2_(a), _y2_(a)
		a = numpy.linspace(0, 1, n3)
		x3_, y3_ = _x3_(a), _y3_(a)


		figure = matplotlib.pyplot.figure()
		matplotlib.pyplot.title(f"Navon3\nd = {d} %")

		"""
		matplotlib.pyplot.plot(x1, y1, 'bo');
		matplotlib.pyplot.plot(x2, y2, 'bo');
		matplotlib.pyplot.plot(x3, y3, 'bo');
		"""
		
		
		matplotlib.pyplot.plot(_x1_(l1_), _y1_(l1_), 'g-')
		matplotlib.pyplot.plot(_x2_(l2_), _y2_(l2_), 'g-')
		matplotlib.pyplot.plot(_x3_(l3_), _y3_(l3_), 'g-')
		
		
		"""
		matplotlib.pyplot.plot(x1_, y1_, 'ro')
		matplotlib.pyplot.plot(x2_, y2_, 'ro')
		matplotlib.pyplot.plot(x3_, y3_, 'ro')
		"""
		
		for i in range(0, len(x1_)) :
			 matplotlib.pyplot.text(x1_[i], y1_[i], 'U', horizontalalignment = "center", verticalalignment = "center")
		for i in range(0, len(x2_)) :
			matplotlib.pyplot.text(x2_[i], y2_[i], 'U', horizontalalignment = "center", verticalalignment = "center")
		for i in range(0, len(x3_)) :
			matplotlib.pyplot.text(x3_[i], y3_[i], 'U', horizontalalignment = "center", verticalalignment = "center")

		matplotlib.pyplot.axis('equal')
		#matplotlib.pyplot.axis('off')
		matplotlib.pyplot.savefig(f"Navon3/{d} %.png")
		#im = fig2img(figure)
		#im.show()

def fig2img(fig):
    """Convert a Matplotlib figure to a PIL Image and return it"""
    import io
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img


mainWindow = tk.Tk()
mainWindow.title("générateur de Navon")
mainWindow.geometry("600x500")
mainWindow.resizable(False, False)
print_Button = tk.Button(width=10, height=3, text="preview", command=func)
print_Button.pack()

mainWindow.mainloop()