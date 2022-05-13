#Output

import pandas as pd
import numpy as np

def output(complex_name,dcrg_m, dcrg_e, rtr_m, rtr_e, water_m,water_e, boresch, sim_length):
    #Outputs .dat file containing summary statistics of various types of lambda windows and overall dG values
    dG_m = water_m - boresch - dcrg_m - rtr_m
    dG_e = (dcrg_e + rtr_e + water_e)**.5
    round_vector = np.around(np.array([sim_length, dG_m, dG_e,
                                      dcrg_m, dcrg_e**.5,
                                      rtr_m, rtr_e**.5,
                                      water_m, water_e**.5, boresch]), decimals=2)
    df=pd.DataFrame(round_vector).transpose()
    df.columns=['simulation_length' ,'ddG', 'ddG_std_err', 'dcrg+vdw', 'dcrg+vdw_std_err',
                'rtr', 'rtr_std_err', 'water', 'water_std_err', 'Boresch']

    df.to_csv(complex_name+'_summary.dat', sep='\t', index=False)