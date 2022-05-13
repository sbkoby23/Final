# Final
Final Project for Parallel Computing course
This final project is a software package for the calculation of dG values from thermodynamic integration of alchemical absolute binding free energy simulations of protein-ligand systems generated using the AMBER pmemd.cuda engine.



APIs:

lambda_window module: A class for the parsing of TI Thermodynamic data generated from AMBER. This class is used to process data from the dcrg+vdw and water steps. The class requires a path to a .out file for inititalization, and contains functions for the equilibration, decorrelation, and truncation of the data.

rtr_window module: A class for the parsing of TI Thermodynamic data generated from AMBER. This class is used to parse data from the rtr step. The class requires a path to a .out file, rstr file, and k_list and ref_list from the parsing the k.RST file. It contains functions for the equilibration, decorrelation, and truncation of the data.

Analytical module: This module contains a function for the analytical calculation of the mean and variance of a equilibrated and decorrelated time series.

Input: np.ndarray of time series data
Output: Mean and Variance of input time series

Bootstrap module: This module contains a function for the calculation of the mean and variance of an equilibrated and decorrelated time series using the standard bootstrap resampling algorithm.

Input: np.ndarray of time series data
Output: Mean and Variance of input time series

Boresch module: This module contains a function for the application of the Boresch formula.

Input: ref_list and k_list from k_file_parser module.
Output: float representing result of Boresch formula

Importer module: This module contains two functions for the importing of thermodynamic data

import_TI: (for .out files)
Input: path to directory contatining thermodynamic data
output: three lists containing the paths to the producion .out files for the dcrg+vdw, rtr, and water steps, respectively.

import_rtr: (for rstr files)
Input: path to directory containing thermodynamid data.
Output: list containing the paths to the rstr files.

Integrate module: This module contains functions for the integration of the the summary statistics from various lambda windows.

lambda_integrate: (for dcrg+vdw or water windows)
Input: a list of means and a list of variances of the lambda windows
Output: Integrated Mean and Variance of the windows

rtr_integrate: (for rtr windows)
Input: a list of means, a list of variances, and alist of lambda values for the rtr windows.
Output: Integrated Mean and Variance of the windows

k_file_parser module: This module parses the k_file and returns the ref_list and k_list for use by other modules.
Input: path to the k.RST file
Output: ref_list and k_list, respectively.

Output module: This module contains a function for the generation and output of summary statistics for the overall windows and the overall dG value.
Input: 
complex_name: string representing the location of the directory containing the TI data
dcrg_m: float representing the integrated mean value of the dcrg+vdw simulations
dcrg_e: float representing the integrated variance value of the dcrg+vdw simulations
rtr_m: float representing the integrated mean value of the rtr simulations
rtr_e: float representing the integrated variance value of the rtr simulations
water_m: float representing the integrated mean value of the water simulations
water_e: float representing the integrated variance value of the water simulations
boresch: float representing the value of the Boresch formula
sim_length: float representing the simulation maximum time length

Output: .dat file named "complex_name"_summary.dat containing summary data in tab separated format

Rstr_parse module: Module for the parsing of rstr files.
Input: path to rstr file, the k_list and the ref_list.
Output: an np.ndarray of the thermodynamic time series

Sim_Time module: this module calculates the maximum simulation time.
Input: three lists containing the maximum simulation time from each lambda window of the dcrg+vdw, rtr, and water steps.
Output: Float representing the maximum simulation time
