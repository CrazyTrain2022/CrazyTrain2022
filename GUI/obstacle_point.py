#File for class to handle obstacles

from tkinter import *
from tkinter import ttk
import tkinter as tk



class Obstacle_point:
    def __init__(self, master_, number_) -> None:
        self.master = master_
        self.number = number_

        # create and place entries for obstacles
        self.x = Entry(self.master, width=5)
        self.x.grid(column=1, row=self.number, padx=5, pady=1)
        self.y = Entry(self.master, width=5)
        self.y.grid(column=2, row=self.number, padx=5, pady=1)
        self.z = Entry(self.master, width=5)
        self.z.grid(column=3, row=self.number, padx=5, pady=1)
        self.h = Entry(self.master, width=5)
        self.h.grid(column=4, row=self.number, padx=5, pady=1)
        self.w = Entry(self.master, width=5)
        self.w.grid(column=5, row=self.number, padx=5, pady=1)
        self.d = Entry(self.master, width=5)
        self.d.grid(column=6, row=self.number, padx=5, pady=1)


    # getters for obstacle coordinates
    def get_x(self):
        return self.x.get()

    def get_y(self):
        return self.y.get()

    def get_z(self):
        return self.z.get()

    def get_h(self):
        return self.h.get()

    def get_w(self):
        return self.w.get()

    def get_d(self):
        return self.d.get()


    # input: [string lst]
    # output: -
    def set_coord(self, coord):
        self.x.delete(0,END)
        self.x.insert(0,float(coord[0]))
        self.y.delete(0,END)
        self.y.insert(0,float(coord[1]))
        self.z.delete(0,END)
        self.z.insert(0,float(coord[2]))
        self.h.delete(0,END)
        self.h.insert(0,float(coord[3]))
        self.w.delete(0,END)
        self.w.insert(0,float(coord[4]))
        self.d.delete(0,END)
        self.d.insert(0,float(coord[5]))

        x = self.x.get()
        y = self.y.get()
        z = self.z.get()
        h = self.h.get()
        w = self.w.get()
        d = self.d.get()
        return [float(x), float(y), float(z), float(h), float(w), float(d)]

    #Check if actually obstacle or empty row
    def check_obstacle(self):
        x = self.x.get()
        if(x != ''):
            return True
        else:
            return False