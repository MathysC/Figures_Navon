import numpy
import scipy.interpolate
import matplotlib.pyplot

# Je ne vois pas ce qu'est L
L = 0.4

# Si L est > 1 le programme crash
if L >1:
	print("L must be <=1")
	exit()


# La figure représentée est faite de deux segments et un demi cercle

# Premier Segment #y
x1 = numpy.array([ 0,  0, 0])
y1 = numpy.array([ 2,  1, 0])

# Deuxième Segment
x2 = numpy.array([ 0,  0, 0])
y2 = numpy.array([ 0, -1, -2])

# Demi cercle
t = numpy.linspace(-numpy.pi / 2, numpy.pi / 2, 10)
r = numpy.sqrt(1.0) # sqrt change rien vu que c'est 1
c = [(0 + r * numpy.cos(t_), 1 + r * numpy.sin(t_)) for t_ in t]
x3 = [c_[0] for c_ in c]
y3 = [c_[1] for c_ in c]

# Interpolation du premier segment
l1 = numpy.cumsum(numpy.sqrt(numpy.ediff1d(x1, to_begin = 0)**2 + numpy.ediff1d(y1, to_begin = 0)**2))
l = l1 / l1[-1]
_x1_ = scipy.interpolate.interp1d(l, x1)
_y1_ = scipy.interpolate.interp1d(l, y1)

# Interpolation du deuxième segment
l2 = numpy.cumsum(numpy.sqrt(numpy.ediff1d(x2, to_begin=0)**2 + numpy.ediff1d(y2, to_begin=0)**2))
l = l2 / l2[-1]
_x2_ = scipy.interpolate.interp1d(l, x2)
_y2_ = scipy.interpolate.interp1d(l, y2)

# Interpolation du troisième segment
l3 = numpy.cumsum(numpy.sqrt(numpy.ediff1d(x3, to_begin=0)**2 + numpy.ediff1d(y3, to_begin=0)**2))
l = l3/ l3[-1]
_x3_ = scipy.interpolate.interp1d(l, x3)
_y3_ = scipy.interpolate.interp1d(l, y3)

# Somme des derniers éléments des listes l1 l2 l3
g = sum([l1[-1], l2[-1], l3[-1]])

ite = 0 # Ite que j'ai rajouté, question d'ordre des fichiers dans l'arborescence
for d in [100, 80, 75, 50, 40, 33, 30, 25, 15]:	# d représente les pourcentages
	ite += 1
	n = int(d / 100 * g / L)
	n1 = n
	n3 = n
	
	while (l3[-1] / n3) > (l1[-1] / n1) :
			print(f"({format(l3[-1], '.2f')} / {n3}) > {l1[-1]} / {n1}")
			n3 +=1

	print(f"n°{ite} : n = {n} | n3 = {n3}") # Ligne rajoutée afin de voir les différentes valeurs 

	
	a = numpy.linspace(0, 1, n1)
	x1_, y1_ = _x1_(a), _y1_(a)
	x2_, y2_ = _x2_(a), _y2_(a)
	a = numpy.linspace(0, 1, n3)
	x3_, y3_ = _x3_(a), _y3_(a)


	matplotlib.pyplot.figure()
	matplotlib.pyplot.axis('equal');	

	# matplotlib.pyplot.title(f"d = {d} %")

	"""
	# Points bleus un peu avant 50%
	# Je ne sais pas à quoi ils servent
	matplotlib.pyplot.plot(x1, y1, 'bo');
	matplotlib.pyplot.plot(x2, y2, 'bo');
	matplotlib.pyplot.plot(x3, y3, 'bo');
	"""
	
	# Tracé vert de la figure 
	# Mettre la valeur 'w-' afin de ne pas voir apparaître le tracé
	# Il ne doit pas être visible mais doit être là sinon les lettres ne peuvent être placé
	matplotlib.pyplot.plot(_x1_(l), _y1_(l), 'g-')
	matplotlib.pyplot.plot(_x2_(l), _y2_(l), 'g-')
	matplotlib.pyplot.plot(_x3_(l), _y3_(l), 'g-')	

	"""
	# Points rouge représentant les emplacements des lettres
	matplotlib.pyplot.plot(x1_, y1_, 'ro')
	matplotlib.pyplot.plot(x2_, y2_, 'ro')
	matplotlib.pyplot.plot(x3_, y3_, 'ro')
	"""
	
	# Ajout des lettres locales au premier segment
	for i in range(0, len(x1_)) :
		 matplotlib.pyplot.text(x1_[i], y1_[i], 'U', horizontalalignment = "center", verticalalignment = "center")
	# Ajout des lettres locales au deuxième segment
	for i in range(0, len(x2_)) :
		matplotlib.pyplot.text(x2_[i], y2_[i], 'U', horizontalalignment = "center", verticalalignment = "center")
	# Ajout des lettres locales au troisième segment
	for i in range(0, len(x3_)) :
		matplotlib.pyplot.text(x3_[i], y3_[i], 'U', horizontalalignment = "center", verticalalignment = "center")
	
	#Enregistrement de la figure de Navon
	#matplotlib.pyplot.axis('off')
	matplotlib.pyplot.savefig(f"{ite} - {d} %.png")
	#matplotlib.pyplot.savefig(f"{ite} - {d} %.png", bbox_inches='tight', pad_inches=0)
