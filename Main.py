#!/usr/bin/env python3

import Analytical
import Bootstrap
import Boresch
import k_file_parser
import lambda_window
import rtr_window
import Integrate
import Output
import Importer
import Sim_Time
import argparse
import random

#Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('complex', type=str, help='path to directory containing complex TI calculations')
parser.add_argument('--bootstrap', type=int, default=0, help='determines bootstrap sample for variance estimation. Default gives analytical variance')
parser.add_argument('--bootstrap_seed', type=int, default=random.randint(0, 1000000), help='random seed for bootstrap resampling')
args = parser.parse_args()

#Remove / from end of complex argument
if args.complex[len(args.complex)-1] == '/':
    args.complex = args.complex[:-1]

#Parse k_file
ref_list, k_list = k_file_parser.k_parse(args.complex+'/k.RST')

#Calculate Boresch value
boresch=Boresch.boresch(ref_list, k_list)

#Find location of *.out and rstr* files
dcrg_fnamelist, water_fnamelist, rtr_fnamelist = Importer.import_TI(args.complex)
rstr_fnamelist = Importer.import_rstr(args.complex)

#Define lists for storing dHdl values
dcrg_equilibrated=[]
water_equilibrated=[]
rtr_equilibrated=[]
lambda_list=[]
dcrg_times=[]
rtr_times=[]
water_times=[]


#Extract equilibrated and decorrelated thermodynamic time series data, simulation time length,
#and rtr lambda values
for i in range(9):
    l_window=lambda_window.lambda_window(file=dcrg_fnamelist[i])
    dcrg_equilibrated.append(l_window.equilibrate_ssmp())
    dcrg_times.append(l_window.get_sim_time())
    w_window=lambda_window.lambda_window(file=water_fnamelist[i])
    water_equilibrated.append(w_window.equilibrate_ssmp())
    water_times.append(w_window.get_sim_time())
    if i < 7:
        r_window = rtr_window.rtr_window(file=rtr_fnamelist[i], rstr=rstr_fnamelist[i], ref_list=ref_list, k_list=k_list)
        rtr_equilibrated.append(r_window.equilibrate_ssmp())
        lambda_list.append(r_window.get_lam())
        rtr_times.append(r_window.get_sim_time())

#Calculate simulation maximum time length in ns
sim_time = Sim_Time.sim_time(dcrg_times, water_times, rtr_times)

#Calculate thermodynamic statistics via bootstrap or analytical methodologies
dcrg_means, dcrg_vars, water_means, water_vars, rtr_means, rtr_vars = [],[],[],[],[],[]
if args.bootstrap != 0:
    for i in range(9):
        dcrg_mean, dcrg_var = Bootstrap.boot(dcrg_equilibrated[i], args.bootstrap, args.bootstrap_seed)
        dcrg_means.append(dcrg_mean)
        dcrg_vars.append(dcrg_var)
        water_mean, water_var = Bootstrap.boot(water_equilibrated[i], args.bootstrap, args.bootstrap_seed)
        water_means.append(water_mean)
        water_vars.append(water_var)
        if i < 7:
            rtr_mean, rtr_var = Bootstrap.boot(rtr_equilibrated[i], args.bootstrap, args.bootstrap_seed)
            rtr_means.append(rtr_mean)
            rtr_vars.append(rtr_var)
else:
    for i in range(9):
        dcrg_mean, dcrg_var = Analytical.analytical(dcrg_equilibrated[i])
        dcrg_means.append(dcrg_mean)
        dcrg_vars.append(dcrg_var)
        water_mean, water_var = Analytical.analytical(water_equilibrated[i])
        water_means.append(water_mean)
        water_vars.append(water_var)
        if i < 7:
            rtr_mean, rtr_var = Analytical.analytical(rtr_equilibrated[i])
            rtr_means.append(rtr_mean)
            rtr_vars.append(rtr_var)   

#Integrate dHdl means and variances
dcrg_mean, dcrg_error = Integrate.lambda_integrate(dcrg_means, dcrg_vars)
rtr_mean, rtr_error = Integrate.rtr_integrate(rtr_means, rtr_vars, lambda_list)
water_mean, water_error = Integrate.lambda_integrate(water_means, water_vars)

#Output .dat file of summary statistics
Output.output(args.complex, dcrg_mean, dcrg_error, rtr_mean, rtr_error, water_mean, water_error, boresch, sim_time)

  