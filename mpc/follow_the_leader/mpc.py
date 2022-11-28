import numpy as np
from mpc_model import mpc_model
from mpc_controller import mpc_controller
from mpc_simulator import mpc_simulator


#Funktion för simuleringar.
def mpc(
    mpc,
    simulator, 
    x0, 
    u0, 
    debug_mode = False, 
    prediction_range = 10
    ):


    if debug_mode:
        print("Using debug mode.\n")

    mpc.x0 = x0 #current states (position and velocity)
    mpc.u0 = u0 #current control signals (pitch, roll, thrust)
    simulator.x0 = x0
    simulator.u0 = u0


    #Control loop   
    mpc.set_initial_guess()  
    u0_return = mpc.make_step(x0)
    x0_return = simulator.make_step(u0_return) #Simulated next step
    

    #Projected trajectory for simulations
    # trajectory = []
    # trajectory.extend([x0_return[0:3]])
    # for i in range(prediction_range-1): #10 steps prediction by standard, -1 from u0_return,x0_return
    #         u0 = mpc.make_step(x0)
    #         x0 = simulator.make_step(u0)
    #         trajectory.extend([x0[0:3]])

    return(u0_return, x0_return.reshape(-1))#, trajectory)



# #Slimmad version av samma funktion. Räknar enbart ut nästa styrsignal utifrån observerat x (inputs).
# def mpc(mpc,
#     x_obs, 
#     u0, 
#     debug_mode = False
#     ):

#     if debug_mode:
#         print("Using debug mode.\n")

#     mpc.x0 = x_obs
#     mpc.u0 = u0
#     #Control loop   
#     mpc.set_initial_guess()  
#     u0_return = mpc.make_step(x_obs)

#     return u0_return