from mpc import mpc
from mpc_model import mpc_model
from mpc_controller import mpc_controller
from mpc_simulator import mpc_simulator
import numpy as np
import time
#from Mission_select import mission_selection


#Mission: Follow the leader
def mpc_main(
    x0 = np.array([0,0,0,0,0,0, 0,-1,0,0,0,0, 0,-2,0,0,0,0, 0,-3,0,0,0,0, 1,1,1,2,3,2]), #Initial states (x1,y1,z1,vx1,vy1,vz1, x2,...,vz4, d12,d23,d34,d13,d14,24)
    u0 = np.array([0,0,0, 0,0,0, 0,0,0, 0,0,0]), #Initial input  (roll_1,pitch_1,thrust_1,roll_2,...,)
    goals = np.array([0,0,0]), 
    break_dist = 1e-2,
    print_goal_number = False,
    print_goal_position = False,
    print_mpc_cycle_time = False,
    print_run_time = False,
    print_position = False,
    print_deviation = False
    ):    

    import numpy as np
    trajectory = np.array(x0)

    #trajectory = []
    #trajectory.append([x0[0], x0[1], x0[2], x0[6], x0[7], x0[8], x0[12], x0[13], x0[14], x0[18], x0[19], x0[20]])

    model = mpc_model()
    simulator = mpc_simulator(model)

    if print_run_time:
        time_start = time.time()

    goal_num = 0
    while goal_num < len(goals): #Mission loop
        controller = mpc_controller(model, goals[goal_num])

        if print_goal_number:
            print('Goal', goal_num + 1, "out of", len(goals)) 
        if print_goal_position:
            print("Goal (x,y,z) = (%3.3f, %3.3f, %3.3f)" %(goals[goal_num,0], goals[goal_num,1], goals[goal_num,2]))

        while (abs(x0[0] - goals[goal_num,0]) > break_dist) or (abs(x0[1] - goals[goal_num,1]) > break_dist) or (abs(x0[2] - goals[goal_num,2]) > break_dist):
            if print_mpc_cycle_time:
                t_start = time.time()

            u0, x0 = mpc(controller, simulator, x0, u0)

            if print_mpc_cycle_time:
                t_end = time.time()

            #trajectory.append([x0[0], x0[1], x0[2], x0[6], x0[7], x0[8], x0[12], x0[13], x0[14], x0[18], x0[19], x0[20]])
            trajectory = np.vstack((trajectory, x0))

            if print_mpc_cycle_time:
                print("Mpc cycle time: ", t_end - t_start) 

            if print_position:
                print("(x1,y1,z1) = (%3.3f, %3.3f, %3.3f)" %(x0[0], x0[1], x0[2]))
                print("(x2,y2,z2) = (%3.3f, %3.3f, %3.3f)" %(x0[6], x0[7], x0[8]))
                print("(x3,y3,z3) = (%3.3f, %3.3f, %3.3f)" %(x0[12], x0[13], x0[14]))
                print("(x4,y4,z4) = (%3.3f, %3.3f, %3.3f)" %(x0[18], x0[19], x0[20]))

            if print_deviation:
                print("x_diff: ", abs(x0[0] - goals[goal_num,0]))
                print("y_diff: ", abs(x0[1] - goals[goal_num,1]))
                print("z_diff: ", abs(x0[2] - goals[goal_num,2]))

        goal_num += 1   

    
    if print_run_time:
        time_end = time.time()
        print("Total runtime: ", time_end - time_start)
    
    if trajectory.ndim == 1: #in case of goal is close enough to starting point
        trajectory = trajectory.reshape(1, trajectory.shape[0]) #Ensure correct shape (matrix)
        print("WARNING: GOAL POINT MAY BE WITHIN REACH OF START POINT AT START.")

    return trajectory #numpy array with [x1,y1,z1,x2,y2,z2,x3,y3,z3,x4,y4,z4]
