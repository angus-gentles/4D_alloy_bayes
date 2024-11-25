#!/usr/bin/env python3
import numpy as np
import json
import os
import sys
import subprocess 
from local.U_standard_main import U_it_to_st,U_st_to_it
from local.make_U import write_U_to_files
from local.bandgaps_alloy_bands import bandgaps_xml_csv
from local.do_loss import find_differences,loss_fn
from local.bayes_class import BayesianOpt
from local.meff import get_xml_info,meff_kpoints_eigenvalues

data_don=np.loadtxt("cube_donati.csv",delimiter=',',skiprows=1)

def iteration_old(Us):
    os.chdir('intermediate_SR')
    out0=subprocess.run(['rm -r ./*/'],shell=True)
    out1=subprocess.run(['tar','-xf','base_SR.tar'])
    U_new=U_it_to_st(Us)
    with open('U_int.json','w') as uo:
        json.dump(U_new,uo)
    write_U_to_files(U_new)
    out2=subprocess.run(['../local/run_all.sh'],shell=True)
    data1=bandgaps_xml_csv()
    delta_E=find_differences(data1,data_don)
    sorted_data_don = data_don[np.lexsort((data_don[:, 0], data_don[:, 1]))]
    delta_E_dimless=delta_E/sorted_data_don[:,2]
    loss=loss_fn(delta_E_dimless)
    os.chdir('../')
    return loss

def iteration(Us):
    os.chdir('intermediate_SR')
    out0=subprocess.run(['rm -r ./*/'],shell=True)
    out1=subprocess.run(['tar','-xf','base_SR.tar'])
    print(Us)
    U_new=Us
    #U_new=U_it_to_st(Us)
    with open('U_int.json','w') as uo:
        json.dump(U_new,uo)
    write_U_to_files(U_new)
    #exit(0)
    out2=subprocess.run(['../local/run_vary_2.sh >script_out.txt'],shell=True)
    data1=bandgaps_xml_csv()
    delta_E=find_differences(data1,data_don)
    sorted_data_don = data_don[np.lexsort((data_don[:, 0], data_don[:, 1]))]
    delta_E_dimless=delta_E/sorted_data_don[:,2]
    loss=loss_fn(delta_E_dimless)
    os.chdir('../')
    return loss

def extract_data(Us,loss,dir):
    os.chdir(dir)
    Eg_array=np.loadtxt('data_Eg.csv',dtype=str,delimiter=',',skiprows=1)
    Eg_data={}
    for i in range(len(Eg_array)):
        Eg_data[Eg_array[i,0]]=Eg_array[i,1]

    meff_data={}
    for item in ['GaAs','InAs','GaSb','InSb']:
        list1=os.listdir("%s/meff"%item)
        xml_file=''
        for item1 in list1:
            if '.xml' in item1:
                xml_file=item1
        k_points,eigenvalues,a,occupations=get_xml_info('%s/meff/%s'%(item,xml_file))
        homo_i=int(int(np.sum(occupations[0]))-1)
        homo_i=13
        meff_data["meff_%s"%item]=meff_kpoints_eigenvalues(k_points,eigenvalues,a,homo_i+1)
    data_all={}
    for key in Us.keys():
        data_all[key]=Us[key]
    for key in Eg_data.keys():
        data_all["Eg_%s"%key]=Eg_data[key]
    for key in meff_data.keys():
        data_all[key]=meff_data[key]
    data_all['loss']=loss
    os.chdir('../')
    print(data_all)
    return data_all

def current_data(direc):
    os.chdir(direc)
    data1=bandgaps_xml_csv()
    delta_E=find_differences(data1,data_don)
    sorted_data_don = data_don[np.lexsort((data_don[:, 0], data_don[:, 1]))]
    delta_E_dimless=delta_E/sorted_data_don[:,2]
    loss=loss_fn(delta_E_dimless)
    os.chdir('../')
    return loss


def init_keys():
    data_keys=['GaAs','GaSb','InSb','InAs']
    #with open('U_0.json','r') as ji:
    #    Us=json.load(ji)
    #for key in Us.keys():
    #    data_keys.append(key)
    for key in ['GaAs','GaAs3Sb1','GaAs2Sb2','GaAs1Sb3',
                'GaSb','In1Ga3Sb','In2Ga2Sb','In3Ga1Sb',
                'InSb','InAs1Sb3','InAs2Sb2','InAs3Sb1',
                'InAs','In3Ga1As','In2Ga2As','In1Ga3As']:
        data_keys.append('Eg_%s'%key)
    for key in ['GaAs','GaSb','InSb','InAs']:
        data_keys.append('meff_%s'%key)
    data_keys.append('loss')
    return data_keys


def whole_proc():
    binaries=['GaAs','GaSb','InSb','InAs']
    data_files={}
    pbounds={}
    for bina in binaries:
        data_files[bina]=np.loadtxt('data_int_%s.csv'%bina,skiprows=1,delimiter=',')[:,0:2]
        pbounds[bina]=(0,len(data_files[bina])-1)
    data_file="all_data.csv"
    data_keys=init_keys()
    print(data_keys)
    with open(data_file,'w') as fo:
        for i,key in enumerate(data_keys):
            if i==0:
                fo.write(key)
            else:
                fo.write(',%s'%key)
        fo.write('\n')
    print(pbounds)
    BO=BayesianOpt(pbounds)
    iterations=10
    U_register={'GaAs':0,'InAs':0,'GaSb':0,'InSb':0}
    for i in range(iterations):
        length_along=BO.suggest()
        for key in length_along:
            length_along[key]=np.round(length_along[key],0)
        print(i,length_along)
        Us_new={}
        Us_new['GaAs']={'Ga-4p':data_files['GaAs'][int(length_along['GaAs']),0],'As-4p':data_files['GaAs'][int(length_along['GaAs']),1]}
        Us_new['InAs']={'In-5p':data_files['InAs'][int(length_along['InAs']),0],'As-4p':data_files['InAs'][int(length_along['InAs']),1]}
        Us_new['GaSb']={'Ga-4p':data_files['GaSb'][int(length_along['GaSb']),0],'Sb-5p':data_files['GaSb'][int(length_along['GaSb']),1]}
        Us_new['InSb']={'In-5p':data_files['InSb'][int(length_along['InSb']),0],'Sb-5p':data_files['InSb'][int(length_along['InSb']),1]}
        for binary in ['GaAs','InAs','GaSb','InSb']:
            U_register[binary]=int(np.round(length_along[binary],0))
        print(i,U_register)
        loss=iteration(Us_new)
        BO.register_param(U_register,loss)
        data_all=extract_data(U_register,loss,'intermediate_SR')
        with open(data_file,'a') as fo:
            for j,key in enumerate(data_keys):
                if j==0:
                    fo.write(str(data_all[key]))
                else:
                    fo.write(',%s'%str(data_all[key]))
            fo.write('\n')

def cont_proc():
    binaries=['GaAs','GaSb','InSb','InAs']
    data_files={}
    pbounds={}
    for bina in binaries:
        data_files[bina]=np.loadtxt('data_int_%s.csv'%bina,skiprows=1,delimiter=',')[:,0:2]
        pbounds[bina]=(0,len(data_files[bina])-2)
    data_file="all_data.csv"
    data_keys=init_keys()
    
    BO=BayesianOpt(pbounds)
    #must now read the keys 
    with open(data_file,'r') as fi:
        line_keys=fi.readline().strip().split(',')
        print(line_keys)
        keys1=[]
        for line in line_keys:
            #line=line_keys[i]
            if  line=='InAs' or line=='GaAs' or line=='GaSb' or line=='InSb':
                keys1.append(line)
        print(keys1)
        line='hello'
        k=0
        line=fi.readline()
        while line and len(line)>0:
            datum=line.strip().split(',')
            Us={}
            for i in range(len(keys1)):
                Us[keys1[i]]=float(datum[i])
            loss=float(datum[-1])
            print(Us,loss)
            BO.register_param(Us,loss)
            #print(Us)
            k=1
            line=fi.readline()
        print('this_worked')

    iterations=200
    #exit(0)
    U_register={'GaAs':0,'InAs':0,'GaSb':0,'InSb':0}
    for i in range(iterations):
        length_along=BO.suggest()
        for key in length_along:
            length_along[key]=np.round(length_along[key],0)
        print(i,length_along)
        Us_new={}
        Us_new['GaAs']={'Ga-4p':data_files['GaAs'][int(length_along['GaAs']),0],'As-4p':data_files['GaAs'][int(length_along['GaAs']),1]}
        Us_new['InAs']={'In-5p':data_files['InAs'][int(length_along['InAs']),0],'As-4p':data_files['InAs'][int(length_along['InAs']),1]}
        Us_new['GaSb']={'Ga-4p':data_files['GaSb'][int(length_along['GaSb']),0],'Sb-5p':data_files['GaSb'][int(length_along['GaSb']),1]}
        Us_new['InSb']={'In-5p':data_files['InSb'][int(length_along['InSb']),0],'Sb-5p':data_files['InSb'][int(length_along['InSb']),1]}
        for binary in ['GaAs','InAs','GaSb','InSb']:
            U_register[binary]=int(np.round(length_along[binary],0))
        print(i,U_register)
        loss=iteration(Us_new)
        BO.register_param(U_register,loss)
        data_all=extract_data(U_register,loss,'intermediate_SR')
        with open(data_file,'a') as fo:
            for j,key in enumerate(data_keys):
                if j==0:
                    fo.write(str(data_all[key]))
                else:
                    fo.write(',%s'%str(data_all[key]))
            fo.write('\n')
'''
def cont_proc():
    with open('U_0.json','r') as ji:
        Us=json.load(ji)

    pbounds={}
    for key in Us.keys():
        #print(key)
        if 'As-4p' in key or 'Sb-5p' in key:
            pbounds[key]=(0.01,10)
        elif 'Ga-4p' in key or 'In-5p' in key :
            pbounds[key]=(-10,10)
        else:
            print('something is hella wrong')
            exit(1)

    BO=BayesianOpt(pbounds)

    data_keys=init_keys()
    data_file="all_data.csv"

    with open(data_file,'r') as fi:
        line_keys=fi.readline().strip().split(',')
        print(line_keys)
        keys1=[]
        #data_line={}
        #data1=np.array(fi.readline().strip().split(','))
        for i in range(len(line_keys)):
            if not ';' in line_keys[i]:
                last_ind=i-1
                print(line_keys[i-1])
                break
            keys1.append(line_keys[i])
        #print(keys1)
        line='hello'
        k=0
        line=fi.readline()
        while line and len(line)>0:
            datum=line.strip().split(',')
            Us={}
            for i in range(len(keys1)):
                Us[keys1[i]]=float(datum[i])
            loss=float(datum[-1])
            BO.register_param(Us,loss)
            #print(Us)
            k=1
            line=fi.readline()
        print('this_worked')

    iterations=200
    for i in range(iterations):
        Us_new=BO.suggest()
        for key in Us_new.keys():
            Us_new[key]=np.round(Us_new[key],2)

        loss=iteration(Us_new)
        BO.register_param(Us_new,loss)
        data_all=extract_data(Us_new,loss,'intermediate_SR')
        with open(data_file,'a') as fo:
            for i,key in enumerate(data_keys):
                if i==0:
                    fo.write(str(data_all[key]))
                else:
                    fo.write(',%s'%str(data_all[key]))
            fo.write('\n')
'''

if __name__=="__main__":
    cont_proc()
