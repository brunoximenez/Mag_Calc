import numpy as np 
import matplotlib.pyplot as plt 
import sys


h = 6.62606976e-34  # J*s

def gf(F, J=.5, I=3/2, L=0, S=.5):

	gj = J*(J+1) - L*(L+1) + S*(S+1)
	gj = gj / (2 * J * (J + 1))
	gj += 1
	print

	g_f = gj * ( F * ( F + 1) + J * (J + 1) - I * (I + 1) )
	g_f = g_f / (2 * F * (F + 1))

	return g_f


def K(F, I=3/2, J=.5):
	k = .5 * (F*(F+1) - I*(I+1) - J*(J+1))
	return k


def H_hfs(F):
	a = 3.417341e3 # MHz
	x = a * K(F)
	print(x)
	return x


def H(B):
	'''
	Calculates the Zeeman Hamiltonian of the system
	given a B field in T
	'''

	# Bohr magneton
	mu_B = 9.2740100783e-24 # J T^-1
		
	plt.figure('Zeeman shit')
	# Subspace mf = +/- 2
	H_mf2 = 2 * mu_B * gf(2) * B / (h * 1e6) + H_hfs(2)
	H_mf_2 = - 2 * mu_B * gf(2) * B / (h * 1e6) + H_hfs(2)

	plt.plot(B, H_mf2, label='mf=2')
	plt.plot(B, H_mf_2, label='mf=-2')



	# mf = 1; F=1, F=2
	'''
	For the states mf=1 I will need to diagonalize the matrix.
	It is a 2x2 matrix with states 1,1 and 2,1
	Hamiltonian is calculated in MHz
	'''
	H_mf1_1 = np.array([])
	H_mf1_2 = np.array([]) 
	for b in B:
		mat_mf1 = np.zeros((2,2), dtype=float)
		mat_mf1[0,0] = mu_B * gf(1) * b / (h * 1e6) + H_hfs(1)
		mat_mf1[1,0] = mat_mf1[0,0]
		mat_mf1[0,1] = mu_B * gf(2) * b / (h * 1e6)
		mat_mf1[1,1] = mat_mf1[0,1] + H_hfs(2)
		eigenvalues = np.linalg.eigvals(mat_mf1)
		H_mf1_1 = np.append(H_mf1_1, eigenvalues[0])
		H_mf1_2 = np.append(H_mf1_2, eigenvalues[1])

	plt.plot(B, H_mf1_1, label='mf=1')
	plt.plot(B, H_mf1_2, label='mf=1')
	plt.legend()
	plt.show()



def main():
	B = np.linspace(0, 0.01, 100)
	H(B)


main()