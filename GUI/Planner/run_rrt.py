# run_rrt.py

# Import dependencies from packages
from random import sample
import numpy as np
from world import BoxWorld
import csv
import sys

# Import functions for the planner
from rrt import rrt_planner
from rrt_star import rrt_star_particle

def run_planner(drone_id):
    # Define surronding world (width, height, depth)
    VISIONEN_X_DIM = 8
    VISIONEN_Y_DIM = 8
    VISIONEN_Z_DIM = 3.0

    # Create the surronding world as an object BoxWorld
    world = BoxWorld([[-VISIONEN_X_DIM/2, VISIONEN_X_DIM/2], [-VISIONEN_Y_DIM/2, VISIONEN_Y_DIM/2], [0, VISIONEN_Z_DIM]])

    # Coordinates are closest to origo h,w,d is the box dim
    sys.path.append("/home/crazycrowd/CrazyTrain/CrazyTrain2022/crazyswarm/ros_ws/src/crazyswarm/scripts/pycrazyswarm")
    file_obs = "visualizer/obstacles.csv"
    with open(file_obs, 'r') as file:
        reader = csv.reader(file, skipinitialspace=True)
        obs = np.empty((0,6),int)
        for coord in reader:
            step = np.array([[float(coord[0]),float(coord[1]),float(coord[2]),float(coord[3]),float(coord[4]),float(coord[5])]])
            obs = np.append(obs ,step, axis = 0)
        for i in range(0,len(obs)):
            world.add_box(obs[i][0],obs[i][1],obs[i][2],obs[i][3],obs[i][4],obs[i][5])

    # Define planner options
    opts = {
        "beta": 0.05,  # Probability of selecting goal state as target state
        "lambda": 0.1,  # Step size
        "eps": 0.01,  # Threshold for stopping the search (negative for full search)
        "r_neighbor": 0.5,  # Radius of circle for definition of neighborhood
        "K": 10000,
    }  # Maximum number of iterations 

    # Read .csv file
    #with open('../GUI/points_csv/drone'+str(drone_number)+'waypoints.csv', 'r') as file:
    with open('points_csv/drone'+drone_id+'waypoints.csv', 'r') as file:
        reader = csv.reader(file, skipinitialspace=True)
        points = np.empty((0,3),int)
        for coord in reader:
            step = np.array([[float(coord[0]),float(coord[1]),float(coord[2])]])
            points = np.append(points ,step, axis = 0)
        print("File Read")

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
        #idx_goal, nodes, parents = rrt_planner(start, goal, world, opts)
        idx_goal, nodes, parents = rrt_star_particle(start, goal, world, opts)

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
    #with open('drone'+str(drone_number)+'rrttrajectory.csv','w') as file:
    print("Creating .csv file")
    with open('drone'+drone_id+'rrttrajectory.csv','w') as file:
        writer = csv.writer(file)
        for i in range(0,len(path[0])):
            row = [path[0][i],path[1][i],path[2][i]]
            writer.writerow(row)
        print(".csv file created")
