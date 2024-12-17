#!/usr/bin/env python3

#import numpy as np 

increase=653
with open('all_data.csv','r') as fi:
    with open('all_data_3.csv','w') as fo:
        line=fi.readline()
        fo.write(line)
        line=fi.readline()
        while line :
            datum=line.split(',')
            number=str(int(datum[0])+increase)
            datum[0]=number
            new_line='%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s'%tuple(datum)
            fo.write(new_line)
            line=fi.readline()