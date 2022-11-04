import sys
import numpy as np
import matplotlib.pyplot as plt
import argparse
from patterns import Pattern_obj

if __name__ == "__main__":
    # Parse input from terminal

    parser = argparse.ArgumentParser(description="Create waypoints for a specified number of drones according to a pattern.\
        \n Specify: Number of drones, mirroring, pattern, arguments for the selected pattern, replication-mirroring settings.",
        epilog="For helix the arguments are: radius, height, increasing radius (0 for inactivate and 1 for activate),\
            center (x,y,z), number of waypoints\n \For the circle the arguments are: radius, height, center (x,y,z),\
            number of waypoints\n For the line the arguments are: startpoint (x,y,z), endpoint (x,y,z), \
            number of waypoints.\nIf the mirroring is set to replication, there are three additional arguments:\
            distance between replicated drones, formation (x,y)."
        ,formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("nbr_of_drones", type=int, help="Number of drones")
    parser.add_argument("mirroring", type=str,help="Select mirroring option", choices=['circular', 'linear', 'replicate'])
    parser.add_argument("pattern", type=str, help="Select a pattern", choices=['helix', 'circle','line'])
    parser.add_argument("arg", nargs='*', type=float, help="Arguments for the selected pattern and replication-settings.")
    args = parser.parse_args()
    
    original_waypoints = [] 
    if args.pattern == 'helix':
        original_waypoints = Pattern_obj.helix(args.arg[0], args.arg[1], args.arg[2],[args.arg[3], args.arg[4]], args.arg[5]) 
    elif args.pattern == 'circle':
        original_waypoints = Pattern_obj.circle(args.arg[0], args.arg[1], [args.arg[2], args.arg[3]], args.arg[4])
    elif args.pattern == 'line':
        original_waypoints = Pattern_obj.line([args.arg[0], args.arg[1], args.arg[2]],[args.arg[3], args.arg[4], args.arg[5]], args.arg[6])
    
    nbr_of_drones = args.nbr_of_drones 
    shape = np.shape(original_waypoints)
    x_shape = shape[0]
    y_shape = shape[1]
    waypoints_array = np.zeros([x_shape,y_shape,nbr_of_drones])
    
    # Plot the results of the mirroring if wanted
    #fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')

    #circular mirroring
    
    if args.mirroring=='circular':
        theta = 2*np.pi / nbr_of_drones
        for drone in range(nbr_of_drones):
            temp_waypoints = np.zeros(np.shape(original_waypoints))

            for i in range(len(original_waypoints)):
                temp_waypoints[i][0] = original_waypoints[i][0]*np.cos(drone*theta) - original_waypoints[i][1]*np.sin(drone*theta)
                temp_waypoints[i][1] = original_waypoints[i][1]*np.cos(drone*theta) + original_waypoints[i][0]*np.sin(drone*theta)
                temp_waypoints[i][2] = original_waypoints[i][2]

            waypoints_array[:,:,drone] = temp_waypoints

            # Plot the result if wanted
            #ax.plot(waypoints_array[:,0,drone], waypoints_array[:,1,drone], waypoints_array[:,2,drone])
            #ax.set_xlabel('x')
            #ax.set_ylabel('y')
            #ax.set_zlabel('z')
            np.savetxt('drone'+str(drone+1)+'waypoints.csv', X=waypoints_array[:,:,drone], delimiter=',', fmt='%10.5f')
    
    # linear mirroring

    elif args.mirroring=='linear':
        signx=1
        signy=1
        if nbr_of_drones>4:
            sys.exit("ERROR! Make sure that number of drones are maximum 4.")
        
        for drone in range(nbr_of_drones):
            temp_waypoints = np.zeros(np.shape(original_waypoints))

            for i in range(len(original_waypoints)):
                temp_waypoints[i][0] = signx*original_waypoints[i][0]
                temp_waypoints[i][1] = signy*original_waypoints[i][1]
                temp_waypoints[i][2] = original_waypoints[i][2]
                
                #check if outside quadrant
                crit_dist = 0.2
                if not(original_waypoints[0][0] >crit_dist and original_waypoints[i][0] >crit_dist or \
                    original_waypoints[0][1] < -crit_dist and original_waypoints[i][1]<-crit_dist):
                    sys.exit("ERROR! Make sure that the settings are such that the drone stays within \
                        it's quadrant and %s away from the axes." %crit_dist)
            if temp_waypoints[drone][0] <0:
                signy=-1
            else:
                signy=1
            if temp_waypoints[drone][1] >0:
                signx=-1
            else:
                signx=1

            waypoints_array[:,:,drone] = temp_waypoints

            # Plot the result if wanted
            #ax.plot(waypoints_array[:,0,drone], waypoints_array[:,1,drone], waypoints_array[:,2,drone])
            #ax.set_xlabel('x')
            #ax.set_ylabel('y')
            #ax.set_zlabel('z')
            np.savetxt('drone'+str(drone+1)+'waypoints.csv', X=waypoints_array[:,:,drone], delimiter=',', fmt='%10.5f')
    
    # replicative mirroring

    elif args.mirroring=='replicate':
        dist = int(args.arg[-3])
        nbr_xdir = int(args.arg[-2])
        nbr_ydir = int(args.arg[-1])
        if nbr_xdir*nbr_ydir < nbr_of_drones:
            sys.exit("ERROR! Make sure that number of drones in x-dir and y-dir are less than or equal number of drones in total.")
        
        formation = [[k,i] for k in range(nbr_xdir) for i in range(nbr_ydir)]
        for drone in range(nbr_of_drones):
            temp_waypoints = np.zeros(np.shape(original_waypoints))

            for i in range(len(original_waypoints)):
                temp_waypoints[i][0] = original_waypoints[i][0] + dist*formation[drone][0]
                temp_waypoints[i][1] = original_waypoints[i][1] + dist*formation[drone][1]
                temp_waypoints[i][2] = original_waypoints[i][2]

            waypoints_array[:,:,drone] = temp_waypoints

            # Plot the result if wanted
            #ax.plot(waypoints_array[:,0,drone], waypoints_array[:,1,drone], waypoints_array[:,2,drone])
            #ax.set_xlabel('x')
            #ax.set_ylabel('y')
            #ax.set_zlabel('z')
            np.savetxt('drone'+str(drone+1)+'waypoints.csv', X=waypoints_array[:,:,drone], delimiter=',', fmt='%10.5f')
    plt.show()
