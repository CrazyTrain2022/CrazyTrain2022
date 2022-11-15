# file for menu class handling everything in the GUI menu

from tkinter import *
from tkinter import ttk
import tkinter as tk

from subprocess import Popen
import yaml
import os
import sys

from pop_up import Pop_up

# Creating class for Gui menu
# Input: master frame and gui_main_frame instance
class Gui_upper_tab_menu:
    def __init__(self, master_, gui_main_frame_) -> None:
        # Instantiating toplevel window
        self.master = master_

        # save the instance of gui_main_frame
        self.gui_main_frame = gui_main_frame_

        # variable to keep track of if yaw option is showing or not
        self.yaw_option_showing = False

        # # create the menu
        menu_widget = tk.Menu(self.master)

        # file menu
        self.file_submen = tk.Menu(menu_widget, tearoff=False)
        self.file_submen.add_command(label="Save mission", command=self.save_mission)
        self.file_submen.add_command(label="Load mission", command=self.load_mission)
        self.file_submen.add_command(label="Remove saved missions", command=self.delete_saved_missions)
        self.file_submen.add_command(label="Show yaw option", command=self.yaw_option)
        self.file_submen.add_command(label="Change parameters", command=self.change_parameters)
        menu_widget.add_cascade(label="File", menu=self.file_submen)

        # drone menu
        drone_submen = tk.Menu(menu_widget, tearoff=False)
        drone_submen.add_command(label="Select drones", command=self.select_drones)
        drone_submen.add_command(label="Start ROS server", command=self.start_ros_server)
        drone_submen.add_command(label="Start hover swarm", command=self.start_hover_swarm)
        drone_submen.add_command(label="Start mocap helper", command=self.start_mocap_helper)
        drone_submen.add_command(label="Show drone position", command=self.drone_position)
        drone_submen.add_command(label="Update", command=self.update_drone_tabs)
        menu_widget.add_cascade(label="Drone", menu=drone_submen)

        # manual control menu
        manual_ctr_submen = tk.Menu(menu_widget, tearoff=False)
        manual_ctr_submen.add_command(label="Take manual control", command=self.manual_ctr_requested)
        manual_ctr_submen.add_command(label="Deactivate manual control", command=self.manual_ctr_deactivated)
        menu_widget.add_cascade(label="Manual control", menu=manual_ctr_submen)

        # mission menu
        mission_submenu = tk.Menu(menu_widget, tearoff=False)
        mission_pattern = tk.Menu(menu_widget, tearoff=False)
        mission_pattern.add_command(label="Helix", command=self.helix_pattern)
        mission_pattern.add_command(label="Figure8", command=self.run_figure8)
        mission_pattern.add_command(label="Hello world", command=self.run_hello_world)
        mission_submenu.add_cascade(label="Pattern", menu=mission_pattern)
        mission_submenu.add_command(label="Follow the leader", command=self.run_follow_the_leader)
        mission_replicate = tk.Menu(menu_widget, tearoff=False)

        menu_widget.add_cascade(label="Missions", menu=mission_submenu)
        
        self.master.config(menu=menu_widget)

        # make sure the correct tabs are showing
        self.update_drone_tabs()


    # saves the trajectories to be loaded later
    # asks for a name for the save and copies the
    # waypoint csv files to this folder
    # input: -
    # output: -
    def save_mission(self):
        pop_up_window = Tk() # window setup
        pop_up_window.title("Save mission")
        pop_up_window.geometry("250x100")

        Pop_up(pop_up_window,"Enter a name for the save", "Save", self.gui_main_frame)

        
    # opens a popup for loading mission data from a previous save
    # input: -
    # output: -
    def load_mission(self):
        pop_up_window = Tk() # window setup
        pop_up_window.title("Load mission")
        pop_up_window.geometry("250x100")

        Pop_up(pop_up_window,"Select mission to load", "Load", self.gui_main_frame)


    # opens a popup for deleting saves mission data
    # input: -
    # output: -
    def delete_saved_missions(self):
        pop_up_window = Tk() # window setup
        pop_up_window.title("Delete save")
        pop_up_window.geometry("250x100")

        Pop_up(pop_up_window,"Select mission to remove", "Remove", self.gui_main_frame)


    # function to update if yaw column is available or not
    # input: -
    # output: -
    def yaw_option(self):
        if(self.yaw_option_showing): # show yaw option
            self.file_submen.entryconfigure(3, label="Show yaw option")
            self.yaw_option_showing = False
            self.gui_main_frame.hide_yaw_option()
        else: # hide yaw option
            self.file_submen.entryconfigure(3, label="Hide yaw option")
            self.yaw_option_showing = True
            self.gui_main_frame.show_yaw_option()
    
    # runs a bash script that opens hover_swarm file to enable changing
    # controller and filter parameter
    # input: -
    # output: -
    def change_parameters(self):
        os.system('gnome-terminal -- bash GUI/bash_scripts/change_parameters.sh')
        
    # runs a bash script that calls crazyswarm chooser.py script to select drones
    # input: -
    # output: -
    def select_drones(self):
        os.system('gnome-terminal -- bash GUI/bash_scripts/select_drones.sh')

    # runs a bash script that starts the ROS server
    # input: -
    # output: -
    def start_ros_server(self):
        os.system('gnome-terminal -- bash GUI/bash_scripts/start_ros.sh')

    # runs a bash script that starts hover_swarm
    # input: -
    # output: -
    def start_hover_swarm(self):
        os.system('gnome-terminal -- bash GUI/bash_scripts/start_hover_swarm.sh')

    # runs a bash script that starts mocap_helper
    # input: -
    # output: -
    def start_mocap_helper(self):
        os.system('gnome-terminal -- bash GUI/bash_scripts/start_mocap_helper.sh')

    # runs a bash script that will provide the drone position
    # input: -
    # output: -
    def drone_position(self):
        os.system('gnome-terminal -- python3 ./crazyswarm/ros_ws/src/crazyswarm/scripts/positionSubscriber.py ')

    # function that update the drone tabs to show only for the selected drone
    # input: -
    # output: -
    def update_drone_tabs(self):
        file = "./crazyswarm/ros_ws/src/crazyswarm/launch/crazyflies.yaml"
        stream = open(file, 'r')
        data = yaml.safe_load_all(stream)

        # make list of selected drones
        selected_drones = []
        starting_coords = []
        for key in data:
            drones = key["crazyflies"]
            for d in drones:
                selected_drones.append(d["id"])
                starting_coords.append(d["initialPosition"])

        # delete tabs for drones not selected
        # does this till no tabs are deleted
        # TODO: fix this in gui_main_frame to work properly
        while(self.gui_main_frame.delete_drone_tabs_not_needed(selected_drones)):
            x = 1

        # make sure that there is a tab for each drone and with the correct starting coordinates
        for i in range(len(selected_drones)):
            self.gui_main_frame.add_drone_tab(selected_drones[i], starting_coords[i])
        
        

    # popup for when the user asks for manual controll of a drone
    # input: -
    # output: -
    def manual_ctr_requested(self):
        pop_up_window = Tk() # window setup
        pop_up_window.title("Load mission")
        pop_up_window.geometry("350x100")

        Pop_up(pop_up_window,"Which drone do you want to manually control?", "Take control", self.gui_main_frame)

    # when the user deactivates manual control
    # input: -
    # output: -
    def manual_ctr_deactivated(self):
        self.gui_main_frame.manual_ctrl_deactivated()


    # when a pattern creation option is pressed
    # input: -
    # output: -
    def helix_pattern(self):
        pop_up_window = Tk() # window setup
        pop_up_window.title("Load mission")
        pop_up_window.geometry("350x120")

        Pop_up(pop_up_window,"Helix pattern options", "Create Helix", self.gui_main_frame)

    # runs a bash script that starts figure8
    # input: -
    # output: -
    def run_figure8(self):
        os.system('gnome-terminal -- bash GUI/bash_scripts/run_figure8.sh')
    
    # runs a bash script that starts hello_world
    # input: -
    # output: -
    def run_hello_world(self):
        os.system('gnome-terminal -- bash GUI/bash_scripts/run_hello_world.sh')

    # runs a bash script starts follow_the_leader
    # input: -
    # output: -
    def run_follow_the_leader(self):
        print("not implemented yet")