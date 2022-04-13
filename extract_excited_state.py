"""
Created on Wed Apr 13 21:41:22 2022
extract excited state MD files
@author: User
"""
import glob, os
dirf="E:/horizon/LS12/"
f=open(dirf+"result.txt",'w')
os.chdir(dirf)
for file in glob.glob("*.out"):
    start=0
    myfile=dirf+file
    file=open(myfile,'r')
    txttomatch='  Final Excited State Results:'
    for i, line in enumerate(file):
        line=line.strip('\n')
        if "XYZ coordinates" in line:
            cor=line.split('XYZ coordinates')[1]
        if line==txttomatch:
            start=i
        if start!=0 and start+9>=i>=start+4:
            f.write(cor+'  '+line)
            f.write('\n')
f.close()
