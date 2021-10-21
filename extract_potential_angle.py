"""
reated on Thu Oct 21 16:12:07 2021
extract potential and dihedral angle after terachem scan to be used for gromacs
@author: KL WOON
"""
import os
import math

def extract_Potential_Angle(myfile):
    Hatree=27.2114
    convert= math.pi/180
    myfile=os.getcwd()+'/'+myfile
    writemyfile=os.getcwd()+'/extracted.txt'
    read_file=open(myfile)
    with open(writemyfile, 'w') as f:
        for i, line in enumerate(read_file):
            if line.__contains__('Converged'):
                line=line.split()
                energy=float(line[4])*Hatree  # energy of potential
                angle=float(line[6].strip('(').strip(')'))*convert # angle
                f.write(str(angle)+','+str(energy))
                f.write('\n')
            


extract_Potential_Angle('scan_optim.xyz')
