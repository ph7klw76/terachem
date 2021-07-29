# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 11:37:20 2021
Extract singlet-riplet hh-tda 
@author: KL WOON
"""
import re
import os

path='C:/Users/bomoh/OneDrive/Documents/benchamarking/TADF/bhandhlyp/'
with open('C:/Users/bomoh/OneDrive/Documents/benchamarking/TADF/bhandhlyp/data.txt','w') as w:
    for filename in os.listdir(path):
        if filename.endswith('.out'): 
            if 'optopt' in filename:
                new_file = os.path.join(path, filename)
                with open(new_file,'r') as f1:
                    ii=-5
                    T1=''
                    S1=''
                    Os=''
                    new_filename=filename.split('.')[0]
                    for i, line in enumerate(f1):
                        line=line.strip('\n')
                        if re.search('triplet', line):
                            T1=line.split()[4]
                            ii=i
                        if i==ii+1:
                            S1=line.split()[4]
                            Os=line.split()[6]
                            towrite=str(new_filename)+' '+T1+' '+S1+' '+Os+'\n'
                            print(towrite)
                            w.write(str(new_filename)+' '+T1+' '+S1+' '+Os+'\n')
w.close()
