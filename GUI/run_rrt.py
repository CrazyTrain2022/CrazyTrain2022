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

    # Constraint the world around set-points and obstacles
    CALC_X_MAX = 0
    CALC_X_MIN = 0
    CALC_Y_MAX = 0
    CALC_Y_MIN = 0
    CALC_Z_MAX = 0
    CALC_Z_MIN = 0 # Always 0

    # Read drone?waypoints.csv file
    #with open('../GUI/points_csv/drone'+str(drone_number)+'waypoints.csv', 'r') as file:
    with open('GUI/points_csv/drone'+drone_id+'waypoints.csv', 'r') as file:
        reader = csv.reader(file, skipinitialspace=True)
        points = np.empty((0,3),int)
        for coord in reader:
            step = np.array([[float(coord[0]),float(coord[1]),float(coord[2])]])
            points = np.append(points ,step, axis = 0)
            # Constraining the world coordinates
            if step[0] <= CALC_X_MIN:
                CALC_X_MIN = step[0] - 1
            if step[1] <= CALC_Y_MIN:
                CALC_Y_MIN = step[1] - 1
            if step[1] >= CALC_X_MAX:
                CALC_X_MAX = step[0] + 1
            if step[1] >= CALC_Y_MAX:
                CALC_Y_MAX = step[1] + 1
            if step[2] >= CALC_Z_MAX:
                CALC_Z_MAX = step[5] + 1
        print("Waypoints csv-file read!")

    # Read obstacles.csv file
    #sys.path.append("/home/crazycrowd/CrazyTrain/CrazyTrain2022/crazyswarm/ros_ws/src/crazyswarm/scripts/pycrazyswarm")
    file_obs = "crazyswarm/ros_ws/src/crazyswarm/scripts/pycrazyswarm/visualizer/obstacles.csv"
    with open(file_obs, 'r') as file:
        reader = csv.reader(file, skipinitialspace=True)
        obs = np.empty((0,6),int)
        for coord in reader:
            step = np.array([[float(coord[0]),float(coord[1]),float(coord[2]),float(coord[3]),float(coord[4]),float(coord[5])]])
            obs = np.append(obs ,step, axis = 0)
            # Constraining the world coordinates
            if step[0] <= CALC_X_MIN:
                CALC_X_MIN = step[0] - 1
            if step[1] <= CALC_Y_MIN:
                CALC_Y_MIN = step[1] - 1
            if step[3] >= CALC_X_MAX:
                CALC_X_MAX = step[0] + 1
            if step[4] >= CALC_Y_MAX:
                CALC_Y_MAX = step[1] + 1
            if step[5] >= CALC_Z_MAX:
                CALC_Z_MAX = step[5] + 1
        print("Obstacles csv-file read!")

    # Create the surronding world as an object BoxWorld and add obstacles
    #world = BoxWorld([[-VISIONEN_X_DIM/2, VISIONEN_X_DIM/2], [-VISIONEN_Y_DIM/2, VISIONEN_Y_DIM/2], [0, VISIONEN_Z_DIM]])
    world = BoxWorld([[CALC_X_MIN, CALC_X_MAX], [CALC_Y_MIN, CALC_Y_MAX], [CALC_Z_MIN, CALC_Z_MAX]])
    for i in range(0,len(obs)):
        world.add_box(obs[i][0],obs[i][1],obs[i][2],obs[i][3],obs[i][4],obs[i][5])
    
    print("World x-min: ",CALC_X_MIN)
    print("World y-min: ",CALC_Y_MIN)
    print("World z-min: ",CALC_Z_MIN)
    print("World x-max: ",CALC_X_MAX)
    print("World y-max: ",CALC_Y_MAX)
    print("World z-max: ",CALC_Z_MAX)

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
    with open('GUI/Planner/drone'+drone_id+'rrttrajectory.csv','w') as file:
        writer = csv.writer(file)
        for i in range(0,len(path[0])):
            row = [path[0][i],path[1][i],path[2][i]]
            writer.writerow(row)
        print(".csv file created")
