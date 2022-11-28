import do_mpc
import numpy as np
import math
from math import sqrt

#Controller for scenario: "Follow the leader"

def mpc_controller(
    model,
    goal,  
    debug_mode = False, 
    print_mpc_output = False, 
    n_horizon = 5, 
    t_step = 0.1
    ):


    #Setup controller
    mpc = do_mpc.controller.MPC(model)


    setup_mpc = {
        'n_horizon': n_horizon,
        't_step': t_step,
        #'n_robust': 1,z_2_dot-z_1_dot
        'store_full_solution': False,
    }

    mpc.set_param(**setup_mpc)

    if not print_mpc_output:
        surpress_ipopt = {'ipopt.print_level':0, 'ipopt.sb': 'yes', 'print_time':0}
        mpc.set_param(nlpsol_opts = surpress_ipopt)

    if debug_mode:
        print("MPC Setup:")
        print('\n'.join(['{} = {!r}'.format(k, v) for k, v in setup_mpc.items()])) #Print contents of setup_mpc


    x_1_goal = goal[0]
    y_1_goal = goal[1]
    z_1_goal = goal[2]


    #Objective function 
    #Input States from model
    x_1 = model._x['x_1']
    y_1 = model._x['y_1']
    z_1 = model._x['z_1']
    v_x_1 = model._x['v_x_1']
    v_y_1 = model._x['v_y_1']
    v_z_1 = model._x['v_z_1']

    x_2 = model._x['x_2']
    y_2 = model._x['y_2']
    z_2 = model._x['z_2']
    v_x_2 = model._x['v_x_2']
    v_y_2 = model._x['v_y_2']
    v_z_2 = model._x['v_z_2']

    x_3 = model._x['x_3']
    y_3 = model._x['y_3']
    z_3 = model._x['z_3']
    v_x_3 = model._x['v_x_3']
    v_y_3 = model._x['v_y_3']
    v_z_3 = model._x['v_z_3']
    
    x_4 = model._x['x_4']
    y_4 = model._x['y_4']
    z_4 = model._x['z_4']
    v_x_4 = model._x['v_x_4']
    v_y_4 = model._x['v_y_4']
    v_z_4 = model._x['v_z_4']
    
    d_12 = model._x['d_12']
    d_23 = model._x['d_23']
    d_34 = model._x['d_34']
    d_24 = model._x['d_34']



    #weight constants
    q = [1000,1,1,1]


    meyer_term =    q[0]*( (x_1 - x_1_goal)**2 + (y_1 - y_1_goal)**2 + (z_1 - z_1_goal)**2 ) +\
                    q[1]*( (x_2 - x_1)**2 + (y_2 - y_1)**2 + (z_2 - z_1)**2 ) +\
                    q[2]*( (x_3 - x_2)**2 + (y_3 - y_2)**2 + (z_3 - z_2)**2 ) +\
                    q[3]*( (x_4 - x_3)**2 + (y_4 - y_3)**2 + (z_4 - z_3)**2 )

    lagrange_term = q[0]*( (x_1 - x_1_goal)**2 + (y_1 - y_1_goal)**2 + (z_1 - z_1_goal)**2 ) +\
                    q[1]*( (x_2 - x_1)**2 + (y_2 - y_1)**2 + (z_2 - z_1)**2 ) +\
                    q[2]*( (x_3 - x_2)**2 + (y_3 - y_2)**2 + (z_3 - z_2)**2 ) +\
                    q[3]*( (x_4 - x_3)**2 + (y_4 - y_3)**2 + (z_4 - z_3)**2 )

    mpc.set_objective(mterm=meyer_term, lterm=lagrange_term)

    u_lim = { #Penalty for control signals
        'pitch_1': 1,
        'roll_1': 1,
        'thrust_1': 1,

        'pitch_2': 1,
        'roll_2': 1,
        'thrust_2': 1,

        'pitch_3': 1,
        'roll_3': 1,
        'thrust_3': 1,

        'pitch_4': 1,
        'roll_4': 1,
        'thrust_4': 1,
    }
    mpc.set_rterm(**u_lim)

    if debug_mode:
        print("\nObjective function:")
        print("Limits of control signals:")
        print('\n'.join(['{} = {!r}'.format(k, v) for k, v in u_lim.items()])) #Print contents of u_lim




    # Constraints of the model: (TODO: Load from external configuration file?)
    room_x_min = -5
    room_x_max = 5
    room_y_min = -5
    room_y_max = 5
    room_z_min = 0
    room_z_max = 10
    v_min = -1
    v_max = 1
    d_min = 0.3
    d_max = 1
    pitch_min = -math.pi/4
    pitch_max = math.pi/4
    roll_min = -math.pi/4
    roll_max = math.pi/4
    thrust_min = -1    
    thrust_max = 1
    

    lower_limits_states = {# Lower bounds on states:
        'x_1': room_x_min,
        'y_1': room_y_min,
        'z_1': room_z_min,
        'v_x_1': v_min,
        'v_y_1': v_min,
        'v_z_1': v_min,

        'x_2': room_x_min,
        'y_2': room_y_min,
        'z_2': room_z_min,
        'v_x_2': v_min,
        'v_y_2': v_min,
        'v_z_2': v_min,

        'x_3': room_x_min,
        'y_3': room_y_min,
        'z_3': room_z_min,
        'v_x_3': v_min,
        'v_y_3': v_min,
        'v_z_3': v_min,

        'x_4': room_x_min,
        'y_4': room_y_min,
        'z_4': room_z_min,
        'v_x_4': v_min,
        'v_y_4': v_min,
        'v_z_4': v_min,

        'd_12': d_min,
        'd_23': d_min,
        'd_34': d_min,
        'd_13': 2*d_min,
        'd_14': 3*d_min,
        'd_24': 2*d_min,

    }

    lower_lim_val = list(lower_limits_states.values())
    lower_lim_var = list(lower_limits_states.keys())
    for i in range(len(lower_lim_var)):
        mpc.bounds['lower', '_x', lower_lim_var[i]] = lower_lim_val[i]


    
    upper_limits_states = {# Upper limits on states:
        'x_1': room_x_max,
        'y_1': room_y_max,
        'z_1': room_z_max,
        'v_x_1': v_max,
        'v_y_1': v_max,
        'v_z_1': v_max,

        'x_2': room_x_max,
        'y_2': room_y_max,
        'z_2': room_z_max,
        'v_x_2': v_max,
        'v_y_2': v_max,
        'v_z_2': v_max,

        'x_3': room_x_max,
        'y_3': room_y_max,
        'z_3': room_z_max,
        'v_x_3': v_max,
        'v_y_3': v_max,
        'v_z_3': v_max,

        'x_4': room_x_max,
        'y_4': room_y_max,
        'z_4': room_z_max,
        'v_x_4': v_max,
        'v_y_4': v_max,
        'v_z_4': v_max,

        'd_12': d_max,
        'd_23': d_max,
        'd_34': d_max,
        'd_13': 2*d_max,
        'd_14': 3*d_max,
        'd_24': 2*d_max,
    }

    upper_lim_val = list(upper_limits_states.values())
    upper_lim_var = list(upper_limits_states.keys())
    for i in range(len(upper_lim_var)):
        mpc.bounds['upper', '_x', upper_lim_var[i]] = upper_lim_val[i]

    
    
    
    lower_limits_inputs = {# Lower bounds on inputs (control signals):
        'pitch_1': pitch_min,
        'roll_1': roll_min,
        'thrust_1': thrust_min,

        'pitch_2': pitch_min,
        'roll_2': roll_min,
        'thrust_2': thrust_min,

        'pitch_3': pitch_min,
        'roll_3': roll_min,
        'thrust_3': thrust_min,

        'pitch_4': pitch_min,
        'roll_4': roll_min,
        'thrust_4': thrust_min,
    }

    lower_lim_val = list(lower_limits_inputs.values())
    lower_lim_var = list(lower_limits_inputs.keys())
    for i in range(len(lower_lim_var)):
        mpc.bounds['lower', '_u', lower_lim_var[i]] = lower_lim_val[i]

    
    

    upper_limits_inputs = {# Upper limits on inputs (control signals):
        'pitch_1': pitch_max,
        'roll_1': roll_max,
        'thrust_1': thrust_max,

        'pitch_2': pitch_max,
        'roll_2': roll_max,
        'thrust_2': thrust_max,

        'pitch_3': pitch_max,
        'roll_3': roll_max,
        'thrust_3': thrust_max,

        'pitch_4': pitch_max,
        'roll_4': roll_max,
        'thrust_4': thrust_max,
    }

    upper_lim_val = list(upper_limits_inputs.values())
    upper_lim_var = list(upper_limits_inputs.keys())
    for i in range(len(upper_lim_var)):
        mpc.bounds['upper', '_u', upper_lim_var[i]] = upper_lim_val[i]



    if debug_mode:
        print("\nLower Limits of states:")
        print('\n'.join(['{} = {!r}'.format(k, v) for k, v in lower_limits_states.items()]))
        print("\nUpper Limits of states:") 
        print('\n'.join(['{} = {!r}'.format(k, v) for k, v in upper_limits_states.items()])) 
        print("\nLower Limits of inputs:")
        print('\n'.join(['{} = {!r}'.format(k, v) for k, v in lower_limits_inputs.items()])) 
        print("\nUpper Limits of inputs:")
        print('\n'.join(['{} = {!r}'.format(k, v) for k, v in upper_limits_inputs.items()])) 


    
    mpc.setup()

    return(mpc)
    #END OF FUNCTION