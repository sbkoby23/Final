#Analytical analysis
import numpy as np

def analytical(dvdl):
    #Calculates mean and variance of input thermodynamic data
    if not (type(dvdl) == list or type(dvdl)==np.ndarray):
        raise TypeError("Error: Invalid input type")
    mean = dvdl.mean()
    var = dvdl.std()**2/len(dvdl)
    return mean, var
