import do_mpc
import math

#Scenario: Follow the leader for four drones

def mpc_model(debug_mode = False):
    #Setup of variables and input
    model_type = 'continuous' # either 'discrete' or 'continuous'
    model = do_mpc.model.Model(model_type)

    # States of the model
    # Drone 1
    x_1 = model.set_variable(var_type='_x', var_name='x_1') #[x]   #'_x' = 'states'
    y_1 = model.set_variable(var_type='_x', var_name='y_1') #[y]
    z_1 = model.set_variable(var_type='_x', var_name='z_1') #[z]
    v_x_1 = model.set_variable(var_type='_x', var_name='v_x_1')
    v_y_1 = model.set_variable(var_type='_x', var_name='v_y_1')
    v_z_1 = model.set_variable(var_type='_x', var_name='v_z_1')

    #Drone 2
    x_2 = model.set_variable(var_type='_x', var_name='x_2') #[x]   #'_x' = 'states'
    y_2 = model.set_variable(var_type='_x', var_name='y_2') #[y]
    z_2 = model.set_variable(var_type='_x', var_name='z_2') #[z]
    v_x_2 = model.set_variable(var_type='_x', var_name='v_x_2')
    v_y_2 = model.set_variable(var_type='_x', var_name='v_y_2')
    v_z_2 = model.set_variable(var_type='_x', var_name='v_z_2')

    #Drone 3
    x_3 = model.set_variable(var_type='_x', var_name='x_3') #[x]   #'_x' = 'states'
    y_3 = model.set_variable(var_type='_x', var_name='y_3') #[y]
    z_3 = model.set_variable(var_type='_x', var_name='z_3') #[z]
    v_x_3 = model.set_variable(var_type='_x', var_name='v_x_3')
    v_y_3 = model.set_variable(var_type='_x', var_name='v_y_3')
    v_z_3 = model.set_variable(var_type='_x', var_name='v_z_3')
   
    #Drone 4
    x_4 = model.set_variable(var_type='_x', var_name='x_4') #[x]   #'_x' = 'states'
    y_4 = model.set_variable(var_type='_x', var_name='y_4') #[y]
    z_4 = model.set_variable(var_type='_x', var_name='z_4') #[z]
    v_x_4 = model.set_variable(var_type='_x', var_name='v_x_4')
    v_y_4 = model.set_variable(var_type='_x', var_name='v_y_4')
    v_z_4 = model.set_variable(var_type='_x', var_name='v_z_4')

    #Distance between drones
    d_12 = model.set_variable(var_type='_x', var_name='d_12')
    d_23 = model.set_variable(var_type='_x', var_name='d_23') 
    d_34 = model.set_variable(var_type='_x', var_name='d_34')
    d_13 = model.set_variable(var_type='_x', var_name='d_13')
    d_14 = model.set_variable(var_type='_x', var_name='d_14')
    d_24 = model.set_variable(var_type='_x', var_name='d_24')



    # Inputs of the model (set control signal):
    roll_1 = model.set_variable(var_type='_u',var_name='roll_1')    #'_u' = 'inputs'
    pitch_1 =  model.set_variable(var_type='_u',var_name='pitch_1')
    thrust_1 =  model.set_variable(var_type='_u',var_name='thrust_1')

    roll_2 = model.set_variable(var_type='_u',var_name='roll_2')    #'_u' = 'inputs'
    pitch_2 =  model.set_variable(var_type='_u',var_name='pitch_2')
    thrust_2 =  model.set_variable(var_type='_u',var_name='thrust_2')

    roll_3 = model.set_variable(var_type='_u',var_name='roll_3')    #'_u' = 'inputs'
    pitch_3 =  model.set_variable(var_type='_u',var_name='pitch_3')
    thrust_3 =  model.set_variable(var_type='_u',var_name='thrust_3')

    roll_4 = model.set_variable(var_type='_u',var_name='roll_4')    #'_u' = 'inputs'
    pitch_4 =  model.set_variable(var_type='_u',var_name='pitch_4')
    thrust_4 =  model.set_variable(var_type='_u',var_name='thrust_4')


    



    if debug_mode:
        print("States of model: ", model.x.keys(), "\n")
        print("Inputs of model: ", model.u.keys(), "\n")


    # Model used by MPC
    # Right hand side of equation
    # x_dot = f(x)

    g = 9.81 #gravity [ms^-2]
    m = 30e-3 #30 gram
    x_1_dot = v_x_1
    y_1_dot = v_y_1
    z_1_dot = v_z_1
    v_x_1_dot = -g * pitch_1
    v_y_1_dot = g * roll_1
    v_z_1_dot = -1/m * thrust_1 - g

    x_2_dot = v_x_2
    y_2_dot = v_y_2
    z_2_dot = v_z_2
    v_x_2_dot = -g * pitch_2
    v_y_2_dot = g * roll_2
    v_z_2_dot = -1/m * thrust_2 - g

    x_3_dot = v_x_3
    y_3_dot = v_y_3
    z_3_dot = v_z_3
    v_x_3_dot = -g * pitch_3
    v_y_3_dot = g * roll_3
    v_z_3_dot = -1/m * thrust_3 - g

    x_4_dot = v_x_4
    y_4_dot = v_y_4
    z_4_dot = v_z_4
    v_x_4_dot = -g * pitch_4
    v_y_4_dot = g * roll_4
    v_z_4_dot = -1/m * thrust_4 - g

    #time derivative of d_12, d_23, d_34
    d_12_dot = ( (x_2-x_1)**2 + (y_2-y_1)**2 + (z_2-z_1)**2 )**(-1/2) * ( (x_2-x_1)*(x_2_dot-x_1_dot) + (y_2-y_1)*(y_2_dot-y_1_dot) + (z_2-z_1)*(z_2_dot-z_1_dot) )
    d_23_dot = ( (x_3-x_2)**2 + (y_3-y_2)**2 + (z_3-z_2)**2 )**(-1/2) * ( (x_3-x_2)*(x_3_dot-x_2_dot) + (y_3-y_2)*(y_3_dot-y_2_dot) + (z_3-z_2)*(z_3_dot-z_2_dot) )
    d_34_dot = ( (x_4-x_3)**2 + (y_4-y_3)**2 + (z_4-z_3)**2 )**(-1/2) * ( (x_4-x_3)*(x_4_dot-x_3_dot) + (y_4-y_3)*(y_4_dot-y_3_dot) + (z_4-z_3)*(z_4_dot-z_3_dot) )
    d_13_dot = ( (x_3-x_1)**2 + (y_3-y_1)**2 + (z_3-z_1)**2 )**(-1/2) * ( (x_3-x_1)*(x_3_dot-x_1_dot) + (y_3-y_1)*(y_3_dot-y_1_dot) + (z_3-z_1)*(z_3_dot-z_1_dot) )
    d_14_dot = ( (x_4-x_1)**2 + (y_4-y_1)**2 + (z_4-z_1)**2 )**(-1/2) * ( (x_4-x_1)*(x_4_dot-x_1_dot) + (y_4-y_1)*(y_4_dot-y_1_dot) + (z_4-z_1)*(z_4_dot-z_1_dot) )
    d_24_dot = ( (x_4-x_2)**2 + (y_4-y_2)**2 + (z_4-z_2)**2 )**(-1/2) * ( (x_4-x_2)*(x_4_dot-x_2_dot) + (y_4-y_2)*(y_4_dot-y_2_dot) + (z_4-z_2)*(z_4_dot-z_2_dot) )


    model.set_rhs('x_1', x_1_dot)
    model.set_rhs('y_1', y_1_dot)
    model.set_rhs('z_1', z_1_dot)
    model.set_rhs('v_x_1', v_x_1_dot)
    model.set_rhs('v_y_1', v_y_1_dot)
    model.set_rhs('v_z_1', v_z_1_dot)

    model.set_rhs('x_2', x_2_dot)
    model.set_rhs('y_2', y_2_dot)
    model.set_rhs('z_2', z_2_dot)
    model.set_rhs('v_x_2', v_x_2_dot)
    model.set_rhs('v_y_2', v_y_2_dot)
    model.set_rhs('v_z_2', v_z_2_dot)

    model.set_rhs('x_3', x_3_dot)
    model.set_rhs('y_3', y_3_dot)
    model.set_rhs('z_3', z_3_dot)
    model.set_rhs('v_x_3', v_x_3_dot)
    model.set_rhs('v_y_3', v_y_3_dot)
    model.set_rhs('v_z_3', v_z_3_dot)

    model.set_rhs('x_4', x_4_dot)
    model.set_rhs('y_4', y_4_dot)
    model.set_rhs('z_4', z_4_dot)
    model.set_rhs('v_x_4', v_x_4_dot)
    model.set_rhs('v_y_4', v_y_4_dot)
    model.set_rhs('v_z_4', v_z_4_dot)

    model.set_rhs('d_12', d_12_dot)
    model.set_rhs('d_23', d_23_dot)
    model.set_rhs('d_34', d_34_dot)
    model.set_rhs('d_13', d_13_dot)
    model.set_rhs('d_14', d_14_dot)
    model.set_rhs('d_24', d_24_dot)

    if debug_mode:
        print("Model Right hand side:")
        print(model._rhs)

    model.setup()

    return(model)
    #END OF FUNCTION