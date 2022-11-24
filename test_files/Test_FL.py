import numpy as np
from scipy.optimize import minimize
import csv
import matplotlib.pyplot as plt
import math

if __name__ == "__main__":
    file = open('test23.csv')
    csv_reader = csv.reader(file)
    cf1_pos = []
    cf2_pos = []
    

    for row in csv_reader:
        points = [float(row[0]), float(row[1]), float(row[2])]
        cf1_pos.append(points)
        points = [float(row[0]), float(row[1]), float(row[2])]
        cf2_pos.append(points)

    list_len = len(cf1_pos)
    i = 1

    cf1x_plot_list = []
    cf1y_plot_list = []
    cf2x_plot_list = [0]
    cf2y_plot_list = [0]

    
    
    while i < list_len-2:
        cf1x = cf1_pos[i][0]
        cf1y = cf1_pos[i][1]
        cf2x = cf2_pos[i][0]
        cf2y = cf2_pos[i][1]
        cf1x_plot_list.append(cf1x)
        cf1y_plot_list.append(cf1y)
        
        Dis = math.dist(cf1_pos[i],cf2_pos[i])
        Safe_dist = 0.5
        print(Dis)

        if(Dis > Safe_dist):
            cf2x_plot_list.append(cf1x)
            cf2y_plot_list.append(cf1y)
              
        else:
            cf2x_plot_list.append(cf2x_plot_list[i-1])
            cf2y_plot_list.append(cf2y_plot_list[i-1])
            cf2_pos[i+1][0] = cf2x_plot_list[i-1]
            cf2_pos[i+1][1] = cf2y_plot_list[i-1]
            # PLx = cf1_pos[i][0] - cf1_pos[i-1][0]
            # PLy = cf1_pos[i][1] - cf1_pos[i-1][1]
            # if(np.abs(PLx) >= np.abs(PLy)):
            #     if(PLx >= 0):

            #         cf2x_plot_list.append(cf1x - Safe_dist)
            #         cf2y_plot_list.append(cf1y) 
            #         cf2_pos[i+1][0] = cf1x - Safe_dist
            #         cf2_pos[i+1][1] = cf1y
            #     else:  
            #         cf2x_plot_list.append(cf1x + Safe_dist)
            #         cf2y_plot_list.append(cf1y) 
            #         cf2_pos[i+1][0] = cf1x + Safe_dist
            #         cf2_pos[i+1][1] = cf1y
            # else:  
            #     if(PLy >= 0):

            #         cf2x_plot_list.append(cf1x)
            #         cf2y_plot_list.append(cf1y - Safe_dist) 
            #         cf2_pos[i+1][0] = cf1x
            #         cf2_pos[i+1][1] = cf1y - Safe_dist
            #     else:  
            #         cf2x_plot_list.append(cf1x)
            #         cf2y_plot_list.append(cf1y + Safe_dist) 
            #         cf2_pos[i+1][0] = cf1x
            #         cf2_pos[i+1][1] = cf1y + Safe_dist

        i = i + 1
    
    
    fig, ax = plt.subplots()
    ax.plot(cf1x_plot_list, cf1y_plot_list, label = "cf1")
    ax.plot(cf2x_plot_list, cf2y_plot_list, label = "cf2")
    ax.legend()
    plt.show()