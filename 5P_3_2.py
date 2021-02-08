import numpy as np
import matplotlib.pyplot as plt
import sys


h = 6.62606976e-34  # J*s
gi = - 0.0009951414  # Phys. Rev. 174, 23 https://doi.org/10.1103/PhysRev.174.23
# Bohr magneton
mu_B = 9.2740100783e-24  # J T^-1

I = 3 / 2
J = 3 / 2

fontsize = 14


def K(F, I=3 / 2, J=3 / 2):
    k = F * (F + 1) - I * (I + 1) - J * (J + 1)
    return k


def h_hfs(F):
    a = 84.7185  # MHz
    b = 12.4965  # MHz
    temp = 3 * K(F) * (K(F) + 1) / 2
    temp += - 2 * I*(I + 1) * J * (J + 1)
    temp /= 4 * I * (2 * I - 1) * (2 * J - 1)

    x = .5 * a * K(F) + b * temp
    return x

# for x in range(4):
#     print(h_hfs(x))

print(h_hfs(1) - h_hfs(0))
print(h_hfs(2) - h_hfs(1))
print(h_hfs(3) - h_hfs(2))


