#!/usr/bin/env python3

import json
import re

def U_st_to_it(Us_old):
    Us_new={}
    for key1 in Us_old.keys():
        for key2 in Us_old[key1].keys():
            key3="%s;%s"%(key1,key2)
            Us_new[key3]=Us_old[key1][key2]
    return Us_new

def U_it_to_st(Us_new):
    Us_old={}
    p1=re.compile(r"(\S+);(\S+)")
    for key1 in ['InAs','GaAs','GaSb','InSb']:
        Us_old[key1]={}
    for key1 in Us_new.keys():
        #print(key1)
        q1=p1.search(key1)
        Us_old[q1.group(1)][q1.group(2)]=Us_new[key1]
    return Us_old


if __name__=="__main__":
    Uin='U_test.json'
    Uout='U_0.json'
    with open(Uout) as fi:
        Us_old=json.load(fi)
    U_new=U_it_to_st(Us_old)
    with open(Uin,'w') as fo:
        json.dump(U_new,fo)
