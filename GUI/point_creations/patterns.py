import numpy as np
import math

class Patterns():
    def __init__(self) -> None:
        pass

    def helix(self,radius, height, center, nbr_waypoints=10, incr_radius=0):
        x,y,z=create_helix(radius, height, incr_radius, center, int(nbr_waypoints/height))
        return store_waypoints(x,y,z)

    def circle(self, radius, height, center, nbr_waypoints):
        x,y,z = create_circle(radius, height, center, nbr_waypoints)
        return store_waypoints(x,y,z)

    def line(self, startpoint, endpoint, nbr_waypoints):
        x, y, z= create_line(startpoint, endpoint, nbr_waypoints)
        return store_waypoints(x, y, z)

def create_circle(radius, height, center, nbr_waypoints):
    x = []
    y = []
    z = []
    for t in range(int(nbr_waypoints)):
        x.append(radius*math.cos(t)+center[0])
        y.append(radius*math.sin(t)+center[1])
        z.append(height)
    return x,y,z

def create_helix(radius, height, incr_radius, center, nbr_waypoints):
    x = []
    y = []
    z = []

    for t in range(int(nbr_waypoints)):

        # Check if expanding helix or not
        if incr_radius==1:
            expand=t
        else:
            expand=1

        x.append(radius*expand*math.cos(t)+center[0])
        y.append(radius*expand*math.sin(t)+center[1])
        z.append(t*height)#/(nbr_waypoints-1))
    return x,y,z

def create_line(startpoint, endpoint, nbr_waypoints):   
    x = np.linspace(startpoint[0], endpoint[0], int(nbr_waypoints))
    y = np.linspace(startpoint[1], endpoint[1], int(nbr_waypoints))
    z = np.linspace(startpoint[2], endpoint[2], int(nbr_waypoints))
    return x,y,z

def store_waypoints(x, y, z):
    point_array = np.array([[0,0,0]])
    for i in range(len(x)):
        point_array = np.append(point_array, [[x[i],y[i],z[i]/10]], axis = 0)
    point_array = np.delete(point_array,(0),axis=0)
    point_array = np.delete(point_array,(0),axis=0)
    return point_array

# Pattern_obj = Patterns()