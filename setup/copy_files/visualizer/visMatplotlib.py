import warnings

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection
import matplotlib.pyplot as plt
import numpy as np
import math

# to ignore warnings TODO: fix this propperly
from matplotlib.axes._axes import _log as matplotlib_axes_logger

import yaml

import uav_trajectory

COLOR = [[0.5, 0.5, 1], [1, 0.5, 0.5], [0.5, 1, 0.5], [0.5, 1, 1], [0.7, 0.7, 0.5], [0.2, 0.2, 0.2], [0.5, 0.2, 0.8], [0.4, 0.4, 0.1]]
VISIONEN_X_LENGTH = 11.70
VISIONEN_Y_LENGTH = 11.70
VISIONEN_Z_LENGTH = 5.70

#Keep simulation plot inside these limits (in meters).
X_LIMIT = 2.5
Y_LIMIT = 2.5
Z_LIMIT = 3.5

class VisMatplotlib:
    def __init__(self, flags=None):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim([-VISIONEN_X_LENGTH/2, VISIONEN_X_LENGTH/2]) # here the measurements for visionen should be added
        self.ax.set_ylim([-VISIONEN_Y_LENGTH/2, VISIONEN_Y_LENGTH/2])
        self.ax.set_zlim([0, VISIONEN_Z_LENGTH])
        self.ax.set_xlabel("X [m]")
        self.ax.set_ylabel("Y [m]")
        self.ax.set_zlabel("Z [m]")
        self.plot = None
        self.timeAnnotation = self.ax.annotate("Time", xy=(0, 0), xycoords='axes fraction', fontsize=12, ha='right', va='bottom')
        # self.yawAngnotation = self.ax.annotate("Yaw drone 1: ", xy=(1, 1), xycoords='axes fraction', fontsize=12, ha='right', va='bottom')

        self.line_color = 0.3 * np.ones(3)
        #Reading manual or autonomous control
        self.manual_mode = 0
        if flags == "--manual":
            self.manual_mode = 1

        matplotlib_axes_logger.setLevel('ERROR')
        

        # Lazy-constructed data for connectivity graph gfx.
        self.graph_edges = None
        self.graph_lines = None
        self.graph = None

        # print(self.manual_mode)
        if not self.manual_mode == 1:
            # read which drones and used and if they should be plotted or not from plot_trajectories.yaml
            self.drone_lst = []
            self.plot_lst = []
            file = "plot_trajectories.yaml"
            stream = open(file, 'r')
            data = yaml.safe_load_all(stream)
            for aa in data:
                settings = aa["settings"]
                for key in settings:
                    self.drone_lst.append(key["i"])
                    self.plot_lst.append(key["plot"])


            # read waypoints file
            waypoints_lst = []
            self.wayx_lst = [] 
            self.wayy_lst = [] 
            self.wayz_lst = []
            i = 0
            for drone in self.drone_lst:
                waypoints_lst.append(np.loadtxt("../../../../../GUI/points_csv/drone"+str(drone)+"waypoints_local.csv", delimiter=",", usecols=range(3)))
                self.wayx_lst.append([row[0] for row in waypoints_lst[i]])
                self.wayy_lst.append([row[1] for row in waypoints_lst[i]])
                self.wayz_lst. append([row[2] for row in waypoints_lst[i]])
                i += 1

            # read trajectory files and do some stuff
            self.traj_lst = []
            self.evals_lst = []
            i = 0
            for drone in self.drone_lst:
                self.traj_lst.append(uav_trajectory.Trajectory())
                self.traj_lst[i].loadcsv("drone"+str(drone)+"trajectory.csv")

                # do some stuff
                ts = np.arange(0, self.traj_lst[i].duration, 0.01)
                self.evals_lst.append(np.empty((len(ts), 15)))
                for t, j in zip(ts, range(0, len(ts))):
                    e = self.traj_lst[i].eval(t)
                    if(not e == None):
                        self.evals_lst[i][j, 0:3]  = e.pos
                        self.evals_lst[i][j, 12]   = e.yaw
                
                i += 1



    def setGraph(self, edges):
        """Set edges of graph visualization - sequence of (i,j) tuples."""

        # Only allocate new memory if we need to.
        n_edges = len(edges)
        if self.graph_edges is None or n_edges != len(self.graph_edges):
            self.graph_lines = np.zeros((n_edges, 2, 3))
        self.graph_edges = edges

        # Lazily construct Matplotlib object for graph.
        if self.graph is None:
            self.graph = Line3DCollection(self.graph_lines, edgecolor=self.line_color)
            self.ax.add_collection(self.graph)

    def showEllipsoids(self, radii):
        warnings.warn("showEllipsoids not implemented in Matplotlib visualizer.")

    def update(self, t, crazyflies):
        xs = []
        ys = []
        zs = []
        cs = []
        xs_yaw = []
        ys_yaw = []
        cs_yaw = []
        i = 0
        for cf in crazyflies:
            x, y, z = cf.position()
            yaw = cf.yaw()
            yaw_arrow = [math.sin(yaw), math.cos(yaw)]
            arrow_size = 0.3
            color = cf.ledRGB
            color = COLOR[i]
            i += 1
            if i > 7:
                i = 0
            xs.append(x)
            ys.append(y)
            zs.append(z)
            cs.append(color)
            xs_yaw.append(x+(arrow_size*yaw_arrow[0]))
            ys_yaw.append(y+(arrow_size*yaw_arrow[1]))
            cs_yaw = (0,0,0)

        if self.plot is None:
            self.plot = self.ax.scatter(xs, ys, zs, c=cs, marker='X')     # plot drones 
            self.plot_yaw = self.ax.scatter(xs_yaw,ys_yaw,zs, c = cs_yaw, marker ='.') #Plot yaw points drones
            if not self.manual_mode == 1:
                for d in range(len(self.drone_lst)):
                    if(self.plot_lst[d] == 2):
                        for p in range(len(self.wayx_lst[d])):                    # plot waypoints
                            self.ax.scatter3D(self.wayx_lst[d][p], self.wayy_lst[d][p], self.wayz_lst[d][p], c=COLOR[d], s=5)
                        self.ax.plot(self.evals_lst[d][:,0], self.evals_lst[d][:,1], self.evals_lst[d][:,2], linewidth=0.5, c=COLOR[d])
                        
        else:
            # TODO: Don't use protected members.
            self.plot._offsets3d = (xs, ys, zs)
            self.plot.set_facecolors(cs)
            self.plot.set_edgecolors(cs)
            self.plot._facecolor3d = self.plot.get_facecolor()
            self.plot._edgecolor3d = self.plot.get_edgecolor()

            self.plot_yaw._offsets3d = (xs_yaw, ys_yaw, zs)
            self.plot_yaw.set_facecolors(cs_yaw)
            self.plot_yaw.set_edgecolors(cs_yaw)
            self.plot_yaw._facecolor3d = self.plot_yaw.get_facecolor()
            self.plot_yaw._edgecolor3d = self.plot_yaw.get_edgecolor()

        if self.graph is not None:
            # Update graph line segments to match new Crazyflie positions.
            for k, (i, j) in enumerate(self.graph_edges):
                self.graph_lines[k, 0, :] = xs[i], ys[i], zs[i]
                self.graph_lines[k, 1, :] = xs[j], ys[j], zs[j]
                self.graph.set_segments(self.graph_lines)

        self.timeAnnotation.set_text("{} s".format(round(t)))
        cf = crazyflies[0]
        # self.yawAnnotation.set_text("Drone 1 yaw: {:.2f} degrees".format((cf.state.yaw*180/math.pi)%360))
        plt.pause(0.0001)

    def render(self):
        warnings.warn("Rendering video not supported in VisMatplotlib yet.")
        return None
