import numpy
import scipy.interpolate
import matplotlib.pyplot

L = 0.125

x1 = numpy.array([0, 0, 0])
y1 = numpy.array([2, 1, 0])

l1 = numpy.cumsum(numpy.sqrt(numpy.ediff1d(x1, to_begin=0) ** 2 + numpy.ediff1d(y1, to_begin=0) ** 2))
l1_ = l1 / l1[-1]
_x1_ = scipy.interpolate.interp1d(l1_, x1)
_y1_ = scipy.interpolate.interp1d(l1_, y1)


x2 = numpy.array([0, 0, 0])
y2 = numpy.array([0, -1, -2])

l2 = numpy.cumsum(numpy.sqrt(numpy.ediff1d(x2, to_begin=0) ** 2 + numpy.ediff1d(y2, to_begin=0) ** 2))
l2_ = l2 / l2[-1]
_x2_ = scipy.interpolate.interp1d(l2_, x2)
_y2_ = scipy.interpolate.interp1d(l2_, y2)


# En bas à gauche
t = numpy.linspace(-numpy.pi/2,-numpy.pi, 10)
r = numpy.sqrt(1.0)
c = [(0 + r * numpy.cos(t_), 1 + r * numpy.sin(t_)) for t_ in t]
x3 = [c_[0] for c_ in c]
y3 = [c_[1] for c_ in c]

l3 = numpy.cumsum(numpy.sqrt(numpy.ediff1d(x3, to_begin=0) ** 2 + numpy.ediff1d(y3, to_begin=0) ** 2))
l3_ = l3 / l3[-1]
_x3_ = scipy.interpolate.interp1d(l3_, x3)
_y3_ = scipy.interpolate.interp1d(l3_, y3)


# En haut à gauche
t = numpy.linspace(numpy.pi, numpy.pi/2 , 10)
r = numpy.sqrt(1.0)
c = [(0 + r * numpy.cos(t_), 1 + r * numpy.sin(t_)) for t_ in t]
x4 = [c_[0] for c_ in c]
y4 = [c_[1] for c_ in c]

l4 = numpy.cumsum(numpy.sqrt(numpy.ediff1d(x4, to_begin=0) ** 2 + numpy.ediff1d(y4, to_begin=0) ** 2))
l4_ = l4 / l4[-1]
_x4_ = scipy.interpolate.interp1d(l4_, x4)
_y4_ = scipy.interpolate.interp1d(l4_, y4)

# En haut à droite
t = numpy.linspace(numpy.pi/2, 0,  10)
r = numpy.sqrt(1.0)
c = [(0 + r * numpy.cos(t_), 1 + r * numpy.sin(t_)) for t_ in t]
x5 = [c_[0] for c_ in c]
y5 = [c_[1] for c_ in c]

l5 = numpy.cumsum(numpy.sqrt(numpy.ediff1d(x5, to_begin=0) ** 2 + numpy.ediff1d(y5, to_begin=0) ** 2))
l5_ = l5 / l5[-1]
_x5_ = scipy.interpolate.interp1d(l5_, x5)
_y5_ = scipy.interpolate.interp1d(l5_, y5)


# En bas à droite
t = numpy.linspace(0, -numpy.pi/2,  10)
r = numpy.sqrt(1.0)
c = [(0 + r * numpy.cos(t_), 1 + r * numpy.sin(t_)) for t_ in t]
x6 = [c_[0] for c_ in c]
y6 = [c_[1] for c_ in c]


l6 = numpy.cumsum(numpy.sqrt(numpy.ediff1d(x6, to_begin=0) ** 2 + numpy.ediff1d(y6, to_begin=0) ** 2))
l6_ = l6 / l6[-1]
_x6_ = scipy.interpolate.interp1d(l6_, x6)
_y6_ = scipy.interpolate.interp1d(l6_, y6)


g = sum([l1[-1], l2[-1], l3[-1],l4[-1],l5[-1],l6[-1]])

for d in [100, 80, 75, 50, 40, 33, 30, 25, 15 ]: #

    n = d / 100 * g / L
    n1 = round(n * l1[-1] / g)
    n2 = round(n * l2[-1] / g)
    n3 = round(n * l3[-1] / g)
    n4 = round(n * l4[-1] / g)
    n5 = round(n * l5[-1] / g)  
    n6 = round(n * l6[-1] / g)
    
    #while (l3[-1] / n3) > (l1[-1] / n1):
    #    n3 += 1

    #while (l4[-1] / n4) > (l1[-1] / n1):
    #    n4 += 1

    #while (l5[-1] / n5) > (l1[-1] / n1):
    #    n5 += 1

    #while (l6[-1] / n6) > (l1[-1] / n1):
    #    n6 += 1

    a = numpy.linspace(0, 1, n1)
    x1_, y1_ = _x1_(a), _y1_(a)
    a = numpy.linspace(0, 1, n2)
    x2_, y2_ = _x2_(a), _y2_(a)
    a = numpy.linspace(0, 1, n3)
    x3_, y3_ = _x3_(a), _y3_(a)

    a = numpy.linspace(0, 1, n4)
    x4_, y4_ = _x4_(a), _y4_(a)

    a = numpy.linspace(0, 1, n5)
    x5_, y5_ = _x5_(a), _y5_(a)

    a = numpy.linspace(0, 1, n6)
    x6_, y6_ = _x6_(a), _y6_(a)

    matplotlib.pyplot.figure()
    matplotlib.pyplot.title(f"Navon4\nd = {d} %")

    """
	matplotlib.pyplot.plot(x1, y1, 'bo');
	matplotlib.pyplot.plot(x2, y2, 'bo');
	matplotlib.pyplot.plot(x3, y3, 'bo');
	"""

    matplotlib.pyplot.plot(_x1_(l1_), _y1_(l1_), 'w-')
    matplotlib.pyplot.plot(_x2_(l2_), _y2_(l2_), 'w-')
    matplotlib.pyplot.plot(_x3_(l3_), _y3_(l3_), 'w-')
    matplotlib.pyplot.plot(_x4_(l4_), _y4_(l4_), 'w-')
    matplotlib.pyplot.plot(_x5_(l5_), _y5_(l5_), 'w-')
    matplotlib.pyplot.plot(_x6_(l6_), _y6_(l6_), 'w-')

    """
	matplotlib.pyplot.plot(x1_, y1_, 'ro')
	matplotlib.pyplot.plot(x2_, y2_, 'ro')
	matplotlib.pyplot.plot(x3_, y3_, 'ro')
	"""

    for i in range(0, len(x1_)):
        matplotlib.pyplot.text(x1_[i], y1_[i], 'U', horizontalalignment="center", verticalalignment="center")
    for i in range(0, len(x2_)):
        matplotlib.pyplot.text(x2_[i], y2_[i], 'U', horizontalalignment="center", verticalalignment="center")
    for i in range(0, len(x3_)):
        matplotlib.pyplot.text(x3_[i], y3_[i], 'U', horizontalalignment="center", verticalalignment="center")    
    for i in range(0, len(x4_)):
        matplotlib.pyplot.text(x4_[i], y4_[i], 'U', horizontalalignment="center", verticalalignment="center")    
    for i in range(0, len(x5_)):
        matplotlib.pyplot.text(x5_[i], y5_[i], 'U', horizontalalignment="center", verticalalignment="center")
    for i in range(0, len(x6_)):
        matplotlib.pyplot.text(x6_[i], y6_[i], 'U', horizontalalignment="center", verticalalignment="center")

    matplotlib.pyplot.axis('equal');
    matplotlib.pyplot.savefig(f"Navon4/{d} %.png")
