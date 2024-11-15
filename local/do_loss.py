#!/usr/bin/env python3
import numpy as np

def find_differences(data1,data_don):
    #print('here')
    sorted_data1 = data1[np.lexsort((data1[:, 0], data1[:, 1]))]
    sorted_data_don = data_don[np.lexsort((data_don[:, 0], data_don[:, 1]))]
    #print("data1 shape: %s ; data_don shape: %s"%(sorted_data1.shape,sorted_data_don.shape))
    delta_E=sorted_data1[:,2]-sorted_data_don[:,2]
    return delta_E

def loss_fn(delta_E_dimless,weights=[]):
    if len(weights)==0:
        weights=np.ones(delta_E_dimless.shape)
    loss=np.linalg.norm(delta_E_dimless*weights)
    return loss

if __name__ == "__main__":
    data1=np.loadtxt("test1/intermediate.csv",delimiter=',',skiprows=1)
    data_don=np.loadtxt("cube_donati.csv",delimiter=',',skiprows=1)
    #sorted_data1 = data1[np.lexsort((data1[:, 0], data1[:, 1]))]
    #sorted_data_don = data_don[np.lexsort((data_don[:, 0], data_don[:, 1]))]
    #print(sorted_data1[0],sorted_data_don[0])
    #print(sorted_data1[3],sorted_data_don[3])
    #print(data1.shape,data_don.shape)
    delta_E=find_differences(data1,data_don)
    #print(delta_E)