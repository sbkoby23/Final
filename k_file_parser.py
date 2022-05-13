##K_file Parsing
import os

def k_parse(k_file):
    #k_file is a string representing the path to the k_file
    #Parse the provided k_file to extract ref_list and k_list
    if not os.path.isfile(k_file):
        raise TypeError("Error: k file does not exist!")
    ref_list = []
    k_list = []
    with open(k_file) as f:
        size=len([0 for _ in f])
        if size != 24:
            raise TypeError("Error: incorrect number of lines")
    f.close()    
    with open(k_file) as f:
        for line in f:
            for s in line.split(", "):
                if "r2" in s:
                    ref_list.append(float(s[3:]))
                elif "rk2" in s:
                    k_list.append(float(s[4:]))
        if len(k_list) != 6:
            raise TypeError("Error: Incorrect K_list length")
        if len(ref_list) != 6:
            raise TypeError("Error: Incorrect ref_list length")
        #print(k_list)
        return ref_list, k_list