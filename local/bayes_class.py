#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 14:17:41 2024

for the Bayes class

@author: gentles
"""
import numpy as np
from bayes_opt import UtilityFunction
from bayes_opt import BayesianOptimization

class BayesianOpt:
    def __init__(self,pbounds,r_data={},loss_data=[],kappa=5):
        self.r_data=r_data
        
        self.loss_data=loss_data
        self.utility_function = UtilityFunction(kind="ucb", kappa=kappa, xi=0)
        for key in pbounds.keys():
            key1=key
        self.optimizer= BayesianOptimization(f=None, 
                                             pbounds=pbounds,
                                             verbose=2,
                                             random_state=1,
                                             allow_duplicate_points=True)
        if len(r_data)==0:
            #print('here')
            for key in pbounds.keys():
                #print(key)
                r_data[key]=[]
        else:
            #print('here1')
            for i in range(len(self.r_data[key1])):
                inter={}
                for key in self.r_data.keys():
                    inter[key]=self.r_data[key][i]
                self.register_param(inter,self.loss_data[i])
        
    def register_param(self,r,loss):
        print(r)
        if loss>0:
            loss*=-1
        self.optimizer.register(params=r,target=loss)
        
    def save_param(self,r,loss):
        for key in r.keys():
            self.r_data[key].append(r[key])
    
    def suggest(self):
        next_point_to_probe = self.optimizer.suggest(self.utility_function)
        return next_point_to_probe
        
        
if __name__=="__main__":
    GA_file="data_exp-hse_GA.csv"
    data1=np.loadtxt(GA_file,dtype=float,delimiter=',',skiprows=1)
    Us=data1[:,1:3]
    r_data={'x':Us[:,0],'y':Us[:,1]}
    loss=data1[:,6]
    pbounds={'x':(-10,10),'y':(0,10)}
    
    print(len(pbounds))
    this=BayesianOpt(pbounds,r_data,loss)
    print(this.suggest())
