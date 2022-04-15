import subprocess
import time
from shutil import copyfile
import numpy as np
import math
import os
import re
from subprocess import check_output
import sys
import io


def make_ts_file(mybasis,myfile,function,w=0,epsilon=0,dftd='no',run='minimize',charge=0,spinmult=1,dispersion='no', resp=False, restricted='yes', excited='no', state=0, highmethod1='no',highmethod2='no'):
    basis='basis    '+mybasis
    myco=myfile+'.xyz'
    if epsilon!=0:
        epsilon='epsilon'+'  '+str(epsilon)
        if (run=='minimize'and charge==-1):
            thepath=myfile+'add_E.xyz'
            if os.path.isfile(thepath):
                myco=myfile+'add_E.xyz'   
    coordinates='coordinates    '+myco
    filename=myfile+str(run)
    if restricted=='yes' and excited=='yes':
        filename=myfile+str(run)+'singlet'
    if restricted=='no' and excited=='yes':
        filename=myfile+str(run)+'triplet'
    openfile=filename+'.ts'
    charge1='charge          '+str(charge)
    spinmult='spinmult      '+str(spinmult)
    ts_file=open(openfile, 'w')
    ts_file.write(basis)
    ts_file.write('\n')
    ts_file.write(coordinates)
    ts_file.write('\n')
    ts_file.write(charge1)
    ts_file.write('\n')
    ts_file.write(spinmult)
    ts_file.write('\n')
    if w!=0:
        ww='rc_w'+'  '+str(w)
        ts_file.write(ww)
        ts_file.write('\n')
    if restricted=='yes':
        my_function='method    '+str(function)
        ts_file.write(my_function)
    if restricted=='no':
        my_function='method    '+'u'+str(function)
        ts_file.write(my_function)
    ts_file.write('\n')
    if dftd!='no':
        dftd='dftd '+str(dftd)
        ts_file.write(dftd)
        ts_file.write('\n')
    if epsilon!=0:
        epsilon=str(epsilon)
        ts_file.write(epsilon)
        ts_file.write('\n')
        ts_file.write('pcm cosmo')
        ts_file.write('\n')
    if dispersion!='no':
        ts_file.write('dispersion yes')
        ts_file.write('\n')
    if highmethod1=='yes': 
        ts_file.write('min_method bfgs')
        ts_file.write('\n')
        ts_file.write('min_init_hess diagonal')
        ts_file.write('\n')
    if highmethod2=='yes':
        ts_file.write('dftgrid 3')
        ts_file.write('\n')
        ts_file.write('convthre 3e-6')
        ts_file.write('\n')     
        ts_file.write('min_tolerance 4.5E-5')
        ts_file.write('\n')
        ts_file.write('min_tolerance_e 1E-7')
        ts_file.write('\n')
    if run=='minimize':   
        ts_file.write('min_coordinates cartesian')
        ts_file.write('\n')
    ts_file.write('maxit 500')
    ts_file.write('\n')
    if excited=='yes':
        ts_file.write('cis yes')
        ts_file.write('\n')
        ts_file.write('cisnumstates '+str(state))
        ts_file.write('\n')
        ts_file.write('cismaxiter 200')
        ts_file.write('\n')
    if run=='minimize':   
        ts_file.write('run minimize')
        ts_file.write('\n')
    if run=='energy':   
        ts_file.write('run energy')
        ts_file.write('\n')
    if resp==True:
        ts_file.write('resp	yes')
        ts_file.write('\n')
    ts_file.write('end')
    ts_file.close()
    return run,filename

def make_sh_file(file):
    sh_file=str(file)+'.sh'
    f = open(sh_file, 'w')
    sh= open('./terachem2.sh')
    for i, line in enumerate(sh):
        if i==9:
            openfile=myfile+'.ts'
            f.write('terachem '+os.getcwd()+'/'+file+'.ts')
        if (i !=9):
            f.write(line)
    f.close()
    filename = './'+str(file)+'.log'
    with io.open(filename, 'wb') as writer, io.open(filename, 'rb', 1) as reader:
        process = subprocess.Popen('source '+sh_file +'; env -0',shell=True, executable='/bin/bash', stdout=writer)
        while process.poll() is None:
            sys.stdout.write(str(reader.read()))
            time.sleep(0.5)
        # Read the remaining
        sys.stdout.write(str(reader.read()))

def replace_xyz(myfile,new_file=False):
    myco=myfile+'.xyz'
    fline=open(myco).readline().rstrip()
    fline=int(fline)
    newscr='scr.'+myfile
    b=0
    while b==0:
        b = os.path.getsize('./'+newscr+'/optim.xyz')
    time.sleep(10)    
    read_file3=open('./'+newscr+'/optim.xyz')
    if new_file==True:
        mynewco=myfile+'add_E.xyz'
        write_newxyz=open(mynewco, 'w')
        for line in (read_file3.readlines() [-fline-2:]):
            line1=line.rstrip('/n')
            write_newxyz.write(line1)
    if new_file==False:
        write_newxyz=open(myco, 'w')
        for line in (read_file3.readlines() [-fline-2:]):
            line1=line.rstrip('/n')
            write_newxyz.write(line1)
    write_newxyz.close()

def generate_listofname(file):
    a=[]
    file='./'+str(file)+'.txt'
    f=open(file,'r')
    for i, compound in enumerate(f):
        compound=compound.strip('\n')
        a.append(compound)
    return a 

mybasislist=['sto-3g','3-21g','6-31g','def2-SVP']
myfilelist=['Chong','Chong1','Chong2']
for myfile in myfilelist:
    for basis in mybasislist:
        jobtype,filename=make_ts_file(basis,myfile,'wpbeh',w=0.15,epsilon=17,dispersion='no', highmethod1='no',highmethod2='no')
        make_sh_file(filename)
        time.sleep(2)
        replace_xyz(myfile,new_file=False)
        time.sleep(2)
#        if basis=='def2-SVP':
#            jobtype,filename=make_ts_file(basis,myfile,'b3lyp',dispersion='yes', highmethod1='yes',highmethod2='no')
#            make_sh_file(filename)
#            time.sleep(2)
#            replace_xyz(myfile,new_file=False)
#            time.sleep(2)
#            jobtype,filename=make_ts_file(basis,myfile,'b3lyp',dispersion='yes', highmethod1='yes',highmethod2='yes')
#            make_sh_file(filename)
#            time.sleep(2)
#            replace_xyz(myfile,new_file=False)
#            time.sleep(2)
    myco=myfile+'.xyz'
    mynewco='opt'+myfile+'.xyz'
    os.rename(myco, mynewco)
