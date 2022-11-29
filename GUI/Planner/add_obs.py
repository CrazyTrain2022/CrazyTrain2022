# add_obs.py

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d

def add_obs(x,y,z,w,h,d):
    w,h,d = np.indices((w+x, h+y, d+z))
    cube1 = (w >= x) & (h >= y) & (d >= z)
    voxels = cube1
    return voxels
   