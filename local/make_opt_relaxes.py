#!/usr/bin/env python3

import numpy as np 
import sys
import os
import re
import json

def write_Uin(x,y,U_base_file,U_out_file,write=True):
    
    with open(U_base_file,'r') as ui:
        U_params=json.load(ui)
        
    
    U_in={}
    U_in['In-5p']=y*U_params['InSb']['In-5p']+(1-y)*U_params['InAs']['In-5p']
    U_in['Ga-4p']=y*U_params['GaSb']['Ga-4p']+(1-y)*U_params['GaAs']['Ga-4p']
    U_in['As-4p']=x*U_params['InAs']['As-4p']+(1-x)*U_params['GaAs']['As-4p']
    U_in['Sb-5p']=x*U_params['InSb']['Sb-5p']+(1-x)*U_params['GaSb']['Sb-5p']
    if write==True:
        with open(U_out_file,'w') as ui:
            json.dump(U_in,ui)
    else:
        return U_in

def interpolation_a_bin(x,y):
    xar=np.array([x,1-x])
    yar=np.array([1-y,y])
    
    Q=np.array([[11.54,10.72],[12.35,11.51]])
    
    return np.dot(yar,np.dot(Q,xar))

def write_file(base,x,y):
    with open("../base.cube.relax.in") as fi0:
        s=fi0.read()
    a=interpolation_a_bin(x,y)
    #print(a)
    s=re.sub(r"<a>",str(a),s)
    s=re.sub(r"<base>",base,s)
    counter=0
    with open("%s.alat"%(base),'r') as fi1:
        line='hello'
        while line:
            line=fi1.readline()
            line=line.strip()
            #print(line)
            if counter>1:
                s+='%s\n'%line 
            counter+=1
            #print('here')
    
    U_in=write_Uin(x,y,"../U_base.json",'./U_in.json',write=False)
    s+="\nHUBBARD atomic\n"
    for key in U_in.keys():
        s+=("U %s  %s\n")%(key,"<%s>"%key)
    with open('%s.relax.in'%base,'w') as fi2:
        fi2.write(s)
    #print(base)

if __name__=="__main__":
    #print(interpolation_a_bin(1.0,0.0))
    p1=re.compile(r"(\S+).alat")
    p2=re.compile(r"In([0-9|.]+)Ga[0-9|.]+As[0-9|.]+Sb([0-9|.]+)")
    list1=os.listdir()
    #print(list1)
    cur=os.getcwd()
    for thing in list1:
        temp="%s/%s"%(cur,thing)
        if os.path.isdir(temp):
            print("Directory exists")
            #print(temp)
            os.chdir(temp)
            for thing2 in os.listdir():
                if 'alat' in thing2:
                    base=p1.search(thing2).group(1)
                    q2=p2.search(thing2)
                    x=float(q2.group(1))
                    y=float(q2.group(2))
                    print(x,y)
                    write_file(base,x,y)
                    #print(base)
                    #]exit('done done')

            
        else:
            print("Directory does not exist")

