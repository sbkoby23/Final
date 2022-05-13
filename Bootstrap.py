import numpy as np
from sklearn.utils import resample

def boot(dvdl, boot_samples, boot_seed):
    #Calculates mean and variance of input thermodynamic data using bootstrap
    if not (type(dvdl) == list or type(dvdl)==np.ndarray):
        raise TypeError("Error: Invalid dvdl input type")
    if not (type(boot_samples)==int and boot_samples >= 1):
        raise TypeError("Error: boot_samples must be positive and int")
    if not (type(boot_seed)==int and boot_seed >= 1):
        raise TypeError("Error: boot_seed must be positive and int")
    np.random.seed(boot_seed)
    boot_sample = [resample(dvdl, n_samples=len(dvdl)) for j in range(boot_samples)]
    boot_means=np.array([j.mean() for j in boot_sample])
    boot_mean=boot_means.mean()
    boot_var = boot_means.std()**2
    return boot_mean, boot_var
