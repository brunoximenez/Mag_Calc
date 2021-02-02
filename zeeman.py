import numpy as np 
import matplotlib.pyplot as plt 
import sys


def gf(F, J=.5, I=3/2, L=0, S=.5):

	gj = J*(J+1) - L*(L+1) - S*(S+1)
	gj = gj / (2 * J * (J + 1))
	gj += 1

	g_f = gj * ( F * ( F + 1) + J * (J + 1) - I * (I + 1) )
	g_f = g_f / (2 * F * (F + 1))

	return g_f


def Hz():
	# Bohr magneton
	mu_B = 9.2740100783e-24 # J T^-1
	#  Initialize full Hamiltonian matrix
	H = np.zeros((8,8), dtype=float)
	
	# Subspace mf = +/-
	H[0,0] = 2 * mu_B * gf(2)
	H[1,1] = - H[0,0]

	# mf = 1; F=1, F=2
	 



def main():
	Hz()
	


main()