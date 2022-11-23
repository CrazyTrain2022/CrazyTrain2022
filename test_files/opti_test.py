import numpy as np
from scipy.optimize import minimize
import csv
import matplotlib.pyplot as plt

#def cost_fun(cf2_goal_pos, cf1_pos, d1, d2):
    #return np.sqrt((cf1_pos[0] - cf2_goal_pos[0] + d1)^2 + (cf1_pos[1] - cf2_goal_pos[1] + d2)^2)

def cost_fun(cf2, cf1x, cf1y, d1, d2):
    fun1 = (cf1x - cf2[0] + d1)**2 + (cf1y - cf2[1] + d2)**2
    fun = np.sqrt(fun1)
    return fun

if __name__ == "__main__":
    file = open('test18.csv')
    csv_reader = csv.reader(file)
    cf1_pos = []
    cf2_pos = []
    

    for row in csv_reader:
        points = [float(row[0]), float(row[1]), float(row[2])]
        cf1_pos.append(points)
        points = [float(row[0])+0.5, float(row[1])-0.5, float(row[2])]
        cf2_pos.append(points)

    list_len = len(cf1_pos)
    i = 0
    print(cf1_pos)

    cf1x_plot_list = []
    cf1y_plot_list = []
    cf2x_plot_list = []
    cf2y_plot_list = []
    
    while i < list_len:
        cf1x = cf2_pos[i][0]
        cf1y = cf1_pos[i][1]
        cf2x = cf2_pos[i][0]
        cf2y = cf2_pos[i][1]
        d1 = 0.5
        d2 = 0.5
        
        opti_pos = minimize(fun = cost_fun, x0 = [cf2x, cf2y], args = (cf1x, cf1y, d1, d2))
        cf2x_op = opti_pos.x[0]    
        cf2y_op = opti_pos.x[1]

        cf1x_plot_list.append(cf1x)
        cf1y_plot_list.append(cf1y)
        cf2x_plot_list.append(cf2x_op)
        cf2y_plot_list.append(cf2y_op)
        i = i + 1
    
    fig, ax = plt.subplots()
    ax.plot(cf1x_plot_list, cf1y_plot_list, label = "cf1")
    ax.plot(cf2x_plot_list, cf2y_plot_list, label = "cf2")
    ax.legend()
    plt.show()
    