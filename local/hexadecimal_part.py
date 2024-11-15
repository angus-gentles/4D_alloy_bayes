#!/usr/bin/env python3
import numpy as np
import sys

def hexes_from_sets(sets):
    cum=np.cumsum(sets)
    #print(len(sets))
    things=""
    list_hex=[]
    for i,set1 in enumerate(sets):
        for j in range(set1):
            things+='1'
        if i>0:
            for j in range(cum[i-1]):
                things+='0'
        #print(things)
        list_hex.append(hex(int(things,2)))
        things=""
    #things1=hex(int(things,2))
    return list_hex

if __name__=="__main__":
    args=np.array(sys.argv[1:]).astype(int)
    hexes1=hexes_from_sets(args)
    hexes_string=""
    for hex1 in hexes1:
        hexes_string+="%s "%hex1
    print(hexes_string)


