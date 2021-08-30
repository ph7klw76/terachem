"""
Created on Mon May 17 11:03:04 2021
Terachem optimization field with PCM with assigned w
@author: user
"""
import subprocess
import time
from shutil import copyfile
import numpy as np
import math
import os


def make_ts_file(mybasis,myfile,function,w,epsilon,run='minimize',charge=0,spinmult=1):
    basis='basis    '+mybasis
    myco=myfile+'.xyz'
    w='rc_w'+'  '+str(w)
    epsilon='epsilon'+'  '+str(epsilon)
    if (run=='minimize'and charge==-1):
        thepath=myfile+'add_E.xyz'
        if os.path.isfile(thepath):
            myco=myfile+'add_E.xyz'   
    coordinates='coordinates    '+myco
    openfile=myfile+'.ts'
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
    if charge==0:
        my_function='method    '+str(function)
        ts_file.write(my_function)
    if charge!=0:
        my_function='method    '+'u'+str(function)
        ts_file.write(my_function)
    ts_file.write('\n')
    ts_file.write('min_coordinates cartesian')
    ts_file.write('\n')
    ts_file.write('maxit 500')
    ts_file.write('\n')
    ts_file.write(w)
    ts_file.write('\n')
    ts_file.write('pcm cosmo')
    ts_file.write('\n')
    ts_file.write(epsilon)
    ts_file.write('\n')
    if run=='minimize':   
        ts_file.write('run minimize')
    if run=='energy':   
        ts_file.write('run energy')
    ts_file.write('\n')
    ts_file.write('end')
    ts_file.write('\n')
    ts_file.close()


def make_sh_file(myfile):
    sh_file=str(myfile)+'.sh'
    f = open(sh_file, 'w')
    sh= open('./terachem22.sh')
    for i, line in enumerate(sh):
        if i==4:
            line1='#SBATCH --job-name='+myfile
            line1=str(line1)
            f.write(line1)
            f.write('\n')
        if i==19:
            openfile=myfile+'.ts'
            line2='terachem '+os.getcwd()+'/'+openfile
            line2=str(line2)
            f.write(line2)
            f.write('\n')
        if (i !=4 and i !=19):
            f.write(line)
    f.close()
    path='./'+ sh_file
    path=str(path)
    subprocess.run(['sbatch', path])


def check_run_status():
    time.sleep(10)
    read_file=open('./automation.out') # jobname
    for i, line in enumerate(read_file):
        job_id=line.split()[3]
    check_status='squeue -h -j '+ str(job_id)
    process=subprocess.run(check_status, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    output = process.stdout
    while output.__contains__(job_id):
        time.sleep(10)
        process=subprocess.run(check_status, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
        output = process.stdout 
    return True

def replace_xyz(myfile,new_file=False):
    myco=myfile+'.xyz'
    fline=open(myco).readline().rstrip()
    fline=int(fline)
    b=0
    while b==0:
        b = os.path.getsize('./scr/optim.xyz')
    time.sleep(10)    
    read_file3=open('./scr/optim.xyz')
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

mybasislist=['sto-3g','3-21g','cc-pvdz','aug-cc-pvdz']
myfilelist=['TOL']
for myfile in myfilelist:
    for basis in mybasislist:
        make_ts_file(basis,myfile,'wpbeh',0.074,2.34)
        make_sh_file(myfile)
        done=check_run_status()
        time.sleep(10)
        replace_xyz(myfile,new_file=False)
    myco=myfile+'.xyz'
    mynewco='opt'+myfile+'.xyz'
    os.rename(myco, mynewco)
