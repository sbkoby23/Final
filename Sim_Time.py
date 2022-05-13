import numpy as np

def sim_time(dcrg_list, rtr_list, water_list):
    #Determines maximum simulation time from 3 lists of floats
    if not all(isinstance(x,float) for x in dcrg_list):
        raise TypeError("Error: Invalid dcrg list provided")
    if not all(isinstance(x,float) for x in rtr_list):
        raise TypeError("Error: Invalid rtr list provided")
    if not all(isinstance(x,float) for x in water_list):
        raise TypeError("Error: Invalid water list provided")
    water_max = np.array(water_list).max()
    dcrg_max = np.array(dcrg_list).max()
    rtr_max = np.array(rtr_list).max()
    sim_time = np.array([water_max, dcrg_max, rtr_max]).max()
    return sim_time