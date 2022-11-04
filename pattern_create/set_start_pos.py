from tokenize import Pointfloat
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import sys

def main(drone_traj, pos):
    print("Setting starting position", pos[0])

    waypoints = np.array([[0,0,0]])
    waypoints = np.append(waypoints, pos, axis=0)

    np.savetxt(drone_traj, X=waypoints, delimiter=',', fmt='%10.2f')

if __name__ == '__main__':
    args = sys.argv[1:]
    drone_traj = "waypoints.csv"
    x = args[0]
    y = args[1]
    z = args[2]

    pos = np.array([[int(x),int(y),int(z)]])

    main(drone_traj, pos)
