# run_rrt.py

# Import dependencies from packages
from random import sample
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from world import BoxWorld
import csv
import argparse

# Import functions for the planner
from add_obs import add_obs
from rrt import rrt_planner

# Input arguments to the planner
parser = argparse.ArgumentParser()
parser.add_argument('--sim', action='store_true') #Activates simulation
parser.add_argument('--obs', action='store_true') #Includes boxes in simulation
args = parser.parse_args()

# Define surronding world (width, height, depth)
world_h = 10
world_w = 10
world_d = 5

# Create the surronding world as an object BoxWorld
world = BoxWorld([[0, world_h], [0, world_w], [0, world_d]])

# Define Obstacles (x,y,z,w,h,d)
obs1 = np.array([4,6,0,2,2,1])
obs2 = np.array([4,2,0,2,2,1])

# Coordinates are closest to origo h,w,d is the box dim
world.add_box(obs1[0], obs1[1], obs1[2], obs1[3], obs1[4], obs1[5])
world.add_box(obs2[0], obs2[1], obs2[2], obs2[3], obs2[4], obs2[5])

# Define planner options
opts = {
    "beta": 0.05,  # Probability of selecting goal state as target state in the sample
    "lambda": 0.1,  # Step size
    "eps": 0.01,  # Threshold for stopping the search (negative for full search)
    "K": 5000, # Maximum number of iterations, if eps < 0
}  

# Read .csv file
with open('indata.csv', 'r') as file:
    reader = csv.reader(file, skipinitialspace=True)
    points = np.empty((0,3),int)
    for coord in reader:
        step = np.array([[float(coord[0]),float(coord[1]),float(coord[2])]])
        points = np.append(points ,step, axis = 0)

# Run the planner
path = np.vstack(points[0])

for i in range(0, len(points) - 1):
    # Define start and goal
    start = points[i] 
    goal = points[i+1]

    # Adjusting starting point (if threshold active)
    if opts["eps"] > 0 and i > 0:
        start = np.array([path[0][-1],path[1][-1],path[2][-1]])

    # Run planner
    idx_goal, nodes, parents, Tplan = rrt_planner(start, goal, world, opts)

    # Extract finalized path
    idx = idx_goal
    path_section = np.vstack(nodes[:, idx])
    while idx != 0:
        ll = np.column_stack((nodes[:, parents[idx]], nodes[:, idx]))
        path_parent = np.vstack(nodes[:, parents[idx]])
        path_section = np.concatenate((path_section, path_parent), axis = 1)
        idx = parents[idx]
    path_section = np.flip(path_section,axis=1)
    path = np.concatenate((path,path_section[:,1:]), axis=1)

# Creating a .csv file with complete path
with open('utdata.csv','w') as file:
    writer = csv.writer(file)
    for i in range(0,len(path[0])):
        row = [path[0][i],path[1][i],path[2][i]]
        writer.writerow(row)

# Simulation of obstacles and the calculated path (if --sim has been called)
if args.sim:
    # Plot world
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.axes.set_xlim(0,world_w)
    ax.axes.set_ylim(0,world_h)
    ax.axes.set_zlim(0,world_d)

    # Plot Obstacle (if --obs has been called)
    if args.obs:
        ax.voxels(add_obs(obs1[0], obs1[1], obs1[2], obs1[3], obs1[4], obs1[5]), facecolors='red', zorder = 0)
        ax.voxels(add_obs(obs2[0], obs2[1], obs2[2], obs2[3], obs2[4], obs2[5]), facecolors='blue', zorder = 1)

    # Plot path
    ax.plot(path[0], path[1], path[2], color='black', linestyle ='dotted', zorder = 10)

    # Show plot
    plt.show()
