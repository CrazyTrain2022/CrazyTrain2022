from tkinter import *
from tkinter import ttk
import tkinter as tk

import os
import glob
import sys

from gui_menu import Gui_menu
from gui_mission import Gui_mission

# Gui_app class is responsible for the GUI window
class Gui_app:
    def __init__(self, master) -> None:
  
        # Instantiating toplevel window
        self.master = master
        panedwindow = ttk.Panedwindow(master, orient=HORIZONTAL)

        # create frames and display
        pane_mission = LabelFrame(panedwindow, width=380, height=500, relief=SUNKEN)
        panedwindow.add(pane_mission, weight=2)
        panedwindow.pack(fill=BOTH, expand=True)

        # create mission class, filling the mission frame
        self.gui_mission = Gui_mission(pane_mission)

        # create menu
        Gui_menu(master, self.gui_mission)

    # when destroyed, remove all unsaved points_csv files, but leaves the folders with saved missions
    def __del__(self):
        print("Crazycrowd - GUI is being closed. Removing all unsaved waypoints- and trajectory-csv files")

        # delete waypoint csv files
        files = glob.glob('GUI/points_csv/*')
        for f in files:
            if(not os.path.isdir(f)):   # remove everything not being a folder
                os.remove(f)


# main function
if __name__ == "__main__":
    # input flags
    flags = sys.argv[1:]

    # window setup
    window = Tk()
    window.title("Crazytrain - GUI")
    window.geometry("400x600")

    # fullscreen if flag from user
    if("--fullscreen" in flags):
        width= window.winfo_screenwidth()               
        height= window.winfo_screenheight()               
        window.geometry("%dx%d" % (width, height))

    # Calling our App
    app = Gui_app(window)
  
    # Mainloop runs the window until closed
    window.mainloop()