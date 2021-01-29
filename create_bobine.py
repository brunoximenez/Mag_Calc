import numpy as np
import matplotlib.pyplot as plt
from magpylib.source.magnet import Box, Cylinder
from magpylib.source.current import Circular
from magpylib import Collection, displaySystem


def bobine(current, diameter, n_coils, distance):

	distance = diameter 
	dx_coils = 0.3

	coil_setup = Collection()
	for j in range(n_coils):
		z = j * dx_coils + distance / 2
		coil_p = Circular(curr=current, dim=diameter, pos=(0, 0, z))
		coil_m = Circular(curr=current, dim=diameter, pos=(0, 0, - z))
		coil_setup.addSources(coil_p, coil_m)

	return coil_setup


def calc_mod(b):
	b_mod = 0
	for i in range(3):
		b_mod += b[i] ** 2

	return np.sqrt(b_mod)



def B_array(coll):
	# Distances in mm
	dx = 0.2
	n_points = 100
	z = np.array([])
	b = np.array([])
	for j in range(1, n_points + 1):
		x = j * dx / n_points
		b_calc = coll.getB([0,0,x])
		print(b_calc)
		b = np.append(b, calc_mod(b_calc))
		z = np.append(z, x)
		b_calc = coll.getB([0,0, - x])
		b = np.append(b, - calc_mod(b_calc))
		z = np.append(z, - x)
	plt.plot(z, b, 'o')
	print(b)
	# plt.show()

