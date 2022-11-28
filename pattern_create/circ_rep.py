from tokenize import Pointfloat
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

#COMMENT: THIS FILE NEEDS SOME COMMENT.

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.set_xlim3d(-5, 5)
ax.set_ylim3d(-5, 5)
ax.set_zlim3d(0, 5)

original_waypoints = np.genfromtxt('waypoints.csv', delimiter=',')

nbr_of_drones = 2
theta = 2*np.pi / nbr_of_drones

shape = np.shape(original_waypoints)
x_shape = shape[0]
y_shape = shape[1]

waypoints_array = np.zeros([x_shape,y_shape,nbr_of_drones])

for drone in range(nbr_of_drones):
    temp_waypoints = np.zeros(np.shape(original_waypoints))

    for i in range(len(original_waypoints)):
        temp_waypoints[i][0] = original_waypoints[i][0]*np.cos(drone*theta) - original_waypoints[i][1]*np.sin(drone*theta)
        temp_waypoints[i][1] = original_waypoints[i][1]*np.cos(drone*theta) + original_waypoints[i][0]*np.sin(drone*theta)
        temp_waypoints[i][2] = original_waypoints[i][2]

    waypoints_array[:,:,drone] = temp_waypoints

    ax.plot(waypoints_array[:,0,drone], waypoints_array[:,1,drone], waypoints_array[:,2,drone])
    np.savetxt('drone'+str(drone+1)+'waypoints.csv', X=waypoints_array[:,:,drone], delimiter=',', fmt='%10.2f')

plt.show()