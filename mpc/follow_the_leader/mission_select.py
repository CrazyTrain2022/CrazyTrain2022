import numpy as np
import math


def mission_selection(mission_name = "unspecified"):
    goals = []
    break_dist = 1e-1
    illegal_name = True
  
    if mission_name.lower() == "custom" or mission_name.lower() == "original" or mission_name.lower() == "custom":
        illegal_name = False
        
    while illegal_name:
        print("\nAvailable missions:")
        print("Spiral -- Spiral mission will make a helix of five revolutions. Warning: Time consuming mission.")
        print("Original -- Short original mission.")
        print("Custom -- Create custom mission.")
        mission_name = input("Mission name: ")
        
        if mission_name.lower() == "spiral" or mission_name.lower() == "original" or mission_name.lower() == "custom":
            illegal_name = False                    
        else:
            print("Invalid input or mission name. Try again.")            
    #end while


    if mission_name.lower() == "spiral":
        break_dist = 1e-1        
        num_points = 100
        for i in range(num_points):
            z =  1 + (5/num_points)*i
            x = 3 * np.sin(math.pi/10*i)
            y = 3 * np.cos(math.pi/10*i)
            goals.append(np.array([x,y,z]))
        
        #goals = np.array(goals, dtype=object) #Correct format
        

    elif mission_name.lower() == "original":
        break_dist = 1e-2
        sequence = [
        (0, 0, 7/10),
        (2/10, 2/10, 7/10),
        (2/10, -2/10, 9/10),
        (-2/10, 2/10, 5/10),
        (-2/10, -2/10, 7/10),
        (0, 0, 7/10),
        (0, 0, 2/10),
        ]
        for k in sequence:
            goals.append(np.array(k))

        #goals = np.array(goals, dtype=object) #Correct format


    elif mission_name.lower() == "custom":
        more_goals = True
        add_goal = True
        set_break_dist = True

        print("Create custom mission:")
        while more_goals:
            while add_goal:
                try:
                    x,y,z = input("Goal %d x,y,z: " %(len(goals)+1)).split(',')
                    float(x)
                    float(y)
                    float(z)
                    if float(x) > 5 or float(x) < -5 or float(y) > 5 or float(y) < -5 or float(z) > 10 or float(z) < 0:
                        if float(x) < -5 or float(x) > 5:
                            print("x range [-5,5]")
                        if float(y) < -5 or float(y) > 5:
                            print("y range [-5,5]")
                        if float(z) < 0 or float(z) > 10:
                            print("z range [0,10]")
                        print("Try again.")
                        continue
                    #end if
                except ValueError:
                    print("Wrong format. Try again.")
                    
                else:
                    goals.append(np.array([float(x),float(y),float(z)]))
                    add_goal = False

            var = input("Add more goals (yes/no): ")

            if var.lower() == "yes" or var.lower() == "y":
                add_goal = True
            elif var.lower() == "no" or var.lower() == "n":
                more_goals = False
            else:
                print("Invalid input. Try again.")
            
        #end while

        while set_break_dist:
            break_dist = input("Set break_dist (break_dist > 0, normally 1e-1): ")
            try:
                float(break_dist)
            except ValueError:
                print("Invalid input. Try again.")
            else:
                break_dist = float(break_dist)
                if break_dist > 0:                    
                    set_break_dist = False
                else:
                    print("break_dist can not be 0 or lower. Try another number.")
            
        #end while                   

            
    goals = np.array(goals, dtype=object) #Correct format
    return goals, break_dist