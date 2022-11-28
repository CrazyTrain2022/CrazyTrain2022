from tokenize import Pointfloat
import numpy as np
import matplotlib.pyplot as plt         #COMMENT: NOT USED 
from mpl_toolkits import mplot3d        #COMMENT: NOT USED
import sys

#COMMENT: NEEDS SOME COMMENT

def main(drone_traj, pos):
    waypoints = np.genfromtxt(drone_traj, delimiter=',')

    waypoints = np.append(waypoints,pos,axis=0)

    np.savetxt(drone_traj, X=waypoints, delimiter=',', fmt='%10.2f')

if __name__ == '__main__':
    args = sys.argv[1:]
    drone_traj = "waypoints.csv"
    x = args[0]
    y = args[1]
    z = args[2]

    pos = np.array([[int(x),int(y),int(z)]])

    main(drone_traj, pos)
