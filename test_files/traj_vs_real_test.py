from tokenize import Pointfloat
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from matplotlib.animation import FuncAnimation
import uav_trajectory
import warnings

max_deviation = 0.1 #meters

# ------------

fig = plt.figure()
ax = plt.subplot(projection='3d')

traj = uav_trajectory.Trajectory()
traj.loadcsv("drone1trajectory_test23.csv")

ts = np.arange(0, traj.duration, 0.01)
evals = np.empty((len(ts), 15))
for t, i in zip(ts, range(0, len(ts))):
    e = traj.eval(t)
    evals[i, 0:3]  = e.pos
    evals[i, 3:6]  = e.vel
    evals[i, 6:9]  = e.acc
    evals[i, 9:12] = e.omega
    evals[i, 12]   = e.yaw
    evals[i, 13]   = e.roll
    evals[i, 14]   = e.pitch

x_traj = evals[:,0]
y_traj = evals[:,1]
z_traj = evals[:,2]

trajectory_points = np.transpose(np.array([x_traj, y_traj, z_traj]))

#----------------

real_coords = np.genfromtxt('test23.csv', delimiter=',')

x_real = real_coords[:,0]
y_real = real_coords[:,1]
z_real = real_coords[:,2]



# x_real = [1,1,1,0] #change these to something from visionen
# y_real = [2,1,2,0]
# z_real = [0,1,2,0.09]

real_points = np.transpose(np.array([x_real, y_real, z_real]))
#----------------

dist_list = []
for point in real_points:
    temp_list = []
    for p in trajectory_points:
        temp_list.append(np.linalg.norm(p-point))
    dist_list.append(min(temp_list))

for dist in dist_list:
    if abs(dist) > max_deviation:
        print("Test failed")
    else:
        print("Test passed")


ax.plot(x_traj, y_traj, z_traj)
ax.scatter(x_real, y_real, z_real, c='#ff7f0e')

plt.show()