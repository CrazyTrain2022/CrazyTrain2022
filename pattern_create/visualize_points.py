from tokenize import Pointfloat
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

print("Visualizing points")

ax = plt.subplot(projection='3d')

waypoints = np.genfromtxt("waypoints.csv", delimiter=',')

x = waypoints[:,0]
y = waypoints[:,1]
z = waypoints[:,2]

ax.set_xlim3d(-3, 3)
ax.set_ylim3d(-3, 3)
ax.set_zlim3d(0, 3)

ax.plot(x, y, z)

plt.show()