#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 10:04:05 2022

@author: patli821
"""

# %% Imports
from random import sample
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d
from add_obs import add_obs
#from misc import Timer
from world import BoxWorld


# %% Define World
world = BoxWorld([[0, 10], [0, 10], [0, 10]])

# Define start and goal state
start = np.array([5, 0, 5]) # Start state
#goal = np.array([5, 9, 5]) # Goal state
goal = np.array([5, 5, 5]) # Goal state

# Adding Obstacles
x1 = 4
y1 = 6
z1 = 4
w1 = 2
h1 = 2
d1 = 2

x2 = 4
y2 = 2
z2 = 4
w2 = 2
h2 = 2
d2 = 2

# Coordinates are closest to origo h,w,d is the box dim
world.add_box(x1, y1, z1, w1, h1, d1)
world.add_box(x2, y2, z2, w2, h2, d2)

# %% Implementation of RRT*

# Implementation of the RRT planning algorithm for a particle moving in a plane (2D world)
def rrt_star_particle(start, goal, world, opts):
    rg = np.random.default_rng()  # Get the default random number generator

    def sample_free():
        if rg.uniform(0, 1, 1) < opts["beta"]:
            #return goal
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
    
    def near(x, r):
    #"""Find the indices of the states in nodes within a neighborhood with
    #radius r from state x"""
        idx = np.where(np.sum((nodes - x[:, None]) ** 2, axis=0) < r**2)
        return idx[0]

    def steer(x1, x2):
        dx = np.linalg.norm(x2 - x1)
        if dx < opts["lambda"]:
            x_new = x2
        else:
            x_new = x1 + opts["lambda"] * (x2 - x1) / dx
        return x_new
    
    def connect_min_cost(x_new, near_idx, idx_nearest, cost_via_nearest):
    #"""Function for connecting along a path from tree root to x_new with
    #minimum cost among the states in a neighborhood of x_new
    #described by the (column) indices near_idx in nodes. The variable
    #idx_nearest is the index (column in matrix nodes) for the node
    #closest to x_new and cost_via_nearest is the cost to reach x_new
    #via the nearest node."""

        idx_min = idx_nearest
        #cost_min = min(cost_via_nearest)
        cost_min = cost_via_nearest

        for idx_n in near_idx:
            x_near = nodes[:, idx_n]

            if (x_new[0] == x_near[0]) and (x_new[1] == x_near[1]) and (x_new[2] == x_near[2]):
                p = x_new[:, None]
            else:
                    p = np.row_stack(
                (
                    np.arange(x_near[0], x_new[0], (x_new[0] - x_near[0]) / 10),
                    np.arange(x_near[1], x_new[1], (x_new[1] - x_near[1]) / 10),
                    np.arange(x_near[2], x_new[2], (x_new[2] - x_near[2]) / 10),
                )
            )
            cost_near = cost[idx_n] + np.linalg.norm(x_near - x_new)

            if cost_near < cost_min and world.obstacle_free(p):
                cost_min = cost_near
                idx_min = idx_n
        return idx_min, cost_min

    def rewire_neighborhood(x_new, near_idx, cost_min):
        """Function for (possible) rewiring of the nodes in the neighborhood of
        x_new described by the indices near_idx in nodes (column numbers)
        via the new state x_new, if a path with less cost could be found.
        The variable cost_min is the cost-to-come to x_new
        (computed in connect_min_cost)"""
        for idx_n in near_idx:
            x_near = nodes[:, idx_n]

            if (x_new[0] == x_near[0]) and (x_new[1] == x_near[1]) and (x_new[2] == x_near[2]):
                p = node_new[:, None]
                            #if (node_new[0] == node_near[0]) and (node_new[1] == node_near[1]) and (node_new[2] == node_near[2]):
                #p = node_new[:, None]
            else:
                p = np.row_stack(
                    (
                        #np.arange(node_near[0], node_new[0], (node_new[0] - node_near[0]) / 10),
                        #np.arange(node_near[1], node_new[1], (node_new[1] - node_near[1]) / 10),
                        #np.arange(node_near[2], node_new[2], (node_new[2] - node_near[2]) / 10),
                                                
                        np.arange(x_near[0], x_new[0], (x_new[0] - x_near[0]) / 10),
                        np.arange(x_near[1], x_new[1], (x_new[1] - x_near[1]) / 10),
                        np.arange(x_near[2], x_new[2], (x_new[2] - x_near[2]) / 10),
                    )
                )
            cost_near = cost_min + np.linalg.norm(x_near - x_new)
            if cost_near < cost[idx_n] and world.obstacle_free(p):
                parents[idx_n] = len(parents) - 1
                cost[idx_n] = cost_near


    nodes = np.array(start.reshape((-1, 1)))  # Make numpy column vector
    parents = [0]  # Initial state has no parent
    #cost = [0]
    cost = np.array([0])
    # nodes = start.reshape((-1, 1))
    # parents = np.array([0], dtype=int)

    for i in range(0,opts["K"]+1):
        node_sample = sample_free()
        node_idx = nearest(node_sample)
        node_nearest = nodes[:,node_idx]
        node_new = steer(node_nearest,node_sample)
        
        #Changes between RRT_star and RRT here
        cost_via_nearest = cost[node_idx] + np.linalg.norm(node_new-node_nearest)
        node_neigh_idx = near(node_new,opts["r_neighbor"])

        idx_min, cost_min = connect_min_cost(node_new, node_neigh_idx, node_idx, cost_via_nearest)

        path_x = np.linspace(node_nearest[0],node_new[0],num = 50)
        path_y = np.linspace(node_nearest[1],node_new[1],num = 50)
        path_z = np.linspace(node_nearest[2],node_new[2],num = 50)
        path = np.array([path_x,path_y,path_z])
            
        if idx_min == node_idx:
        
            if world.obstacle_free(path):
                cost = np.append(cost, cost_min.reshape((-1,1)),axis=None)
                #cost = cost + cost_min
                nodes = np.append(nodes, node_new.reshape((-1,1)),axis=1)
                parents.append(node_idx)
                rewire_neighborhood(node_new, node_neigh_idx, cost_min)
                
                if (opts["eps"] > 0) and (np.sum((goal - node_new) ** 2, axis=0) < opts["eps"]):
                    #print("Broke early")
                    break
        else: 
            #cost = np.append(cost, cost_min.reshape((-1,1)),axis=1)
            cost = np.append(cost, cost_min.reshape((-1, 1)), axis=None)
            nodes = np.append(nodes, node_new.reshape((-1,1)),axis=1)
            parents.append(idx_min)
            rewire_neighborhood(node_new, node_neigh_idx, cost_min)
            if (opts["eps"] > 0) and (np.sum((goal - node_new) ** 2, axis=0) < opts["eps"]):
                # print("Broke early")
                break


    Tplan = 1337
    goal_idx = np.argmin(np.sum((nodes - goal.reshape((-1, 1))) ** 2, axis=0))

    return goal_idx, nodes, parents, Tplan

# %% # Run the planner

opts = {
    "beta": 0.05,  # Probability of selecting goal state as target state
    "lambda": 0.1,  # Step size
    "eps": -0.01,  # Threshold for stopping the search (negative for full search)
    "r_neighbor": 0.5,  # Radius of circle for definition of neighborhood
    "K": 10000,
}  # Maximum number of iterations

idx_goal, nodes, parents, Tplan = rrt_star_particle(start, goal, world, opts)

print(idx_goal)
print(nodes)

# %% Plots and Analysis

# Define figure
fig = plt.figure()
#ax = Axes3D(fig)
#ax = mpl_toolkits.mplot3d.Axes3D(fig)
ax = fig.add_subplot(projection='3d')

# Plot Obstacle
ax.voxels(add_obs(x1,y1,z1,w1,h1,d1), facecolors='red', zorder = 0)
ax.voxels(add_obs(x2,y2,z2,w2,h2,d2), facecolors='blue', zorder = 1)

#Plot tree
idx = len(parents) - 1
while idx != 0:
    ll = np.column_stack((nodes[:, parents[idx]], nodes[:, idx]))
    ax.plot(ll[0], ll[1], ll[2], color='gray', lw = 2)
    idx = idx - 1

#Plot path
idx = idx_goal
while idx != 0:
    ll = np.column_stack((nodes[:, parents[idx]], nodes[:, idx]))
    ax.plot(ll[0], ll[1], ll[2], color='green', lw = 2, zorder = 10)
    idx = parents[idx]

plt.show()

