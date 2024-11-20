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
    
def ind_U_comb(x,y,U_params):
    #for key in U_params.keys():
    #    print(key,U_params[key])
    U_in={}
    U_in['In-5p']=y*U_params['InSb']['In-5p']+(1-y)*U_params['InAs']['In-5p']
    U_in['Ga-4p']=y*U_params['GaSb']['Ga-4p']+(1-y)*U_params['GaAs']['Ga-4p']
    U_in['As-4p']=x*U_params['InAs']['As-4p']+(1-x)*U_params['GaAs']['As-4p']
    U_in['Sb-5p']=x*U_params['InSb']['Sb-5p']+(1-x)*U_params['GaSb']['Sb-5p']
    return U_in

def write_U_sectionfile(base,x,y):
    with open("./%s.in"%base) as fi0:
        s=fi0.read()
    U_in=write_Uin(x,y,"../U_int.json",'./U_in.json',write=False)
    for key in U_in.keys():
        s=re.sub("<%s>"%key,str(U_in[key]),s)
    with open('%s.in'%base,'w') as fi2:
        fi2.write(s)
    #print(base)

def write_U_to_file(file,Us):
    p1=re.compile(r"(\S+).in")
    p2=re.compile(r"In([0-9|.]+)Ga[0-9|.]+As[0-9|.]+Sb([0-9|.]+)")
    q1=p1.search(file)
    q2=p2.search(file)
    x,y=float(q2.group(1)),float(q2.group(2))
    base=q1.group(1)
    U_in=ind_U_comb(x,y,Us)
    with open(file, 'r') as fi:
        s=fi.read()
    for key in U_in.keys():
        s=re.sub("<%s>"%key,str(U_in[key]),s)
    with open(file,'w') as fo:
        fo.write(s)
    

def write_U_to_files(Us):
    #for key in Us.keys():
    #    print(key,Us[key])
    #print(Us['InSb'])
    p1=re.compile(r"(\S+).in")
    p2=re.compile(r"In([0-9|.]+)Ga[0-9|.]+As[0-9|.]+Sb([0-9|.]+)")
    list1=os.listdir()
    for item1 in list1:
        if os.path.isdir(item1):
            #print('here1')
            list2=os.listdir(item1)
            for item2 in list2:
                if '.in' in item2 and 'test.in' not in item2:
                    #print('here')
                    #print(item2)
                    q1=p1.search(item2)
                    q2=p2.search(item2)
                    x,y=float(q2.group(1)),float(q2.group(2))
                    #U_in=ind_U_comb(x,y,Us)
                    write_U_to_file("%s/%s"%(item1,item2),Us)


if __name__=="__main__":
    #print(interpolation_a_bin(1.0,0.0))
    p1=re.compile(r"(\S+).in")
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
                if '.in' in thing2:
                    base=p1.search(thing2).group(1)
                    q2=p2.search(thing2)
                    x=float(q2.group(1))
                    y=float(q2.group(2))
                    print(x,y)
                    write_U_sectionfile(base,x,y)
                    #print(base)
                    #]exit('done done')

            
        else:
            print("Directory does not exist")

