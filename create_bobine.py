import numpy as np
import matplotlib.pyplot as plt
from magpylib.source.magnet import Box, Cylinder
from magpylib.source.current import Circular
from magpylib import Collection, displaySystem

fontsize = 18


def bobine(current, diameter, n_coils, distance, rotate=False):

    dx_coils = 4.

    coil_setup = Collection()
    for j in range(n_coils):
        z = j * dx_coils + distance / 2
        coil_p = Circular(curr=current, dim=diameter, pos=([0, 0, z]))
        if rotate == True: coil_p.rotate(10, [1, 0, 0], anchor=[0, 0, 0])
        coil_m = Circular(curr=current, dim=diameter, pos=([0, 0, - z]))
        coil_setup.addSources(coil_p, coil_m)

    return coil_setup


def calc_mod(b):
    b_mod = 0
    for i in range(3):
        b_mod += b[i] ** 2

    return np.sqrt(b_mod)


def B_array(coll, distance):
    # Distances in mm
    dx = 200.
    n_points = 100
    z = np.array([])
    b = np.array([])
    label = 'Distance between coils: ' + str(distance) + ' mm'
    for j in range(1, n_points + 1):
        x = j * dx / n_points
        b_calc = coll.getB([0, 0, x])
        print(b_calc)
        b = np.append(b, calc_mod(b_calc))
        z = np.append(z, x)
        b_calc = coll.getB([0, 0, - x])
        b = np.append(b, calc_mod(b_calc))
        z = np.append(z, - x)
    plt.figure('Magnetic Field')
    plt.plot(z, b, 'o', label=label)
    plt.ylabel('B (mT)', fontsize=fontsize)
    plt.xlabel('z (mm)', fontsize=fontsize)
    plt.legend(fontsize=14)
    # plt.show()


def heat_dissipated():
	#ohm mm2 /m
	rho = 0.0171
	N = 4
	r_coil = 40e-3 # in m
	r_wire = 1.5 # in mm
	I = 20 # Amps

	L = N * 2 * 3.14 * r_coil
	r_sol = 2 * r_coil * N * rho / (r_wire ** 2)
	print('Resistance solenoid:')
	print(r_sol)
	p_dissipated = r_sol * I ** 2
	print('Power dissipated:')
	print(p_dissipated)
	print('Total lenght of sol:')
	print(L)