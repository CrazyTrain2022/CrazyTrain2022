import numpy as np

print("Resetting waypoints")

waypoints = np.array([[]])
np.savetxt("waypoints.csv", X=waypoints, delimiter=',', fmt='%10.2f')
