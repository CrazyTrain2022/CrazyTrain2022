#Old
# from difflib import diff_bytes
# from importlib.resources import path
# from xml.etree.ElementTree import TreeBuilder
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# import numpy as np
# #from mpl_toolkits import mplot3d
# from mpl_toolkits.mplot3d import Axes3D


#New
from mpc_main import mpc_main
from mission_select import mission_selection
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D



goals, break_dist = mission_selection()
trajectory = mpc_main(goals=goals, break_dist=break_dist, print_goal_number=True)


#Plotting
import matplotlib.pyplot as plt
fig = plt.figure()
#ax = plt.axes(projection='3d')

ax = Axes3D(fig, auto_add_to_figure=False)
fig.add_axes(ax)


ax.plot3D(trajectory[:,0], trajectory[:,1], trajectory[:,2], 'red') #Route for drone 1
ax.plot3D(trajectory[:,6], trajectory[:,7], trajectory[:,8], 'blue') #Route for drone 2
ax.plot3D(trajectory[:,12], trajectory[:,13], trajectory[:,14], 'green') #Route for drone 3
ax.plot3D(trajectory[:,18], trajectory[:,19], trajectory[:,20], 'black') #Route for drone 4

#Starting point and Goal points
ax.scatter3D(0,0,0, cmap="Blacks")
ax.scatter3D(goals[:,0], goals[:,1], goals[:,2], cmap='Blacks')




# ANIMATION FUNCTION
def update_lines(num, dataSet1, dataSet2, dataSet3, dataSet4, line1, line2, line3, line4):
    # NOTE: there is no .set_data() for 3 dim data...
    line1.set_data(dataSet1[0:2, :num])    
    line1.set_3d_properties(dataSet1[2, :num])  
    line2.set_data(dataSet2[0:2, :num])    
    line2.set_3d_properties(dataSet2[2, :num])  
    line3.set_data(dataSet3[0:2, :num])    
    line3.set_3d_properties(dataSet3[2, :num])  
    line4.set_data(dataSet4[0:2, :num])    
    line4.set_3d_properties(dataSet4[2, :num])  

    return [line1,line2]

dataSet1 = np.array([trajectory[:,0], trajectory[:,1], trajectory[:,2]])
dataSet2 = np.array([trajectory[:,6], trajectory[:,7], trajectory[:,8]])
dataSet3 = np.array([trajectory[:,12], trajectory[:,13], trajectory[:,14]])
dataSet4 = np.array([trajectory[:,18], trajectory[:,19], trajectory[:,20]])
numDataPoints = len(trajectory)

fig = plt.figure()
ax = Axes3D(fig)
line1 = plt.plot(dataSet1[0], dataSet1[1], dataSet1[2], lw=2, c='red')[0]
line2= plt.plot(dataSet2[0], dataSet2[1], dataSet2[2], lw=2, c='blue')[0]
line3= plt.plot(dataSet3[0], dataSet3[1], dataSet3[2], lw=2, c='green')[0]
line4= plt.plot(dataSet4[0], dataSet4[1], dataSet4[2], lw=2, c='black')[0]

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_title('Trajectory of drone 1 (red), drone 2 (blue), drone 3 (green) and drone 4 (black)')
line_ani = animation.FuncAnimation(fig, update_lines, frames=numDataPoints, fargs=(dataSet1,dataSet2,dataSet3,dataSet4,line1,line2,line3,line4), interval=50, blit=False)

plt.show()

"""
fig0 =plt.figure(0)
t = np.linspace(0,len(vx_log), len(vx_log))
ax0 = plt.plot(t, vx_log, label = 'vx')
ax0 = plt.plot(t, vy_log, label = 'vy')
ax0 = plt.plot(t, vz_log, label ='vz')

v_tot = []
for i in range(0, len(vx_log)):
    #v_tot.append(np.abs(vx_log[i]) + np.abs(vy_log[i]) + np.abs(vz_log[i]))
    v_tot.append(np.sqrt(vx_log[i]**2 + vy_log[i]**2 + vz_log[i]**2))

ax0 = plt.plot(t, v_tot, label = 'v_tot')
plt.legend()
title = plt.title("Velocities")
legend = plt.legend(loc=1)

xdata = []
ydata = [] 
zdata = []
Gvx = []
Gvy = []
Gvz = []
Gvtot = []
for g in goals:
    xdata.append(g[0])
    ydata.append(g[1])
    zdata.append(g[2])
    Gvx.append(g[3])
    Gvy.append(g[4])
    Gvz.append(g[5])
    Gvtot.append(np.sqrt(g[3]**2 + g[4]**2 + g[5]**2))



def animate_func(num):
    ax1.clear()

    # Updating Trajectory Line (num+1 due to Python indexing)
    ax1.plot3D(dataSet[0, :num+1], dataSet[1, :num+1], dataSet[2, :num+1], c='black',linestyle='dotted')

    # Updating Point Location 
    ax1.scatter(dataSet[0, num], dataSet[1, num], dataSet[2, num], c='green', marker='o')

    # ax.set_xlim3d([-5, 5])
    # ax.set_ylim3d([-5, 5])
    # ax.set_zlim3d([0, 10])

    ax1.set_xlabel('Position X')
    ax1.set_ylabel('Position Y')
    ax1.set_zlabel('Position Z')
    ax1.set_title('Simulation of MPC controller on a quadcopter')

    ax1.scatter3D(goals[:][0], goals[:][1], goals[:][2], color = 'Red', marker='*')
    #ax1.scatter3D(xdata, ydata, zdata, color = 'Red', marker='*')

fig1 = plt.figure(1)
ax1 = Axes3D(fig1)

traj_x = trajectory[:][0]
traj_y = trajectory[:][1]
traj_z = trajectory[:][2]
dataSet = np.array([traj_x, traj_y, traj_z])
numDataPoints = len(traj_z)
line_ani = animation.FuncAnimation(fig1, animate_func, frames=numDataPoints, interval=10, blit=False)

plt.show()

#line_ani.save("Spiral_trajectory.mp4")

# f = r"c:///home/eriax970/TSFS12.gif" 
# writergif = animation.PillowWriter(fps=30) 
# line_ani.save(f, writer=writergif)



# f = r"c:///home/eriax970/TSFS12/animation.mp4"
# writervideo = animation.FFMpegWriter(fps=60) 
# line_ani.save(f, writer=writervideo)


mpc_trajectory = np.asarray(mpc_trajectory)
mpc_trajectory_x = mpc_trajectory[:,0,0]
mpc_trajectory_y = mpc_trajectory[:,1,0]
mpc_trajectory_z = mpc_trajectory[:,2,0]
traj_x = np.array(traj_x, dtype=object)
traj_y = np.array(traj_y, dtype=object)
traj_z = np.array(traj_z, dtype=object)

#Plotting

fig2 = plt.figure(2)
ax2 = plt.axes(projection = '3d')
ax2.plot3D(mpc_trajectory_x, mpc_trajectory_y, mpc_trajectory_z, 'blue', label = "Projected trajectory") #Projected route for each time step
ax2.plot3D(traj_x, traj_y, traj_z, 'red', label = "Real route") #Real route for drone
ax2.legend()
ax2.set_title("Prediction horizon")
#Starting point and Goal points

#ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Reds')
# print(goals[:][3])


fig3 = plt.figure(3)
ax3 = plt.plot(Gvx, label = "vx")
ax3 = plt.plot(Gvy, label = "vy")
ax3 = plt.plot(Gvz, label = "vz")
ax3 = plt.plot(Gvtot, label = "v_tot")
title = plt.title("Reference velocities")
legend = plt.legend(loc=1)

plt.show()
"""