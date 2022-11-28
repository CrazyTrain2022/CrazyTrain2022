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