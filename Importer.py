import glob
import os

def import_TI(complex_name):
    #complex_name is a string representing the path to the directory containing TI calculations
    #Find and return paths to all production .out files
    if not os.path.isdir(complex_name):
        raise TypeError("Error: complex directory does not exist!")
    fnamelist = glob.glob(complex_name+'/dcrg+vdw/la-0.[1-9]/prod/*.out*')
    fnamelist.sort()

    if len(fnamelist) != 9:
        raise TypeError("Error : Number of lambdas should be 9")

    fnamelist_water = glob.glob(complex_name+'/water-dcrg+vdw/la-0.[1-9]/prod/*.out*')
    fnamelist_water.sort()

    if len(fnamelist_water) != 9:
        raise TypeError("Error : Number of lambdas should be 9")
        
    fnamelist_rtr = glob.glob(complex_name+'/rtr/la-*/prod/*.out*')
    fnamelist_rtr.sort()
    fnamelist_rtr.append(complex_name+'/dcrg+vdw/la-0.0/prod/complex_prod.out')
    return fnamelist, fnamelist_water, fnamelist_rtr

def import_rstr(complex_name):
    #complex_name is a string representing the path to the directory containing TI calculations
    #find and return paths to all rstr files
    if not os.path.isdir(complex_name):
        raise TypeError("Error: complex directory does not exist!")
    files = glob.glob(complex_name+'/rtr/*/rstr*')
    files.sort()
    if len(files) != 7:
        raise TypeError("Error: number of rtr != 7")
    return files