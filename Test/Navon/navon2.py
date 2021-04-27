import numpy
import scipy.interpolate
import matplotlib.pyplot


N = 10


x1 = numpy.array([ 0,  0, 0])
y1 = numpy.array([ 2,  1, 0])

x2 = numpy.array([ 0,  0, 0])
y2 = numpy.array([ 0, -1, -2])

x3 = numpy.array([ 0,  1])
y3 = numpy.array([ 2,  2])

x4 = numpy.array([ 0,  1])
y4 = numpy.array([ 0,  0,])

t = numpy.linspace(-numpy.pi / 2, numpy.pi / 2, 10)
r = numpy.sqrt(1.0)
c = [(1 + r * numpy.cos(t_), 1 + r * numpy.sin(t_)) for t_ in t]
x5 = [c_[0] for c_ in c]
y5 = [c_[1] for c_ in c]


d = numpy.cumsum(numpy.sqrt(numpy.ediff1d(x1, to_begin = 0)**2 + numpy.ediff1d(y1, to_begin = 0)**2 ))
d = d/d[-1]
_x1_, _y1_ = scipy.interpolate.interp1d( d, x1 ), scipy.interpolate.interp1d( d, y1 )

d = numpy.cumsum(numpy.sqrt( numpy.ediff1d(x2, to_begin=0)**2 + numpy.ediff1d(y2, to_begin=0)**2 ))
d = d/d[-1]
_x2_, _y2_ = scipy.interpolate.interp1d( d, x2 ), scipy.interpolate.interp1d( d, y2 )

d = numpy.cumsum(numpy.sqrt( numpy.ediff1d(x3, to_begin=0)**2 + numpy.ediff1d(y3, to_begin=0)**2 ))
d = d/d[-1]
_x3_, _y3_ = scipy.interpolate.interp1d( d, x3 ), scipy.interpolate.interp1d( d, y3 )

d = numpy.cumsum(numpy.sqrt( numpy.ediff1d(x4, to_begin=0)**2 + numpy.ediff1d(y4, to_begin=0)**2 ))
d = d/d[-1]
_x4_, _y4_ = scipy.interpolate.interp1d( d, x4 ), scipy.interpolate.interp1d( d, y4 )

d = numpy.cumsum(numpy.sqrt( numpy.ediff1d(x5, to_begin=0)**2 + numpy.ediff1d(y5, to_begin=0)**2 ))
d = d/d[-1]
_x5_, _y5_ = scipy.interpolate.interp1d( d, x5 ), scipy.interpolate.interp1d( d, y5 )


for n in range(2, N) :

	a = numpy.linspace(0, 1, n)
	x1_, y1_ = _x1_(a), _y1_(a)
	x2_, y2_ = _x2_(a), _y2_(a)
	x3_, y3_ = _x3_(a), _y3_(a)
	x4_, y4_ = _x4_(a), _y4_(a)
	x5_, y5_ = _x5_(a), _y5_(a)


	matplotlib.pyplot.figure()
	matplotlib.pyplot.title(f"n = {n}")

	matplotlib.pyplot.plot(x1, y1, 'bo');
	matplotlib.pyplot.plot(x2, y2, 'bo');
	matplotlib.pyplot.plot(x3, y3, 'bo');
	matplotlib.pyplot.plot(x4, y4, 'bo');
	matplotlib.pyplot.plot(x5, y5, 'bo');

	matplotlib.pyplot.plot(_x1_(d), _y1_(d), 'g-');
	matplotlib.pyplot.plot(_x2_(d), _y2_(d), 'g-');
	matplotlib.pyplot.plot(_x3_(d), _y3_(d), 'g-');
	matplotlib.pyplot.plot(_x4_(d), _y4_(d), 'g-');
	matplotlib.pyplot.plot(_x5_(d), _y5_(d), 'g-');

	matplotlib.pyplot.plot(x1_, y1_, 'ro');
	matplotlib.pyplot.plot(x2_, y2_, 'ro');
	matplotlib.pyplot.plot(x3_, y3_, 'ro');
	matplotlib.pyplot.plot(x4_, y4_, 'ro');
	matplotlib.pyplot.plot(x5_, y5_, 'ro');

	matplotlib.pyplot.axis('equal');
	matplotlib.pyplot.show()
	#matplotlib.pyplot.savefig(f"{n}.png")
