import numpy as np
import matplotlib.pyplot as plt
from magpylib.source.magnet import Box, Cylinder
from magpylib.source.current import Circular
from magpylib import Collection, displaySystem

# Create coils
# Dimension is the diameter in mm
# Current in amps
diameter = 8.
current = 20.
coil1 = Circular(curr=current, dim=diameter, pos=(0, 0, - diameter / 2))
coil2 = Circular(curr=current, dim=diameter, pos=(0, 0, - diameter / 2 + 0.3))
coil3 = Circular(curr=current, dim=diameter, pos=(0, 0, - diameter / 2 + 0.6))
coil4 = Circular(curr=current, dim=diameter, pos=(0, 0, - diameter / 2 + 0.9))


coil5 = Circular(curr=current, dim=diameter, pos=(0, 0, diameter / 2))
coil6 = Circular(curr=current, dim=diameter, pos=(0, 0, diameter / 2 + 0.3))
coil7 = Circular(curr=current, dim=diameter, pos=(0, 0, diameter / 2 + 0.6))
coil8 = Circular(curr=current, dim=diameter, pos=(0, 0, diameter / 2 + 0.9))

# create magnets
# s1 = Box(mag=(0, 0, 600), dim=(3, 3, 3), pos=(-4, 0, 3))
# s2 = Cylinder(mag=(0, 0, 500), dim=(3, 5))
# create collection
c = Collection(coil4, coil3, coil2, coil1, coil5, coil6, coil7, coil8)
# manipulate magnets individually

# s1.rotate(45, (0, 1, 0), anchor=(0, 0, 0))
# s2.move((5, 0, -4))

# manipulate collection
# c.move((-2, 0, 0))

# calculate B-field on a grid
ptx = 33
ptz = 44
xs = np.linspace(-10, 10, ptx)
zs = np.linspace(-10, 10, ptz)
POS = np.array([(x, 0, z) for z in zs for x in xs])

Bs = c.getB(POS).reshape(ptz, ptx, 3)  # <--automatically vectorized

B_center = c.getB([4,0,0])
print(B_center) 

# create figure
fig = plt.figure(figsize=(9, 5))
ax1 = fig.add_subplot(121, projection='3d')  # 3D-axis
ax2 = fig.add_subplot(122)  # 2D-axis

# display system geometry on ax1
displaySystem(c, subplotAx=ax1, suppress=True)
# display field in xz-plane using matplotlib
X, Z = np.meshgrid(xs, zs)

# Take components Bx and Bz 
Bx, By, Bz = Bs[:, :, 0], Bs[:, :, 1], Bs[:, :, 2]



# ax2.streamplot(X, Z, U, V, color=np.log(U**2 + V**2))
b_map = ax2.streamplot(X, Z, Bx, Bz, color=np.sqrt(Bx**2 + By**2 + Bz**2), cmap='autumn')
fig.colorbar(b_map.lines)
plt.show()
