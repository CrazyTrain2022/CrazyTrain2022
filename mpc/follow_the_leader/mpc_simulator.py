import do_mpc

def mpc_simulator(model, t_step = 0.1):
    #Setup simulator
    simulator = do_mpc.simulator.Simulator(model)
    simulator.set_param(t_step = t_step)
    simulator.setup()
    return(simulator)