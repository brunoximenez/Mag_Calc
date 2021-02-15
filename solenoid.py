import numpy as np
import matplotlib.pyplot as plt
from magpylib.source.magnet import Box, Cylinder
from magpylib.source.current import Circular
from magpylib import Collection, displaySystem
import create_bobine as bob
import sys


'''
Some plot settings
'''
plt.rc('xtick', labelsize=14)
plt.rc('ytick', labelsize=14)

# TeX settings
plt.rcParams['text.usetex'] = True
plt.rcParams['text.latex.preamble'] = [
    r'\usepackage{amsmath}']  # for \text command


# Create coils
# Dimension is the diameter in mm
# Current in amps
radius = 35.
current = 20.
n_coils = 8
distance = 38. 

for i in range(1):
    dl = i * 2.
    coll = bob.bobine(current, 2 * radius, n_coils, distance, rotate=False)
    bob.B_array(coll, distance + dl)



# sys.exit()
# calculate B-field on a grid
ptx = 50
ptz = 50
xs = np.linspace(-300, 300, ptx)
zs = np.linspace(-300, 300, ptz)
POS = np.array([(x, 0, z) for z in zs for x in xs])

Bs = coll.getB(POS).reshape(ptz, ptx, 3)  # <--automatically vectorized

B_center = coll.getB([0, 0, 0])
# plt.show()

# sys.exit(0)
# create figure
fig = plt.figure(figsize=(9, 5))
ax1 = fig.add_subplot(121, projection='3d')  # 3D-axis
ax2 = fig.add_subplot(122)  # 2D-axis


# display system geometry on ax1
displaySystem(coll, subplotAx=ax1, suppress=True)
# display field in xz-plane using matplotlib
X, Z = np.meshgrid(xs, zs)


# Take components Bx and Bz
Bx, By, Bz = Bs[:, :, 0], Bs[:, :, 1], Bs[:, :, 2]


# ax2.streamplot(X, Z, U, V, color=np.log(U**2 + V**2))
b_map = ax2.streamplot(X, Z, Bx, Bz, color=np.sqrt(
    Bx**2 + By**2 + Bz**2), cmap='autumn')
fig.colorbar(b_map.lines)
plt.show()

bob.heat_dissipated()