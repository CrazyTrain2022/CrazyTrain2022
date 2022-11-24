import numpy as np
from scipy.optimize import minimize
import csv
import matplotlib.pyplot as plt
import math

if __name__ == "__main__":
    file = open('test23.csv')
    csv_reader = csv.reader(file)
    cf1_pos = []
    #cf2_pos = []
    

    for row in csv_reader:
        points = [float(row[0]), float(row[1]), float(row[2])]
        cf1_pos.append(points)
        #points = [float(row[0])+0.5, float(row[1])-0.5, float(row[2])]
        #cf2_pos.append(points)

    list_len = len(cf1_pos)
    i = 0
    print(cf1_pos)

    cf1x_plot_list = []
    cf1y_plot_list = []
    cf2x_plot_list = [0,0,0,0]
    cf2y_plot_list = [0.5,0.5,0.5,0.5]
    
    while i < list_len:
        cf1x = cf1_pos[i][0]
        cf1y = cf1_pos[i][1]
        
        Disx = math.dist(cf2x_plot_list[i],cf1x)
        Disy = math.dist(cf2y_plot_list[i],cf1y)
        Safe_dist = 0.5

        if(Disx > Safe_dist and Disy > Safe_dist):
            cf2x_plot_list.append(cf1_pos[i][0])
            cf2y_plot_list.append(cf1_pos[i][1])  
        else:
            cf2x_plot_list.append(cf2x_plot_list[i])
            cf2y_plot_list.append(cf2y_plot_list[i])  
        
        """
        opti_pos = minimize(fun = cost_fun, x0 = [cf2x, cf2y], args = (cf1x, cf1y, d1, d2))
        cf2x_op = opti_pos.x[0]    
        cf2y_op = opti_pos.x[1]
        """
        # cf2x_plot_list.append(cf2x_op)
        # cf2y_plot_list.append(cf2y_op)
        i = i + 1
    
    fig, ax = plt.subplots()
    ax.plot(cf1x_plot_list, cf1y_plot_list, label = "cf1")
    ax.plot(cf2x_plot_list, cf2y_plot_list, label = "cf2")
    ax.legend()
    plt.show()