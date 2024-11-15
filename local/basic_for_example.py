#!/usr/bin/env python3

import numpy as np
from xml_bandgap import get_Eg_xml 
from bandgap_qescf import qe_scf_bandgap_SR
import os
import re

def bandgaps_basic_csv():
    ls1=os.listdir()
    #p1=re.compile()
    p1=re.compile(r"In([0-9|.]+)Ga[0-9|.]+As[0-9|.]+Sb([0-9|.]+)")
    data=[]
    for item1 in ls1:
        if os.path.isdir(item1) and 'pycache' not in item1:
            #temp="%s/tmp"%item1
            for item2 in os.listdir(item1):
                if ".in.out" in item2:
                    q1=p1.search(item2)
                    x=float(q1.group(1))
                    y=float(q1.group(2))
                    Eg=float(qe_scf_bandgap_SR("%s/%s"%(item1,item2)))
                    data.append([x,y,Eg])
    print(data)
    np.savetxt('intermediate.csv',data,delimiter=',',header='x,y,Eg(eV)')
    return np.array(data)

if __name__ == "__main__":
    bandgaps_basic_csv()
