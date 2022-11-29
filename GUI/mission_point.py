# file for class with mission point

from tkinter import *
from tkinter import ttk
import tkinter as tk

# global limits to which points can be entered
X_MAX = 5.0
Y_MAX = 5.0
Z_MAX = 5.0

# class for handling waypoints. 
class Mission_point:
    def __init__(self, master_, number_, yaw_option_) -> None:
        self.master = master_
        self.number = number_

        # option to show yaw or not
        self.yaw_option = yaw_option_
        
        # create and place entries for waypoints
        self.nbr_lbl = Label(self.master, text = str(number_)+":", font=("Arial", 12))
        self.nbr_lbl.grid(column=0, row=self.number, padx=1, pady=1)
        self.x = Entry(self.master, width=5)
        self.x.grid(column=1, row=self.number, padx=5, pady=1)
        self.y = Entry(self.master, width=5)
        self.y.grid(column=2, row=self.number, padx=5, pady=1)
        self.z = Entry(self.master, width=5)
        self.z.grid(column=3, row=self.number, padx=5, pady=1)

        # yaw option, defaults to zero
        self.yaw = Entry(self.master, width=5)
        self.yaw.delete(0,END)
        self.yaw.insert(0,"0")
        if(self.yaw_option): # only place on grid if yaw option is selected
            self.yaw.grid(column=4, row=self.number, padx=5, pady=1)

    # getters for mission point coordinates
    def get_x(self):
        return self.x.get()

    def get_y(self):
        return self.y.get()

    def get_z(self):
        return self.z.get()

    def get_yaw(self):
        return int(self.yaw.get())


    # get function for coordinates
    # input: [float list] start_coord with the start coordinates for the drone.
    #         used to check if global coordinates is inside allowed volume
    # output: [float list] returns coordinates if allowed, return 0 if row empty an
    #           and -1 if value not allowed and waypoint load should be terminated
    def get_coord(self, start_coord):
        # get string values from entries
        x = self.x.get()
        y = self.y.get()
        z = self.z.get()

        # check if all entries are numbers (either int or float)
        x_res = (x.replace('.','',1).replace('-','',1).isdigit())
        y_res = (y.replace('.','',1).replace('-','',1).isdigit())
        z_res = (z.replace('.','',1).replace('-','',1).isdigit())

        # check if the enteries are numbers of size that fits in Visionen
        if(x_res and y_res and z_res):
            if(not self.allowed_coord(float(x), float(y), float(z), start_coord)):  # check if in allowed range
                print("not allowed")
                return -1
            return [float(x), float(y), float(z)] # return the coordinates 
        elif(x == '' and y == '' and z == ''): # if empty return 0 to signal row skipped
            return 0
        else:                                  # else return -1 for undefined behaviour
            return -1

    # sets coordiates in the entries
    # input: [string lst]
    # output: -
    def set_coord(self, coord):
        self.x.delete(0,END)
        self.x.insert(0,str(float(coord[0])))
        self.y.delete(0,END)
        self.y.insert(0,str(float(coord[1])))
        self.z.delete(0,END)
        self.z.insert(0,str(float(coord[2])))

    # sets yaw in the optional yaw entry
    # input: [string] yaw
    # output: -
    def set_yaw(self,yaw):
        self.yaw.delete(0,END)
        self.yaw.insert(0,str(int(yaw)))

    # set mission point enable for edit
    # input: -
    # output: -
    def set_enable(self):
        self.x.config(state='enabled')
        self.y.config(state='enabled')
        self.z.config(state='enabled')
        self.yaw.config(state='enabled')

    # set mission point disabled (used for starting position)
    # input: -
    # output: -
    def set_disable(self):
        self.x.config(state='disabled')
        self.y.config(state='disabled')
        self.z.config(state='disabled')
        self.yaw.config(state='disabled')

    # functions for displaying and removing the yaw option
    def show_yaw(self):
        self.yaw.grid(column=4, row=self.number, padx=5, pady=1)

    def hide_yaw(self):
        self.yaw.grid_forget()

        
    # checks if the points are allowed
    # input: [float] x,y,z coordinate & start coordinates
    # output: [bool] if allowed or not
    def allowed_coord(self,x,y,z, start_coord):
        # check again too small (non zero) as uav_trajectories can't handle this
        if(not x == 0 and abs(x) < 0.05):
            return False
        if(not y == 0 and abs(y) < 0.05):
            return False
        if(not z == 0 and abs(z) < 0.05):
            return False

        # check if outside of allowed area
        # takes start coordinates into consideratiion
        if(abs(x+float(start_coord[0])) > X_MAX):
            return False
        if(abs(y+float(start_coord[1])) > Y_MAX):
            return False
        if(abs(z+float(start_coord[2])) > Z_MAX):
            return False
        if(z < 0):          # if bellow ground
            return False

        # otherwise ok
        return True