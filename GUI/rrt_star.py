#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 10:04:05 2022

@author: patli821
"""
# Imports
from random import sample
import numpy as np
from world import BoxWorld

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
        """Function for connecting along a path from tree root to x_new with
        #minimum cost among the states in a neighborhood of x_new
        #described by the (column) indices near_idx in nodes. The variable
        #idx_nearest is the index (column in matrix nodes) for the node
        #closest to x_new and cost_via_nearest is the cost to reach x_new
        #via the nearest node."""

        idx_min = idx_nearest
        cost_min = cost_via_nearest

        for idx_n in near_idx:
            x_near = nodes[:, idx_n]

            if (x_new[0] == x_near[0]) and (x_new[1] == x_near[1]) and (x_new[2] == x_near[2]):
                p = x_new[:, None]
            else:
                # Check if node coordinates for near and new are the same in one of the dimensions and substitute the arange command for runnable code
                if x_near[2] == x_new[2]:
                    p = np.row_stack(
                    (
                        np.arange(x_near[0], x_new[0], (x_new[0] - x_near[0]) / 10),
                        np.arange(x_near[1], x_new[1], (x_new[1] - x_near[1]) / 10),
                        np.full((1,10),x_near[2]),
                        #np.array([x_new[2], x_new[2], x_new[2], x_new[2], x_new[2], x_new[2], x_new[2], x_new[2], x_new[2], x_new[2]]),
                    )
                    )
                elif x_near[1] == x_new[1]:
                    p = np.row_stack(
                    (
                        np.arange(x_near[0], x_new[0], (x_new[0] - x_near[0]) / 10),
                        np.full((1,10),x_near[1]),
                        np.arange(x_near[2], x_new[2], (x_new[2] - x_near[2]) / 10),
                    )
                    )
                elif x_near[0] == x_new[0]:             
                    p = np.row_stack(
                    (
                        np.full((1,10),x_near[0]),
                        np.arange(x_near[1], x_new[1], (x_new[1] - x_near[1]) / 10),
                        np.arange(x_near[2], x_new[2], (x_new[2] - x_near[2]) / 10),
                    )
                    )
                else:
                    p = np.row_stack(
                    (
                        np.arange(x_near[0], x_new[0], (x_new[0] - x_near[0]) / 10),
                        np.arange(x_near[1], x_new[1], (x_new[1] - x_near[1]) / 10),
                        np.arange(x_near[2], x_new[2], (x_new[2] - x_near[2]) / 10),
                    )
                    )
            cost_near = cost[idx_n] + np.sqrt((x_near[0] - x_new[0])**2 + (x_near[1] - x_new[1])**2 + (x_near[2] - x_new[2])**2)

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
            else:
                # Check if node coordinates for near and new are the same in one of the dimensions and substitute the arange command for runnable code
                if x_near[2] == x_new[2]:
                    p = np.row_stack(
                    (
                        np.arange(x_near[0], x_new[0], (x_new[0] - x_near[0]) / 10),
                        np.arange(x_near[1], x_new[1], (x_new[1] - x_near[1]) / 10),
                        np.full((1,10),x_near[2]),
                    )
                    )
                elif x_near[1] == x_new[1]:
                    p = np.row_stack(
                    (
                        np.arange(x_near[0], x_new[0], (x_new[0] - x_near[0]) / 10),
                        np.full((1,10),x_near[1]),
                        np.arange(x_near[2], x_new[2], (x_new[2] - x_near[2]) / 10),
                    )
                    )
                elif x_near[0] == x_new[0]:             
                    p = np.row_stack(
                    (
                        np.full((1,10),x_near[0]),
                        np.arange(x_near[1], x_new[1], (x_new[1] - x_near[1]) / 10),
                        np.arange(x_near[2], x_new[2], (x_new[2] - x_near[2]) / 10),
                    )
                    )
                else:
                    p = np.row_stack(
                    (
                        np.arange(x_near[0], x_new[0], (x_new[0] - x_near[0]) / 10),
                        np.arange(x_near[1], x_new[1], (x_new[1] - x_near[1]) / 10),
                        np.arange(x_near[2], x_new[2], (x_new[2] - x_near[2]) / 10),
                    )
                    )
            cost_near = cost_min + np.linalg.norm(x_near - x_new)
            if cost_near < cost[idx_n] and world.obstacle_free(p):
                parents[idx_n] = len(parents) - 1
                cost[idx_n] = cost_near



    # Initalize lists to contain the node data in planner
    nodes = np.array(start.reshape((-1, 1)))  # Make numpy column vector
    parents = [0]  # Initial state has no parent
    cost = np.array([0]) # Inital cost is zero

    # Run the planning algorithm
    for i in range(0,opts["K"]+1):
        print("Iterating, no: ", i)
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
                    break
        else: 
            cost = np.append(cost, cost_min.reshape((-1, 1)), axis=None)
            nodes = np.append(nodes, node_new.reshape((-1,1)),axis=1)
            parents.append(idx_min)
            rewire_neighborhood(node_new, node_neigh_idx, cost_min)
            if (opts["eps"] > 0) and (np.sum((goal - node_new) ** 2, axis=0) < opts["eps"]):
                break

    goal_idx = np.argmin(np.sum((nodes - goal.reshape((-1, 1))) ** 2, axis=0))

    return goal_idx, nodes, parents

