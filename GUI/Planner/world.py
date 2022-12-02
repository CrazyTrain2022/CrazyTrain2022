# world.py

import numpy as np
import matplotlib.pyplot as plt

class BoxWorld:
    def __init__(self, lattice):
        """Create a BoxWorld object with the given lattice"""
        self.st_sp = state_space_from_lattice(lattice)
        self.xmin = np.min(lattice[0])
        self.xmax = np.max(lattice[0])
        self.ymin = np.min(lattice[1])
        self.ymax = np.max(lattice[1])
        self.zmin = np.min(lattice[2])
        self.zmax = np.max(lattice[2])

        self._fig = None
        self._boxes = []
        self.x_obst = np.array([]).reshape((0, 2))
        self.y_obst = np.array([]).reshape((0, 2))
        self.z_obst = np.array([]).reshape((0, 2))

    def num_nodes(self):
        """Get the total number of nodes in the state space"""
        return self.st_sp.shape[2]

    def add_box(self, x1, y1, z1, x2, y2, z2, fill_box=True):
        """ Add a box to the world

        Input
            x - x coordinate of the lower left corner
            y - y coordinate of the lower left corner
            z - z coordinate of the lower left corner
            width - width of the box
            height - height of the box
            depth - depth of the box
        """
        self._boxes.append((x1, y1, z1, x2, y2, z2, fill_box))
        self.x_obst = np.row_stack((self.x_obst, [x1, x2]))
        self.y_obst = np.row_stack((self.y_obst, [y1, y2]))
        self.z_obst = np.row_stack((self.z_obst, [z1, z2]))

    def in_bound(self, point):
        """Check if a given point is within the world-model boundaries"""
        c = False
        if (point[0] >= self.xmin) and (point[0] <= self.xmax) and (point[1] >= self.ymin) and (point[1] <= self.ymax):
            c = True
        return c

    def obstacle_free(self, p):
        """ Check if any of a set of points are in collision with obstacles in the world

        Input
          p - numpy array with 2 rows and m columns, where each column represents a point to be checked

        Output
          Returns True if all points are in free space, otherwise False.
        """
        for ii in range(p.shape[1]):
            if obstacle_check(p[0, ii], p[1, ii], p[2, ii], self.x_obst, self.y_obst, self.z_obst):
                return False
        return True

def state_space_from_lattice(lattice):
    """Create a matrix st_sp with all states in the world, given the 
        specified lattice parameters. In the lattice planning, this 3 x N
        matrix is used as a mapping between node number and actual
        coordinates, where the column number is the node number."""
    xmin = lattice[0][0]
    xmax = lattice[0][1]
    ymin = lattice[1][0]
    ymax = lattice[1][1]
    zmin = lattice[2][0]
    zmax = lattice[2][1]

    st_sp = np.array([[xmin, xmax, xmax, xmin, xmin, xmin, xmax, xmax, xmax, xmax, xmax, xmax, xmax, xmin, xmin, xmin],
                     [ymin, ymin, ymax, ymax, ymin, ymin, ymin, ymin, ymin, ymax, ymax, ymax, ymax, ymax, ymax, ymin],
                     [zmin, zmin, zmin, zmin, zmin, zmax, zmax, zmin, zmax, zmax, zmin, zmax, zmax, zmin, zmax, zmax]])

    return st_sp

def obstacle_check(x, y, z, x_obst, y_obst, z_obst):
    """Help function to function obstacle_free, to check collision for a 
        single point x,y"""

    for ii in range(x_obst.shape[0]):
        safe = 0.3
        if (x > (x_obst[ii, 0]-safe) and x < (x_obst[ii, 1]+safe)) and \
            (y > (y_obst[ii, 0]-safe) and y < (y_obst[ii, 1]+safe)) and \
            (z > (z_obst[ii, 0]-safe) and z < (z_obst[ii, 1]+safe)):
            return True
    return False
