from alchemlyb.parsing.amber import extract_dHdl
from alchemlyb.preprocessing.subsampling import slicing
from pymbar import timeseries
import math
import os
import numpy as np
import warnings
warnings.filterwarnings('ignore')

class lambda_window:
    #Class containing functions for the processing of dcrg+vdw and water lambda windows. Must be defined with a
    #.out file from TI integration
    def __init__(self, **kwargs):
        self.__temp = 300 #Temperature in Kelvin
        self.__t_eq = .5 #Equilibration time in ns to be discarded
        self.__auto = False #Implement autoequilibration protocol
        self.__lam = -1 #lambda window value. If not provided, will be extracted from .out file
        contains_file = False #Flag to check if .out file is provided
        for kw in kwargs:
            if kw == 'lambda': #Parse user-provided lambda value
                try:
                    lam = float(kwargs[kw]) 
                    if lam < 0 or lam > 1:
                        raise TypeError("Error: invalid lambda window")
                    self.__lam = lam
                except:
                    raise TypeError("Error: lambda must be float between 0 and 1")
            if kw == 'file': #Ensure .out file exists
                if os.path.isfile(kwargs[kw]):
                    self.__file = kwargs[kw]
                    contains_file = True
                else:
                    raise TypeError('Error: invalid file')
            elif kw == 'temp': #Check if user defined temperature
                self.__temp = kwargs[kw]
            elif kw == 't_eq': #Check if user provides valid equilibration time
                try:
                    t_eq = float(kwargs[kw])
                    if t_eq < 0:
                        raise TypeError("t_eq must be positive")
                    self.__t_eq = t_eq
                except:
                    raise TypeError("Error: t_eq must be float")
            elif kw == 'auto' and kwargs[kw] == True: #Check if user utilizes autoequilibration protocol
                self.__auto = True
        if not contains_file:
            raise TypeError("Error: no file given")
        self.__dvdl = extract_dHdl(self.__file, self.__temp) #Extract thermodynamic data
        if self.__lam == -1: #Automatically determine lambda value
            self.__lam = self.__dvdl.index[0][1]
        with open(self.__file) as f: #Extract simulation constants
            self.__ntpr = 0
            self.__dt = 0
            self.__nstlim = 0
            for line in f:
                if self.__ntpr != 0 and self.__dt != 0 and self.__nstlim!= 0:
                    break
                for s in line.split(", "):
                    if "dt" in s and self.__dt == 0:
                        self.__dt = float(s[5:])
                    elif "ntpr" in s and self.__ntpr == 0:
                        self.__ntpr = int(s[7:])
                    elif 'nstlim' in s and self.__nstlim == 0:
                        self.__nstlim = int(s[9:])
                        
        
                
                
    def get_dt(self):
        return self.__dt
    
    def get_ntpr(self):
        return self.__ntpr
    
    def get_nstlim(self):
        return self.__nstlim
    
    def get_temp(self):
        return self.__temp
    
    def get_lam(self):
        return self.__lam
    
    def get_file(self):
        return self.__file
    
    def get_dvdl(self):
        return self.__dvdl
    
    def set_dvdl(self, new_dvdl):
        self.__dvdl = new_dvdl
        
    def get_sim_time(self): #Returns simulation time in ns
        return self.get_dt() * self.get_nstlim()/1000
    
    def get_auto(self):
        return self.__auto

    def get_t_eq(self):
        return self.__t_eq
    
    def get_short(self, time): #Returns a shortened simulation trajectory
        frame_cutoff = int(time*1000/self.get_ntpr()/self.get_dt+1)
        return self.get_dvdl()[:frame_cutoff]
    
    def equilibrate_ssmp(self): #Returns a equilibrated and decorrelated thermodyanic time series
        dvdl = self.get_dvdl()
        if self.get_auto(): #Use autoequilibration Protocol
            stat_ineff_lists=timeseries.detectEquilibration(self.get_dvdl()['dHdl'])
            dHdl_ssmp=slicing(dvdl[stat_ineff_lists[0]:],step=math.ceil(stat_ineff_lists[1]))
        else: #Use user-defined equilibration times
            dHdl_eq = dvdl[int(self.get_t_eq()*1000/self.get_ntpr()/self.get_dt()+1):]
            dHdl_ssmp_indices=timeseries.subsampleCorrelatedData(dHdl_eq, conservative=True)
            dHdl_ssmp = np.array(dHdl_eq['dHdl'])[dHdl_ssmp_indices]
        return dHdl_ssmp