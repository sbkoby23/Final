import numpy as np
import os


def calc_dvdl(current_values, ref_values, force_constants):
    #This function calculates harmonic energy values. All variables are lists of 6 numbers
    if len(current_values) == len(ref_values) and len(ref_values) == len(force_constants):
        dvdl = 0
        for i in range(len(current_values)):
            dvdl += force_constants[i]*((float(current_values[i])-ref_values[i])**2)
        return dvdl

    else:
        print(len(current_values),' ',len(ref_values),' ',len(force_constants))
        raise TypeError('Error: Number of current values, reference values and/or constants is not the same:')
        


def check_dihedrals(current_values, ref_values):
# this function check values of dihedral angles and converts them to a correct range if needed.
# I.e., if reference value is 179 but a raw value at some frame is -175,
# this value should be converted to 185 to obtain a correct dv/dl.
    checkout = []
    for i in [2,4,5]:
        absdelta = abs(float(current_values[i])-ref_values[i])
        #checkout.append(absdelta)
        if absdelta > 240:
            initial = current_values[i]
            current_values[i] = ref_values[i] - abs(360.0 - absdelta)
            checkout.append(str(i)+' diheral value is changed:  '+str(initial)+'  '+str(current_values[i]))
    return [current_values, checkout]

def get_dvdls(rstr_file, k_list, ref_list):
    #Returns thermodynamic data extracted from the rstr file
    if not os.path.isfile(rstr_file):
        raise TypeError("Error: invalid rstr file given")
    for n in range (1,6):
        k_list[n] = k_list[n]/(57.2958**2)
    dvdls=[]
    cfile = open(rstr_file, 'r') # current file
    lines = cfile.readlines()
    for line in lines:
        cdof = line.split() # current degrees of freedom
        del cdof[0]
        if len(cdof) > 6: del cdof[-1]
        cdof, check_dih = check_dihedrals(cdof, ref_list)
        dvdl_val = calc_dvdl(cdof, ref_list, k_list)
        #print(dvdl_val)
        dvdls.append(dvdl_val)
    return np.array(dvdls)

