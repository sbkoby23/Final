from alchemlyb.preprocessing.subsampling import slicing
import numpy as np
from pymbar import timeseries
import math
import os
import re
import Resr_parse
import warnings
warnings.filterwarnings('ignore')


class rtr_window:
    #Class containing functions for the processing of dcrg+vdw and water lambda windows. Must be defined with a
    #.out file and rstr* file from TI integration, and a k_list and ref_list from the k_file_parser module
    def __init__(self, **kwargs):
        self.__t_eq = .5 #Equilibration time in ns
        self.__auto = False #Implement autoequilibratoin protocol
        self.__lam = -1 #Placeholder for lambda value
        contains_file = False #Flags for necessary user-provided variables
        contains_k_list = False
        contains_ref_list = False
        contains_rstr = False
        for kw in kwargs:
            if kw == 'lambda': #parse user-defined lambda value
                try:
                    lam = float(kwargs[kw])
                    if lam < 0 or lam > 1:
                        raise TypeError("Error: invalid lambda window")
                    self.__lam = lam
                except:
                    raise TypeError("Error: lambda must be float between 0 and 1")
            elif kw == 'file': #Ensure .out file exists
                if os.path.isfile(kwargs[kw]):
                    self.__file = kwargs[kw]
                    contains_file = True
                else:
                    raise TypeError('Error: invalid file')
            elif kw == 'rstr': #Ensure rstr file exists
                if os.path.isfile(kwargs[kw]):
                    self.__rstr = kwargs[kw]
                    contains_rstr = True
                else:
                    raise TypeError('Error: invalid rstr file')
            elif kw == 'temp':
                self.__temp = kwargs[kw]
            elif kw == 't_eq': #ensure valid user-defined equilibration temp
                try:
                    t_eq = float(kwargs[kw])
                    if t_eq < 0:
                        raise TypeError("t_eq must be positive")
                    self.__t_eq = t_eq
                except:
                    raise TypeError("Error: t_eq must be float")
            elif kw == 'auto' and kwargs[kw] == True: #Check whether to implement autoequilibration protocol
                self.__auto = True
            elif kw == 'ref_list': #Define ref_list
                self.__ref_list = kwargs[kw]
                if len(self.__ref_list) != 6 or type(self.__ref_list) != list:
                    raise TypeError("Error: Invalid ref_list")
                contains_ref_list = True
            elif kw == 'k_list': #Define k_list
                self.__k_list = kwargs[kw]
                if len(self.__k_list) != 6 or type(self.__k_list) != list:
                    raise TypeError("Error: Invalid k_list")
                contains_k_list = True
        if not contains_file:
            raise TypeError("Error: no file given")
        if not contains_rstr:
            raise TypeError("Error: no rstr file given")
        if not contains_ref_list or not contains_k_list:
            raise TypeError("Error: no k_list or ref_list given")
        #Parse .out file for simulation constants
        self.__istep1 = 0
        self.__dt = 0
        self.__ntpr = 0
        self.__nstlim = 0
        with open(self.__file) as f:
            for line in f:
                if self.__istep1 != 0 and self.__dt != 0 and self.__ntpr != 0 and self.__nstlim != 0:
                    break
                for s in line.split(", "):
                    if "dt" in s and self.__dt == 0:
                        self.__dt = float(s[5:])
                    elif "istep1" in s and self.__istep1 == 0:
                        self.__istep1 = int(s[9:])
                    elif "ntpr" in s and self.__ntpr == 0:
                        self.__ntpr = int(s[7:])
                    elif 'nstlim' in s and self.__nstlim == 0:
                        self.__nstlim = int(s[9:])
        #Parse rstr, k_list and ref_list for dvdl data
        self.__dvdl = Resr_parse.get_dvdls(self.__rstr, self.__k_list, self.__ref_list)
        #Automatically determine lambda value
        if self.__lam == -1:
            self.__lam = float(re.findall('\d+\.\d+',self.__rstr )[0])



    def get_istep1(self):
        return self.__istep1
    
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
    
    def get_auto(self):
        return self.__auto

    def get_t_eq(self):
        return self.__t_eq
    
    def get_sim_time(self): #Returns simulation time in ns
        return self.get_dt() * self.get_nstlim()/1000
    
    def get_short(self, time): #Returns truncated thermodynamic data
        frame_cutoff = int(time*1000/self.get_istep1()/self.get_dt()+1)
        return self.get_dvdl()[:frame_cutoff]
    
    def equilibrate_ssmp(self, dvdl=0): #Equilibrate and decorrelate thermodynamic times series data.
        #User can provide a numpy array of thermodynamic data, specifically from the get_short() method
        if dvdl==0:
            dvdl = self.get_dvdl()
        elif type(dvdl) != np.ndarray or len(dvdl) < 3:
            raise TypeError("Error: Invald dvdl value given.")
        if self.get_auto(): #Implement autoequilibration protocol
            stat_ineff_lists=timeseries.detectEquilibration(self.get_dvdl()['dHdl'])
            dHdl_ssmp=slicing(dvdl[stat_ineff_lists[0]:],step=math.ceil(stat_ineff_lists[1]))
        else: #Implement user-defined equilibration time
            dHdl_eq = dvdl[int(self.get_t_eq()*1000/self.get_istep1()/self.get_dt()+1):]
            dHdl_ssmp_indices=timeseries.subsampleCorrelatedData(dHdl_eq, conservative=True)
            dHdl_ssmp = dHdl_eq[dHdl_ssmp_indices]
        return dHdl_ssmp