#rrt.py

from random import sample
import numpy as np
from world import BoxWorld
#from misc import Timer

# Implementation of the RRT planning algorithm for a particle moving in a plane (2D world)
def rrt_planner(start, goal, world, opts):
    rg = np.random.default_rng()  # Get the default random number generator

    def sample_free():
        if rg.uniform(0, 1, 1) < opts["beta"]:
            return np.array(goal)
        else:
            found_random = False
            while not found_random:
                x = rg.uniform(0, 1, 3) * [
                    world.xmax - world.xmin,
                    world.ymax - world.ymin,
                    world.zmax - world.zmin,
                ] + [world.xmin, world.ymin, world.zmin]
                if world.obstacle_free(x[:, None]):
                    found_random = True
            return x

    def nearest(x):
        idx = np.argmin(np.sum((nodes - x[:, None]) ** 2, axis=0))
        return idx

    def steer(x1, x2):
        dx = np.linalg.norm(x2 - x1)
        if dx < opts["lambda"]:
            x_new = x2
        else:
            x_new = x1 + opts["lambda"] * (x2 - x1) / dx
        return x_new

    nodes = np.array(start.reshape((-1, 1)))  # Make numpy column vector
    parents = [0]  # Initial state has no parent

# Run planner
    for i in range(0,opts["K"]+1):
        node_sample = sample_free()
        node_idx = nearest(node_sample)
        node_nearest = nodes[:,node_idx]
        node_new = steer(node_nearest,node_sample)

        path_x = np.linspace(node_nearest[0],node_new[0],num = 50)
        path_y = np.linspace(node_nearest[1],node_new[1],num = 50)
        path_z = np.linspace(node_nearest[2],node_new[2],num = 50)
        path = np.array([path_x,path_y,path_z])

        if world.obstacle_free(path):
            nodes = np.append(nodes,node_new.reshape((-1,1)),axis=1)
            parents.append(node_idx)
            if (opts["eps"] > 0) and (np.sum((goal - node_new) ** 2, axis=0) < opts["eps"]):
                #print("Broke early")
                break

    Tplan = 1337
    goal_idx = np.argmin(np.sum((nodes - goal.reshape((-1, 1))) ** 2, axis=0))

    return goal_idx, nodes, parents, Tplan