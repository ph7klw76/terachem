"""
Created on Thu Dec 24 18:21:44 2020

input must be terachem md xyz files
"""

import numpy as np
import math


def calc_dihedral(pA, pB, pC, pD):
    
    a1 = ((pB[0]-pA[0]),(pB[1]-pA[1]),(pB[2]-pA[2]))
    a2 = ((pC[0]-pB[0]),(pC[1]-pB[1]),(pC[2]-pB[2]))
    a3 = ((pD[0]-pC[0]),(pD[1]-pC[1]),(pD[2]-pC[2]))
    a1 = a1/np.sqrt(np.dot(a1,a1))
    a2 = a2/np.sqrt(np.dot(a2,a2))
    a3 = a3/np.sqrt(np.dot(a3,a3))
    v1 = np.cross(a1, a2)
    v2 = np.cross(a2, a3)
    dihedral = math.acos(np.dot(v1,v2))
    
    return dihedral


def extracttorsionalangle(filepath,c1,c2,c3,c4):
    ii=0
    mydata=[]
    with open(filepath,'r') as f:
        for i,line in enumerate(f):
            if i==0:
                no_of_atom=int(line)
            if i==int((no_of_atom+2)*ii+(c1+1)):
                A=np.asarray(line.split())
            if i==int((no_of_atom+2)*ii+(c2+1)):
                B=np.asarray(line.split())
            if i==int((no_of_atom+2)*ii+(c3+1)):
                C=np.asarray(line.split())
                print(line, ii, (no_of_atom+2)*ii+(c3+1), i)
            if i==int((no_of_atom+2)*ii+(c4+1)):
                D=np.asarray(line.split())
            if i==int((no_of_atom+2)*(ii+1)):
                a=A[1:]
                b=B[1:]
                c=C[1:]
                d=D[1:]
                u1=np.array([a[0],a[1],a[2]])
                u2=np.array([b[0],b[1],b[2]])
                u3=np.array([c[0],c[1],c[2]])
                u4=np.array([d[0],d[1],d[2]])
                pA=u1.astype(np.float)
                pB=u2.astype(np.float)
                pC=u3.astype(np.float)   
                pD=u4.astype(np.float)
                dihedral=calc_dihedral(pA, pB, pC, pD)*180/np.pi
                ii+=1
                mydata.append(dihedral)
    return mydata
        
                
            
                
LS19=extracttorsionalangle('E:/coors-MDLS19.xyz',19,18,23,24)  
with open('E:/MDLS19-3.txt','w') as ff:
    for data in LS19:
        ff.write(str(data))
        ff.write('\n')
