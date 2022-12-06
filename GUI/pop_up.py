# a general class for pop-up windows taking an entry

from tkinter import *
from tkinter import ttk
import tkinter as tk
from typing import Pattern
from obstacle_point import Obstacle_point

from point_creations.patterns import Patterns

import os
import glob
from shutil import copyfile, rmtree
import csv

# general class popup for when a entry is needed
# class uses the text of the button to determine what sort of 
# popup window it should be
# input: main window, label text, button text and gui_mission object
class Pop_up:
    def __init__(self, master_, text_lbl_, text_btn_, object_) -> None:
        self.master = master_
        self.text_lbl = text_lbl_
        self.text_btn = text_btn_
        self.object = object_

        # header
        self.header_lbl = Label(self.master, text=self.text_lbl)
        self.header_lbl.pack(pady=2)

        # save popup: entry text defined
        self.entry1 = Entry(self.master)
        if(self.text_btn == "Save"):
            self.entry1.pack(pady=2)

        # load/remove popup: dropdown menu and variable defined
        self.selected_value = StringVar(self.master)
        self.selected_value.set("Select a saved mission") # default value
        if(self.text_btn == "Load" or self.text_btn == "Remove"):
            self.load_options = os.listdir("GUI/points_csv/saved_missions/") # reads all saved missions into dropdow menu
            self.dropdown = OptionMenu(self.master, self.selected_value, *self.load_options)
            self.dropdown.pack(pady=2)

        # manual controll popup: dropdown menu to select drone for manual flight
        # TODO: here self.load_options should be the drones currently selected
        self.selected_drone = StringVar(self.master)
        self.selected_drone.set("Select a drone") # default value
        if(self.text_btn == "Take control"):
            self.load_options = ["1"] #, "2", "3", "4"] # currently only drone 1 available for manual control
            self.dropdown = OptionMenu(self.master, self.selected_drone, *self.load_options)
            self.dropdown.pack(pady=2)

        # helix popup: create helix pattern
        if(self.text_btn == "Create Helix"):
            self.frame = Frame(self.master)
            self.entry2 = Entry(self.frame, width=7)
            self.entry3 = Entry(self.frame, width=7)
            self.lbl1 = Label(self.frame, text="Radius:")
            self.lbl2 = Label(self.frame, text="Height")

            self.lbl1.grid(row=1, column=1, pady=2)
            self.lbl2.grid(row=2, column=1, pady=2)
            self.entry2.grid(row=1, column=2, pady=2)
            self.entry3.grid(row=2, column=2,pady=2)
            self.frame.pack()

        # Circle popup: create circle pattern
        if(self.text_btn == "Create Circle"):
            self.frame = Frame(self.master)
            self.entry4 = Entry(self.frame, width=7)
            self.lbl3 = Label(self.frame, text="Radius:")

            self.lbl3.grid(row=1, column=1, pady=2)
            self.entry4.grid(row=1, column=2, pady=2)
            self.frame.pack()
        
        # Obstacle popup: Create an obstacle and load in existing obstacles   
        if(self.text_btn == "Create Obstacle"):
            self.frame = Frame(self.master)

            Label(self.frame, text = "Obstacles ", font=("Arial", 12)).grid(column=0, row=0)

            # Create A Main Frame
            self.mission_frame = Frame(self.frame, height=150, width=250)
            self.mission_frame.grid(column=0, row=2)
            
            # Create A Canvas
            self.canvas = Canvas(self.mission_frame, height=150, width=350)
            self.canvas.grid(column=0, row=1, columnspan=3)

            # Add A Scrollbar To The Canvas
            self.scroll = ttk.Scrollbar(self.mission_frame, orient=VERTICAL, command=self.canvas.yview)
            self.scroll.grid(column=4, row=0, rowspan=8, sticky=N+S+E)

            # Configure The Canvas
            self.canvas.configure(yscrollcommand=self.scroll.set)
            self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all")))

            self.obstacle_frame = Frame(self.canvas)

            # add that new frame to a window in the canvas
            self.canvas.create_window((0,0), window=self.obstacle_frame, anchor="nw")

            # add obstacle rows to obstacle frame by loading in already exising obstacle
            self.obs_entry_lst = []

            file_obs = "crazyswarm/ros_ws/src/crazyswarm/scripts/pycrazyswarm/visualizer/obstacles.csv"
            i = 0
            with open(file_obs, 'r') as file:
                reader = csv.reader(file, skipinitialspace=True)
                for row in reader:
                    self.obs_entry_lst.append(Obstacle_point(self.obstacle_frame,i))
                    self.obs_entry_lst[i].set_coord(row)
                    i+=1
            # always add empty row
            self.obs_entry_lst.append(Obstacle_point(self.obstacle_frame,i))

            # add buttons to manipulate these obstacles
            Button(self.mission_frame, text = "Add entry",command=self.add_entry).grid(column=0, row=1111)
            Button(self.mission_frame, text = "Delete last",command=self.delete_entry).grid(column=1, row=1111)
            Button(self.mission_frame, text=self.text_btn, command=self.button_clicked).grid(column=2, row=1111)
            self.frame.pack()


    # determine what function to call when button is pressed
    # input: -
    # output: -
    def button_clicked(self):
        if(self.text_btn == "Save"):
            self.save_mission()
        elif(self.text_btn == "Load"):
            self.load_mission()
        elif(self.text_btn == "Remove"):
            self.remove_save()
        elif(self.text_btn == "Take control"):
            self.manual_ctrl()
        elif(self.text_btn == "Create Helix"):
            self.create_helix()
        elif(self.text_btn == "Create Circle"):
            self.create_circle()
        elif(self.text_btn == "Create Obstacle"):
            self.create_obstacle()
        self.close_popup()


    # function to update scrollbar when obstacles are added/removed
    # input: -
    # output: -
    def updateScrollRegion(self):
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.obstacle_frame.bbox())

    # adds a new obstacle
    # input: -
    # output: -
    def add_entry(self):
        self.obs_entry_lst.append(Obstacle_point(self.obstacle_frame,len(self.obs_entry_lst)))
        self.updateScrollRegion()

    # deletes the last obstacle in the list and detroy it properly
    # input: -
    # output: -
    def delete_entry(self):
        if(len(self.obs_entry_lst) > 1):
            last_row = self.obs_entry_lst.pop()
            last_row.x.destroy()
            last_row.y.destroy()
            last_row.z.destroy()
            last_row.h.destroy()
            last_row.w.destroy()
            last_row.d.destroy()
            
        self.updateScrollRegion()

    # runs the command to save the file
    # input: -
    # output: -
    def save_mission(self):
        new_folder = self.entry1.get() # get name of new save

        # if no name was entered
        if(new_folder == ""):
            print("Please enter a name for the save")
            return

        # set path and create a folder for new save
        path = "GUI/points_csv/saved_missions/" + new_folder 

        # if save already exists then overwrite save, otherwise create folder for save
        if(not os.path.isdir(path)):
            os.system("mkdir "+path)
        else:
            print("Overwriting save named: " + new_folder)

        # call gui_mission function for it to save all waypoints to path
        self.object.save_all_mission_points(path)

    # runs the command to place saved waypoint csv files into points_csv
    # then call gui_drone_tabs to display waypoint info
    # input: -
    # output: -
    def load_mission(self):
        # remove current wypoints.csv files
        files = glob.glob('GUI/points_csv/*')
        for f in files:
            if(not os.path.isdir(f)):   # remove everything not being a folder
                os.remove(f)

        # read which save to read from
        folder = self.selected_value.get()
        if(folder == "Select a saved mission"): #check so default value hasn't been selected
            print("Cannot open this save")
            return
        path = "GUI/points_csv/saved_missions/"+folder+"/"

        # check so the correct drones are selected for the mission
        waypoint_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        drone_tabs = self.object.get_active_tabs()
        tmp = []
        for file in waypoint_files:
            if('waypoints.csv' in file):
                tmp.insert(0,file.replace('drone', '').replace('waypoints.csv',''))

        # if lists don't match, then show new pop-up and do nothing
        # TODO: the lists shouldn't have to be exactly the same,
        #       they should for example be allowed to be in mixed order
        if(not tmp == drone_tabs):
            pop_up_window = Tk()
            pop_up_window.title("Load mission")
            pop_up_window.geometry("350x100")
            Pop_up(pop_up_window, "The correct drones haven't been selected. \nPlease select drones "+str(tmp)+".", "Ok", None)
            return

        # copy files from this folder to points_csv
        for file in os.listdir(path):
            if(os.path.isfile(path+file)):
                copyfile(path+file, path+"../../"+file)

        # call gui_mission instance to make gui_drone_tabs show the info
        self.object.load_mission_points()

    # removes saved mission 
    # input: - 
    # output: -
    def remove_save(self):
        folder = self.selected_value.get()
        if(folder == "Select a saved mission"): #check so default value hasn't been selected
            print("Cannot remove this save")
            return

        # remove folder and containing files
        path = "GUI/points_csv/saved_missions/"
        for file in os.listdir(path+folder):
            if os.path.isfile(path+folder+"/"+file):
                os.unlink(path+folder+"/"+file)
        if os.path.isdir(path+folder):
            rmtree(path+folder)

        print("Removed: "+str(folder))

    # enables manual controll of a drone
    # input: -
    # output: -
    def manual_ctrl(self):
        drone = self.selected_drone.get()

        # call gui_mission instance to ennable manual control
        self.object.manual_ctrl_activated(drone)

    # creates waypoints for a helix
    def create_helix(self):
        points_per_height = 15
        radius = float(self.entry2.get()) # read user input
        height = float(self.entry3.get())
        
        start_coord = self.object.drone_tabs[0].start_coord
        waypoints = Patterns().helix(radius, height, start_coord, points_per_height)   # create waypoints

        # save waypoints and save to csv file
        self.object.drone_tabs[0].save_csv_file(waypoints)
        self.object.drone_tabs[0].display_loaded_mission()

    # creates waypoints for a circle
    def create_circle(self):
        radius = float(self.entry4.get())
        start_coord = self.object.drone_tabs[0].start_coord
        waypoints = Patterns().circle(radius, 15, start_coord, 10)

        # save waypoints and save to csv file
        self.object.drone_tabs[0].save_csv_file(waypoints)
        self.object.drone_tabs[0].display_loaded_mission()
    
    # creates obstacle/obstacles for rrt
    def create_obstacle(self):
        data = []
        for entry in self.obs_entry_lst:
            if(entry.check_obstacle()):
                value = entry.get_obstacle()
                data.append(value)

        file_obs = "crazyswarm/ros_ws/src/crazyswarm/scripts/pycrazyswarm/visualizer/obstacles.csv"
        with open(file_obs, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

    # close pop-up window
    def close_popup(self):
        self.master.destroy()
