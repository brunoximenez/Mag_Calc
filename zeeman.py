import numpy as np 
import matplotlib.pyplot as plt
from sympy.physics.quantum.cg import CG
import sys


h = 6.62606976e-34  # J*s
gi = - 0.0009951414 # Phys. Rev. 174, 23 https://doi.org/10.1103/PhysRev.174.23
# Bohr magneton
mu_B = 9.2740100783e-24 # J T^-1

fontsize = 14

def g_j(J=1/2, L=0, S=1/2):
	gj = J*(J+1) - L*(L+1) + S*(S+1)
	gj = gj / (2 * J * (J + 1))
	gj += 1

	return gj


def gf(F, J=.5, I=3/2, L=0, S=.5):

	gj = g_j()
	g_f = gj * ( F * ( F + 1) + J * (J + 1) - I * (I + 1) )
	g_f = g_f / (2 * F * (F + 1))

	return g_f


def K(F, I=3/2, J=.5):
	k = .5 * (F*(F+1) - I*(I+1) - J*(J+1))
	return k


def H_hfs(F):
	a = 3.417341e3 # MHz
	x = a * K(F)
	return x


def hz(mj, mi):

	return g_j() * mj + gi*mi


def H_2x2_mf_minus1(H_mat_hfs, B):
	''''
	In the 2x2 subspace of mf=1, we have for j=1/2 and I=3/2:
	(in the basis mj, mi):
	| (-1/2, 3/2), (1/2, 1/2)>
	And linear combinations of the states above leads to:
	(in F,mf basis):
	(2,-1) and (1,-1)
	Expressing those in F mf in terms of mj mi:
	(2,-1) = a_(21) (-1/2, -1/2) + b_(21) (1/2, -3/2)
	(1,-1) = a_(11) (-1/2, -1/2) + b_(11) (1/2, -3/2)
	I will define state vector and represent as a vector in this basis
	'''
	a_21 = np.sqrt(3)/2
	b_21 = 1/2
	a_11 = - b_21
	b_11 = a_21
	# state vector:
	psi_21 = np.array([a_21, b_21])
	psi_11 = np.array([a_11, b_11])

	Hz_psi_21 = np.zeros(2)
	# print('psi_21', psi_21)

	Hz_psi_21[0] = psi_21[0] * hz(-1/2, -1/2)
	Hz_psi_21[1] = psi_21[1] * hz(1/2, -3/2)

	# print('Hz_psi_21', Hz_psi_21)

	psi_21_Hz_psi_21 = np.dot(psi_21, Hz_psi_21)
	psi_11_Hz_psi_21 = np.dot(psi_11, Hz_psi_21)

	Hz_psi_11 = np.zeros(2)
	Hz_psi_11[0] = psi_11[0] * hz(-1/2, -1/2)
	Hz_psi_11[1] = psi_11[1] * hz(1/2, -3/2)

	psi_11_Hz_psi_11 = np.dot(psi_11, Hz_psi_11)
	Hz_mat_mf1 = np.zeros((2,2), dtype=float)

	Hz_mat_mf1[0,0] = psi_11_Hz_psi_11
	Hz_mat_mf1[0,1] = psi_11_Hz_psi_21
	Hz_mat_mf1[1,0] = Hz_mat_mf1[0,1]
	Hz_mat_mf1[1,1] = psi_21_Hz_psi_21

	H_mf1_1 = np.array([])
	H_mf1_2 = np.array([])
	for b in B:
		print(Hz_mat_mf1)
		Hz = Hz_mat_mf1 * mu_B * b / (h * 1e6)
		
		# mat_mf1 = np.zeros((2,2), dtype=float)

		mat_mf1 = Hz + H_mat_hfs
		# mat_mf1[0,0] = Hz_mat_mf1[0,0] + H_hfs(1)
		# mat_mf1[1,0] = mat_mf1[0,0]
		# mat_mf1[0,1] = Hz_mat_mf1[0,1]
		# mat_mf1[1,1] = Hz_mat_mf1[1,1] + H_hfs(2)
		eigenvalues = np.linalg.eigvals(mat_mf1)
		H_mf1_1 = np.append(H_mf1_1, eigenvalues[0])
		H_mf1_2 = np.append(H_mf1_2, eigenvalues[1])

	plt.plot(B, H_mf1_1, label=r'$m_{f}=-1$')
	plt.plot(B, H_mf1_2, label=r'$m_{f}=-1$')
	# plt.ylim((-25000, 25000))
	# plt.xlim((0, 1.5))
	plt.legend()
	# plt.show()


def H_2x2_mf1(H_mat_hfs, B):
	''''
	In the 2x2 subspace of mf=1, we have for j=1/2 and I=3/2:
	(in the basis mj, mi):
	| (-1/2, 3/2), (1/2, 1/2)>
	And linear combinations of the states above leads to:
	(in F,mf basis):
	(2,1) and (1,1)
	Expressing those in F mf in terms of mj mi:
	(2,1) = a_(21) (-1/2, 3/2) + b_(21) (1/2, 1/2)
	(1,1) = a_(11) (-1/2, 3/2) + b_(11) (1/2, 1/2)
	I will define state vector and represent as a vector in this basis
	'''
	a_21 = 1/2
	b_21 = np.sqrt(3)/2
	a_11 = - b_21
	b_11 = 1/2
	# state vector:
	psi_21 = np.array([a_21, b_21])
	psi_11 = np.array([a_11, b_11])

	Hz_psi_21 = np.zeros(2)
	# print('psi_21', psi_21)

	Hz_psi_21[0] = psi_21[0] * hz(-1/2, 3/2)
	Hz_psi_21[1] = psi_21[1] * hz(1/2, 1/2)

	# print('Hz_psi_21', Hz_psi_21)

	psi_21_Hz_psi_21 = np.dot(psi_21, Hz_psi_21)
	psi_11_Hz_psi_21 = np.dot(psi_11, Hz_psi_21)

	Hz_psi_11 = np.zeros(2)
	Hz_psi_11[0] = psi_11[0] * hz(-1/2, 3/2)
	Hz_psi_11[1] = psi_11[1] * hz(1/2, 1/2)

	psi_11_Hz_psi_11 = np.dot(psi_11, Hz_psi_11)
	Hz_mat_mf1 = np.zeros((2,2), dtype=float)

	Hz_mat_mf1[0,0] = psi_11_Hz_psi_11
	Hz_mat_mf1[0,1] = psi_11_Hz_psi_21
	Hz_mat_mf1[1,0] = Hz_mat_mf1[0,1]
	Hz_mat_mf1[1,1] = psi_21_Hz_psi_21

	H_mf1_1 = np.array([])
	H_mf1_2 = np.array([])
	for b in B:
		print(Hz_mat_mf1)
		Hz = Hz_mat_mf1 * mu_B * b / (h * 1e6)
		
		# mat_mf1 = np.zeros((2,2), dtype=float)

		mat_mf1 = Hz + H_mat_hfs
		# mat_mf1[0,0] = Hz_mat_mf1[0,0] + H_hfs(1)
		# mat_mf1[1,0] = mat_mf1[0,0]
		# mat_mf1[0,1] = Hz_mat_mf1[0,1]
		# mat_mf1[1,1] = Hz_mat_mf1[1,1] + H_hfs(2)
		eigenvalues = np.linalg.eigvals(mat_mf1)
		H_mf1_1 = np.append(H_mf1_1, eigenvalues[0])
		H_mf1_2 = np.append(H_mf1_2, eigenvalues[1])

	plt.plot(B, H_mf1_1, label=r'$m_{f}=1$')
	plt.plot(B, H_mf1_2, label=r'$m_{f}=1$')
	# plt.ylim((-25000, 25000))
	# plt.xlim((0, 1.5))
	plt.legend()
	# plt.show()


def H_2x2_mf_0(H_mat_hfs, B):
	''''
	In the 2x2 subspace of mf=-1, we have for j=1/2 and I=3/2:
	(in the basis mj, mi):
	| (1/2, -1/2), (-1/2, 1/2)>
	And linear combinations of the states above leads to:
	(in F,mf basis):
	(2,0) and (1,0)
	Expressing those in F mf in terms of mj mi:
	(2,0) = a_(21) (1/2, -1/2) + b_(21) (-1/2, 1/2)
	(1,0) = a_(11) (1/2, -1/2) + b_(11) (-1/2, 1/2)
	I will define state vector and represent as a vector in this basis
	'''
	a_21 = 1 / np.sqrt(2)
	b_21 = 1 / np.sqrt(2)
	a_11 = - b_21
	b_11 = a_21
	# state vector:
	psi_21 = np.array([a_21, b_21])
	psi_11 = np.array([a_11, b_11])

	Hz_psi_21 = np.zeros(2)
	# print('psi_21', psi_21)

	Hz_psi_21[0] = psi_21[0] * hz(1/2, -1/2)
	Hz_psi_21[1] = psi_21[1] * hz(-1/2, 1/2)

	# print('Hz_psi_21', Hz_psi_21)

	psi_21_Hz_psi_21 = np.dot(psi_21, Hz_psi_21)
	psi_11_Hz_psi_21 = np.dot(psi_11, Hz_psi_21)

	Hz_psi_11 = np.zeros(2)
	Hz_psi_11[0] = psi_11[0] * hz(1/2, -1/2)
	Hz_psi_11[1] = psi_11[1] * hz(-1/2, 1/2)

	psi_11_Hz_psi_11 = np.dot(psi_11, Hz_psi_11)
	Hz_mat_mf1 = np.zeros((2,2), dtype=float)

	Hz_mat_mf1[0,0] = psi_11_Hz_psi_11
	Hz_mat_mf1[0,1] = psi_11_Hz_psi_21
	Hz_mat_mf1[1,0] = Hz_mat_mf1[0,1]
	Hz_mat_mf1[1,1] = psi_21_Hz_psi_21

	H_mf1_1 = np.array([])
	H_mf1_2 = np.array([])
	for b in B:
		Hz = Hz_mat_mf1 * mu_B * b / (h * 1e6)
		
		# mat_mf1 = np.zeros((2,2), dtype=float)
		mat_mf_1 = Hz + H_mat_hfs
		eigenvalues = np.linalg.eigvals(mat_mf_1)
		H_mf1_1 = np.append(H_mf1_1, eigenvalues[0])
		H_mf1_2 = np.append(H_mf1_2, eigenvalues[1])

	plt.plot(B, H_mf1_1, label=r'$m_{f}=0$')
	plt.plot(B, H_mf1_2, label=r'$m_{f}=0$')
	# plt.ylim((-25000, 25000))
	# plt.xlim((0, 1.5))
	plt.legend()
	# plt.show()


def H(B):
	'''
	Calculates the Zeeman Hamiltonian of the system
	given a B field in T
	'''
		
	H_mat_hfs = np.zeros((2,2), dtype=float)
	H_mat_hfs[0,0] = H_hfs(1)
	H_mat_hfs[1,1] = H_hfs(2)

	plt.figure('Zeeman shift')


	# Subspace mf = +/- 2
	mf = 2
	H_mf2 = mf * mu_B * gf(2) * B / (h * 1e6) + H_mat_hfs[1,1]
	mf = - 2
	H_mf_2 = mf * mu_B * gf(2) * B / (h * 1e6) + H_mat_hfs[1,1]

	# subspace +/-1:
	# mj = 1
	# H_mf1 = mj * mu_B * gf(2) * B / (h * 1e6) + H_mat_hfs[1,1]
	# # mj = - 1
	# # H_mf_2 = mj * mu_B * gf(2) * B / (h * 1e6) + H_mat_hfs[1,1]
	# plt.plot(B, H_mf1, 'o')


	plt.plot(B, H_mf2, label=r'$m_{f}=2$')
	plt.plot(B, H_mf_2, label=r'$m_{f}=-2$')


	# mf = 1; F=1, F=2
	'''
	For the states mf=1 I will need to diagonalize the matrix.
	It is a 2x2 matrix with states 1,1 and 2,1
	Hamiltonian is calculated in MHz
	'''
	H_2x2_mf1(H_mat_hfs, B)
	H_2x2_mf_minus1(H_mat_hfs, B)
	H_2x2_mf_0(H_mat_hfs, B)

	plt.xlim((np.amin(B), np.amax(B)))
	plt.xlabel('B (T)', fontsize=fontsize)
	plt.ylabel(r'$\mathcal{E}$ / h (MHz)', fontsize=fontsize)
	plt.title(r'5S$_{1/2}$', fontsize=fontsize)
	plt.show()


def main():
	B = np.linspace(0., .1 , 100)
	x = mu_B * gf(1) * 1e-3 / h
	print(x / 1e6)
	# sys.exit(0)
	H(B)


main()