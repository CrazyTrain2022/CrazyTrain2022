from tokenize import Pointfloat
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

plot = False

print("Adding Circle")

waypoints = np.genfromtxt("waypoints.csv", delimiter=',')
last_pos = waypoints[-1,:]

n = 4
for t in range(n+1):
    x = (1.5*np.cos(2*np.pi*t/n))
    y = (1.5*np.sin(2*np.pi*t/n))
    z = (last_pos[2])
    waypoints = np.append(waypoints,np.array([[x,y,z]]),axis=0)

np.savetxt('waypoints.csv', X=waypoints, delimiter=',', fmt='%10.2f')
