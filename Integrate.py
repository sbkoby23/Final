#integrate
import numpy as np

temp=300.0 #temp in K
k_b = 1.9872041e-3 #Boltzmann const in kcal/(mol*K)

def lambda_integrate(means, errors):
    #Integrate dHdl mean and variance from dcrg+vdw or water lambda windows. Output mean and variance.
    if len(means) != 9:
        raise TypeError("Error: means length != 9")
    if len(errors) != 9:
        raise TypeError("Error: errors length != 9")
    weights = np.array([.1]*9)
    mean = float(sum(np.array(means)*weights)*k_b*temp)
    error = float(sum(np.array(errors)*(weights*k_b*temp)**2))
    return mean, error

def rtr_integrate(means, errors, lambda_list):
    #Integrate dvdl mean and variance from rtr lambda windows. Output mean and variance.
    if len(means) != 7:
        raise TypeError("Error: means length != 7")
    if len(errors) != 7:
        raise TypeError("Error: errors length != 7")
    print(len(lambda_list))
    if len(lambda_list) != 7:
        raise TypeError("Error: lambda list length != 7")
    mean = np.trapz(means, lambda_list)
    error = 0
    for i in range(6):
        error += ((lambda_list[i+1]-lambda_list[i])/2)**2 * (errors[i]+errors[i+1])
    return mean, error