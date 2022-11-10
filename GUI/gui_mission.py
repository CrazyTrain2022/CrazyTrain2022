# file for mission pane class

from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk

from subprocess import Popen
import os

from gui_drone_tab import Gui_drone_tab

# Creating App class 
# Label Widgets
class Gui_mission:
    def __init__(self, master) -> None:
        # Instantiating master frame
        self.master = master
        self.master.grid_columnconfigure(0, weight=1)

        # value for keeping track of manual/autonomous
        self.autonomous = TRUE

        # bool to keep track if yaw column should be showing or not
        self.yaw_option_showing = False

        # mission pane definitions
        Label(master, text = "Crazytrain", font=("Helvetica", 25)).grid(column=0, row=0, padx=1, pady=1)

        # add tabs for drone data
        pane_drone = LabelFrame(master, text="Mission planning",width=250, height=300, relief=SUNKEN)
        self.tabControl = ttk.Notebook(pane_drone)

        # list of tabs
        self.drone_tabs = []

        # place the tabs in the frame
        self.tabControl.pack(expand=1, fill="both")
        pane_drone.grid(column=0, row=1, padx=1, pady=1)

        # mission start buttons
        pane_start_flight = Frame(master, width=250, height=100)
        pane_start_flight.grid(column=0, row=2, padx=1, pady=10)

        emergency_btn = Button(pane_start_flight, text = "Emergency Stop", bg='red',fg="black", command=self.emergency_pressed)
        emergency_btn.grid(column=0, row=0, columnspan=2, padx=5, pady=5)

        sim_btn = Button(pane_start_flight, text = "Start simulation", command=self.run_trajectory_simulation)
        sim_btn.grid(column=0, row=1, padx=5, pady=1)
        drone_btn = Button(pane_start_flight, text = "Start drone flight", command=self.run_flight)
        drone_btn.grid(column=1, row=1, padx=5, pady=1)
        flight_sim_btn = Button(pane_start_flight, text = "Start flight and simulation", command=self.run_flight_sim)
        flight_sim_btn.grid(column=0, row=2, columnspan=2, padx=5, pady=5)

        # indicator for showing control mode active
        self.pane_man_ctrl = LabelFrame(master, text="Control mode" , width=200, height=200, relief=SUNKEN, )
        automatic_ctr_image_load = Image.open("GUI/pictures/xbox_controller_inactive.png")
        manual_ctr_image_load = Image.open("GUI/pictures/xbox_controller_active.png")
        self.automatic_ctr_image = ImageTk.PhotoImage(automatic_ctr_image_load)
        self.manual_ctr_image = ImageTk.PhotoImage(manual_ctr_image_load)

        self.control_image = Label(self.pane_man_ctrl, image=self.automatic_ctr_image)
        self.control_image.grid(column=0, row=0, sticky="WE")
        self.pane_man_ctrl.grid_rowconfigure(0, weight=1)
        self.pane_man_ctrl.grid_columnconfigure(0, weight=1)
        self.pane_man_ctrl.grid(column=0, row=3, padx=1, pady=1)
        


    # function for starting simulation from the terminal
    # input: -
    # output: -
    def run_trajectory_simulation(self):
        if(self.autonomous):
            worked = self.load_waypoints_to_csv() # make sure there are trajectory files to load
            if(worked):
                Popen("python3 gui_simulate.py --sim", shell=True, cwd="crazyswarm/ros_ws/src/crazyswarm/scripts")
        else:
            Popen("python3 manual_control.py --sim --manual", shell=True, cwd="crazyswarm/ros_ws/src/crazyswarm/scripts")


    # start flight script by callin a bash script
    # input: -
    # output: -
    def run_flight(self):
        if(self.autonomous):
            worked = self.load_waypoints_to_csv() # make sure there are trajectory files to load
            if(worked):
                os.system('gnome-terminal -- bash GUI/bash_scripts/start_flight.sh')
        else:
            Popen("python3 manual_control.py --t --manual", shell=True, cwd="crazyswarm/ros_ws/src/crazyswarm/scripts")

    def run_flight_sim(self):
        if(self.autonomous):
            worked = self.load_waypoints_to_csv() # make sure there are trajectory files to load
            if(worked):
                #os.system('gnome-terminal -- bash GUI/bash_scripts/start_flight.sh')
                print("not implemented yet")
        else:
            #Popen("python3 manual_control.py --t --manual", shell=True, cwd="crazyswarm/ros_ws/src/crazyswarm/scripts")
            print("not implemented yet")

    # function for loading all drone mission data to waypoint csv files
    # input: -
    # output: [bool] True or False depending on if the trajectory was created properly
    def load_waypoints_to_csv(self):
        for tab in self.drone_tabs:
            worked = tab.set_points()
            if(not worked):
                return False
        return True
        

    # function for saving all mission points for all drones
    # input: -
    # output: -
    def save_all_mission_points(self, folder_path):
        for drone in self.drone_tabs:
            drone.save_mission(folder_path)

    # function for loading all mission points for all drones from the waypoint csv files
    # input: -
    # output: -
    def load_mission_points(self):
        # delete extra waypoint rows and display waypoints
        for drone in self.drone_tabs:
            drone.clear_all_entries()
            drone.display_loaded_mission()

    # show yaw option for every drone tab
    # input: -
    # output: -
    def show_yaw_option(self):
        for drone in self.drone_tabs:
            drone.show_yaw_option()

    # hide yaw option for every drone tab
    # input: -
    # output: -
    def hide_yaw_option(self):
        for drone in self.drone_tabs:
            drone.hide_yaw_option()

    # make sure that there is a tab for the drone
    # if there isn't one then create one
    # input: [int] drone number
    # output: -
    def add_drone_tab(self, drone_nr, start_coord):
        # if tab doesn't exsist add tab
        if(not any(x for x in self.drone_tabs if x.name == str(drone_nr))):
            tab = ttk.Frame(self.master, width=250, height=300)
            self.tabControl.add(tab, text="Drone "+str(drone_nr))

            # create tab
            self.drone_tabs.append(Gui_drone_tab(tab, str(drone_nr), start_coord, self.yaw_option_showing))

    # deletes tabs for drones not selected
    # input: [list] of selected drones
    # output: [bool] to indicate if a tab was removed
    def delete_drone_tabs_not_needed(self, selected_drones):
        removed = FALSE
        for tab in self.drone_tabs:
            if(not any(x for x in selected_drones if str(x) == str(tab.name))):
                tab_index = self.drone_tabs.index(tab)
                self.drone_tabs.remove(tab)
                self.tabControl.forget(tab_index)
                removed = TRUE
        
        self.tabControl.pack(expand=1, fill="both")
        return removed

    # returns a list of tabs currently showing
    # input: -
    # output: [list] of drone tabs
    def get_active_tabs(self):
        lst = []
        for tab in self.drone_tabs:
            lst.append(tab.name)
        return lst

    # runs bash script to send ROS topic of emergency landing
    # input: -
    # output: -
    def emergency_pressed(self):
        print("Emergency pressed")
        os.system('gnome-terminal -- bash GUI/bash_scripts/emergency.sh')


    # enabled manual control of a drone
    # input: -
    # output: -
    def manual_ctrl_activated(self, drone):
        print("Manual control for drone " + drone)
        self.autonomous = FALSE
        self.control_image.config(image=self.manual_ctr_image)

    # disables manual control of a drone. This should make all drones land
    # input: -
    # output: -
    def manual_ctrl_deactivated(self):
        print("Disables manual control, automatic landing initiated")
        self.autonomous = TRUE
        self.control_image.config(image=self.automatic_ctr_image)