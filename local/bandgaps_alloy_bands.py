#!/usr/bin/env python3

import numpy as np
from local.xml_bandgap import get_Eg_xml 
import os
import re

def bandgaps_xml_csv():
    ls1=os.listdir()
    #p1=re.compile()
    p1=re.compile(r"In([0-9|.]+)Ga[0-9|.]+As[0-9|.]+Sb([0-9|.]+)")
    data=[]
    data1=[]
    for item1 in ls1:
        if os.path.isdir(item1) and 'pycache' not in item1:
            temp="%s/tmp"%item1
            xml_found=False
            for item2 in os.listdir(temp):
                if '.xml' in item2:
                    #print(item2)
                    q1=p1.search(item2)
                    if q1:
                        x=float(q1.group(1))
                        y=float(q1.group(2))
                        Eg=float(get_Eg_xml("%s/%s"%(temp,item2)))
                        data.append([x,y,Eg])
                        data1.append([item1,str(Eg)])
                        xml_found=True
                    else:
                        print("sheeiitt not found that xml file, things not looking hot")
                        print(item2)
            if xml_found==False: #for if the .out crashed with dE0 problem
                for item2 in os.listdir(temp):
                    if '.save'  in item2:
                        q1=p1.search(item2)
                        if q1:
                            x=float(q1.group(1))
                            y=float(q1.group(2))
                            Eg=float(get_Eg_xml("%s/%s/%s"%(temp,item2,'data-file-schema.xml')))
                            data.append([x,y,Eg])
                            data1.append([str(item1),str(Eg)])
                        else:
                            print("sheeiitt not found that xml file, things not looking hot, data schema version")
                            print(item2)
    np.savetxt('intermediate.csv',data,delimiter=',',header='x,y,Eg(eV)')
    print(data1[0])
    np.savetxt('data_Eg.csv',data1,delimiter=',',header='key,Eg',fmt='%s,%s')
    return np.array(data)

if __name__ == "__main__":
    bandgaps_xml_csv()
