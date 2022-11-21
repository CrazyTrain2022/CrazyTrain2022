# file for class with drone tab in mission creation
from tkinter import *
from tkinter import ttk
import tkinter as tk

import numpy as np
from numpy import genfromtxt

import os
from shutil import copyfile
from subprocess import Popen
from mission_point import Mission_point

class Gui_drone_scroll_tab:
    def __init__(self, master, name_, start_coord_, show_yaw_, rrt_on_) -> None:
        self.connected = False
        self.battery_level = 0
        self.points_np_mtx = np.array([0.0,0.0,0.0])
        self.name = name_
        self.start_coord = start_coord_
        self.show_yaw = show_yaw_
        self.rrt_on = rrt_on_

        Label(master, text = "Drone " + self.name, font=("Arial", 18)).grid(column=0, row=0)

        # Create A Main Frame
        mission_frame = Frame(master, height=150, width=250)
        mission_frame.grid(column=0, row=2)

        # header update variable
        self.show_yaw_txt = "x             y             z          yaw \n ---------------------------------------------"
        self.hide_yaw_txt = "x \t y \t z \t \n ----------------------------------- \t \t "
        self.yaw_txt = StringVar()
        self.yaw_txt.set(self.hide_yaw_txt)

        self.header_lbl = Label(mission_frame, textvariable=self.yaw_txt)
        self.header_lbl.grid(column=0, row=0, columnspan=8)

        # Create A Canvas
        self.canvas = Canvas(mission_frame, height=150, width=250)
        self.canvas.grid(column=0, row=1, columnspan=3)

        # Add A Scrollbar To The Canvas
        scroll = ttk.Scrollbar(mission_frame, orient=VERTICAL, command=self.canvas.yview)
        scroll.grid(column=4, row=0, rowspan=8, sticky=N+S+E)

        # Configure The Canvas
        self.canvas.configure(yscrollcommand=scroll.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all")))

        # Create ANOTHER Frame INSIDE the Canvas (yeah I know...)
        self.points_frame = Frame(self.canvas)

        # add that new frame to a window in the canvas
        self.canvas.create_window((0,0), window=self.points_frame, anchor="nw")

        # add mission point rows to points_frame
        self.points_entry_lst = []
        # add the start position for the drone
        self.points_entry_lst.append(Mission_point(self.points_frame,0, self.show_yaw))
        self.points_entry_lst[0].set_coord(self.start_coord)
        self.points_entry_lst[0].set_disable()
        
        # add two mission points as default
        self.points_entry_lst.append(Mission_point(self.points_frame,1, self.show_yaw))
        self.points_entry_lst.append(Mission_point(self.points_frame,2, self.show_yaw))

        # add buttons to manipulate these mission_points
        Button(mission_frame, text = "Add entry",command=self.add_entry).grid(column=0, row=1111)
        Button(mission_frame, text = "Delete last",command=self.delete_entry).grid(column=1, row=1111)

    # adds a new misison point
    # input: -
    # output: -
    def add_entry(self):
        self.points_entry_lst.append(Mission_point(self.points_frame,len(self.points_entry_lst), self.show_yaw))
        self.updateScrollRegion()

    # deletes the last mission point in the list and detroy it properly
    # input: -
    # output: -
    def delete_entry(self):
        if(len(self.points_entry_lst) > 1):
            last_row = self.points_entry_lst.pop()
            last_row.nbr_lbl.destroy()
            last_row.x.destroy()
            last_row.y.destroy()
            last_row.z.destroy()
            last_row.yaw.destroy()
        self.updateScrollRegion()


    # saves the points from the tab in an np.array
    # input: -
    # output: [bool] True or False depending on if the trajectory was created properly
    def set_points(self):
        self.points_np_array = np.array([[12,-3,-1]])
        for entry in self.points_entry_lst:
            value = entry.get_coord(self.start_coord)
            if((np.array(value) == self.points_np_array[-1]).all()):    # if row same as the one above it
                print("Same row twice in a row. The duplicate is skipped")
            elif(value != -1 and value != 0):                           # if row can be read fine
                self.points_np_array = np.append(self.points_np_array, [value], axis=0)
            elif(value == -1):                                          # if a number can't be read
                print("WARNING: Can't load trajectory for drone "+str(self.name))
                return False

        self.points_np_array = np.delete(self.points_np_array, (0), axis=0) # remove dummy entry
        self.points_np_array = np.delete(self.points_np_array, (0), axis=0) # remove starting position
        self.points_np_array = np.insert(self.points_np_array, (0), [0,0.01,self.points_np_array[0][2]], axis=0) # add point to rise to
        self.save_csv_file(self.points_np_array)
        #planner_on = True
        if self.rrt_on:
            Popen("python3 run_rrt.py ", shell=True, cwd="Planner/")
            print("running rrt")
        self.make_trajectory_file()
        return True


    # function to update scrollbar when mission points are added/removed
    # input: -
    # output: -
    def updateScrollRegion(self):
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.points_frame.bbox())
    # creates a csv file for path points from points_mtx
    # this function takes waypoints as input argument instead of using class variable to enable
    # usage from other class with different waypoints as well
    # input: [np.array] waypoints
    # output: -
    def save_csv_file(self, waypoints):
        print("working")
        np.savetxt('GUI/points_csv/drone'+ str(self.name)+'waypoints.csv', X=waypoints, delimiter=',', fmt='%10.3f')


    # use waypoint CSV file to make trajectory CSV file
    # also handles some global vs local coordinates
    # input: -
    # output: -
    def make_trajectory_file(self):
        print("Create trajectory for drone "+str(self.name))
        v_max = 1.5
        a_max = 1.5
        #planner_on = True
        if self.rrt_on:
            print("using rrt")
            waypoint_file = './Planner/utdata.csv'
        else:
            waypoint_file = './GUI/points_csv/drone'+str(self.name)+'waypoints.csv'
        # create local_waypoint file so the trajectories are made from the correct place
        global_waypoints = genfromtxt(waypoint_file, delimiter=',')
        local_waypoints = global_waypoints + self.start_coord
        waypoint_file_local = 'GUI/points_csv/drone'+str(self.name)+'waypoints_local.csv'

        # create new local_drone*waypoints.csv file
        np.savetxt(waypoint_file_local, X=local_waypoints, delimiter=',', fmt='%10.3f')
        trajectory_file = './crazyswarm/ros_ws/src/crazyswarm/scripts/drone'+str(self.name)+'trajectory.csv'
        os.system('./uav_trajectories/build/genTrajectory -i ' + waypoint_file_local + ' --v_max ' + str(v_max) + ' --a_max ' + str(a_max) + ' -o ' + trajectory_file)

        # add yaw to the trajectory file if the yaw option is active
        if(self.show_yaw):
            print("adding yaw")
            yaw_np = np.array(self.get_yaws())
            self.make_yaw_csv(yaw_np)
            os.system('python3 crazyswarm/ros_ws/src/crazyswarm/scripts/yaw_generation.py crazyswarm/ros_ws/src/crazyswarm/scripts/drone' + str(self.name) + 'trajectory.csv GUI/points_csv/drone' + str(self.name) + 'yaw.csv ' + str(self.name))
            

    # saves its csv file into a folder in the save_missions dir
    # input: [string] the destinated folder which to save the file in
    # output: -
    def save_mission(self, dest_folder):
        self.set_points() # read waypoints to CSV file
        
        # check so the csv file exists
        if(os.path.isfile('GUI/points_csv/drone'+str(self.name)+'waypoints.csv')):
            # save waypoints
            self.set_points()
            copyfile('GUI/points_csv/drone'+str(self.name)+'waypoints.csv', dest_folder+'/drone'+str(self.name)+'waypoints.csv')
            # save yaw
            yaw_np = np.array(self.get_yaws())
            self.make_yaw_csv(yaw_np)
            copyfile('GUI/points_csv/drone'+str(self.name)+'yaw.csv', dest_folder+'/drone'+str(self.name)+'yaw.csv')
            print("Drone " + str(self.name) + " waypoints saved")
        else:
            print("Drone " + str(self.name) + " has no waypoint csv file to save")

    # display waypoints from waypoint csv files on gui
    # input: -
    # output: -
    def display_loaded_mission(self):
        # read from the correct waypoint csv file
        self.points_np_array = genfromtxt('GUI/points_csv/drone'+str(self.name)+'waypoints.csv', delimiter=',')

        # read drone*yaw-csv file if there is one, otherwise create np.array of zeros
        try:
            yaw_np_array = genfromtxt('GUI/points_csv/drone'+str(self.name)+'yaw.csv', delimiter=',')
            # np.append(yaw_np_array, 0)
        except:
            l = len(self.points_np_array)
            yaw_np_array = np.zeros(l+1)

        # make sure there are enough mission points to display all waypoints
        while(self.points_np_array.ndim == 2 and len(self.points_np_array) +1 > len(self.points_entry_lst)):
            self.points_entry_lst.append(Mission_point(self.points_frame, len(self.points_entry_lst), self.show_yaw))

        # set the values for each mission_point
        if(self.points_np_array.ndim == 2): #if matrix or just list
            for i in range(len(self.points_np_array)):
                self.points_entry_lst[i+1].set_coord(self.points_np_array[i])
                self.points_entry_lst[i+1].set_yaw(yaw_np_array[i])
        else:
            if(len(self.points_entry_lst) == 0):    # make sure there is a entry to load data to
                self.points_entry_lst.append(Mission_point(self.points_frame, 1, self.show_yaw))
            self.points_entry_lst[0].set_coord(self.points_np_array)
            self.points_entry_lst[0].set_yaw(yaw_np_array)

        # update scroll region
        self.updateScrollRegion()

    # clear all entries 
    # input: -
    # output: -
    def clear_all_entries(self):
        #destroy and unpack entries
        while(len(self.points_entry_lst) > 1):
            self.delete_entry()

    # collect all yaws
    # input - 
    # output: [list] yaws
    def get_yaws(self):
        yaw_lst = []
        for p in self.points_entry_lst:
            if(not p.number == 0):
                yaw_lst.append(p.get_yaw())
        return yaw_lst


    # show yaw option for drone
    # input: -
    # output: -
    def show_yaw_option(self):
        self.yaw_txt.set(self.show_yaw_txt)
        self.show_yaw = True
        for point in self.points_entry_lst:
            point.show_yaw()

    # hide yaw option for drone
    # input: -
    # output: -
    def hide_yaw_option(self):
        self.yaw_txt.set(self.hide_yaw_txt)
        self.show_yaw = False
        for point in self.points_entry_lst:
            point.hide_yaw()

    # creating a yaw_csv file to save
    # input: [np.array] yaw_np cotaining all ways from the mission points
    # output: -
    def make_yaw_csv(self, yaw_np):
        yaw_file = 'GUI/points_csv/drone'+str(self.name)+"yaw.csv"
        np.savetxt(yaw_file, X=yaw_np, delimiter=',', fmt='%i', header="yaw^0")
