import subprocess
import time
from shutil import copyfile
import numpy as np
import math
import os
import re


def make_ts_file(mybasis,myfile,myw,run='minimize',charge=0,spinmult=1):
    basis='basis    '+mybasis
    rc_w='rc_w '+str(myw)
    myco=myfile+'.xyz'
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
        ts_file.write('method          wB97x')
    if charge!=0:
        ts_file.write('method          uwB97x')
    ts_file.write('\n')
    ts_file.write(rc_w)
    ts_file.write('\n')
    ts_file.write('pcm cosmo')
    ts_file.write('\n')
    ts_file.write('epsilon 6')
    ts_file.write('\n')
    ts_file.write('dispersion       yes')
    ts_file.write('\n')
    ts_file.write('pcm_scale 1')
    ts_file.write('\n')
    ts_file.write('min_coordinates cartesian')
    ts_file.write('\n')
    ts_file.write('maxit 500')
    ts_file.write('\n')
    ts_file.write('solvent_radius 	3.48')
    ts_file.write('\n')
    if run=='minimize':   
        ts_file.write('run minimize')
    if run=='energy':   
        ts_file.write('run energy')
    ts_file.write('\n')
    ts_file.write('end')
    ts_file.write('\n')
    ts_file.close()


def make_ts_file_EST(mybasis,myfile,myw,run='energy',charge=0,spinmult=1, cal='singlet'):
    basis='basis    '+mybasis
    rc_w='rc_w '+str(myw)
    myco=str(myfile)+'.xyz'
    coordinates='coordinates    '+myco
    openfile='./'+str(myfile)+'.ts'
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
    if cal=='singlet':
        ts_file.write('method          wB97x')
    if cal=='triplet':
        ts_file.write('method          uwB97x')
    ts_file.write('\n')
    ts_file.write(rc_w)
    ts_file.write('\n')
    ts_file.write('pcm cosmo')
    ts_file.write('\n')
    ts_file.write('epsilon 6')
    ts_file.write('\n')
    ts_file.write('pcm_scale 1')
    ts_file.write('\n')
    ts_file.write('dispersion       yes')
    ts_file.write('\n')
    ts_file.write('cismaxiter 500')
    ts_file.write('\n')
    ts_file.write('cis yes')
    ts_file.write('\n')
    ts_file.write('solvent_radius 	3.48')
    ts_file.write('\n')
    ts_file.write('cisnumstates 1')
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
    return True,job_id

def extract_HOMO_LUMO(myfile):
    mymolden='./scr/' +myfile+'.molden'
    read_file=open(mymolden)
    n=0
    for i, line in enumerate(read_file):
        if line.__contains__('Occup= 2.0'):
            i2=i
        if line.__contains__('Occup= 0.0') and n==0:
            i0=i
            n=1
    read_file2=open(mymolden)
    for i, line in enumerate(read_file2):
        if i==i2-2:
            HOMO=line.split()[1]
        if i==i0-2:
            LUMO=line.split()[1]
    return HOMO,LUMO

def extract_Energy(myfile):
    myfile1='./'+myfile+'.out'
    read_file3=open(myfile1)
    for line in (read_file3.readlines() [-90:]):
        if line.__contains__('FINAL ENERGY:'):
            energy=line.split()[2]
    return energy

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


def w_tuning(mybasis,myw,myfile):
    make_ts_file(mybasis,myfile,myw)
    make_sh_file(myfile)
    done=check_run_status()
    time.sleep(10)
    Energy0=extract_Energy(myfile)
    HOMO, LUMO= extract_HOMO_LUMO(myfile)
    replace_xyz(myfile)   
    make_ts_file(mybasis,myfile,myw,run='energy',charge=1,spinmult=2)  #remove one electron
    make_sh_file(myfile)
    done=check_run_status()
    Energy_0p1=extract_Energy(myfile)
    make_ts_file(mybasis,myfile,myw,run='minimize',charge=-1,spinmult=2) #add one electron
    make_sh_file(myfile)
    done=check_run_status()
    time.sleep(10)
    Energy_n1=extract_Energy(myfile)
    replace_xyz(myfile,new_file=True)
    myfile2=myfile+'add_E' #new file
    make_ts_file(mybasis,myfile2,myw,run='energy',charge=0,spinmult=1)  
    make_sh_file(myfile2)
    done=check_run_status()
    time.sleep(10)
    Energy_n1p0=extract_Energy(myfile2)
    errorH=(float(Energy0)-float(Energy_0p1))-float(HOMO)
    errorL=(float(Energy_n1)-float(Energy_n1p0))-float(LUMO)
    error=np.sqrt(errorH**2+errorL**2)
    return error


def gss(J, a, b,mybasis,myfile, tol=0.01):
    listofw=open('./w_file.txt', 'w')
    gr = (math.sqrt(5) + 1) / 2
    c = b - (b - a) / gr
    d = a + (b - a) / gr
    while abs(b - a) > tol:
        J1=w_tuning(mybasis,c,myfile)
        time.sleep(10)
        J2=w_tuning(mybasis,d,myfile)
        if J1<J2:
            b = d
        else:
            a = c
        txt='w1= '+ str(c)+ 'J1= '+ str(J1)+'w2= '+ str(d) + ' J2= '+str(J2)
        listofw.write(txt)
        listofw.write('/n')
        c = b - (b - a) / gr
        d = a + (b - a) / gr
    return (b + a) / 2


def extractxyzfromscan(molecule):
    mymolecule=[]
    f=open('./scr/scan_optim.xyz', 'r') #you can change the path pf oroginal file
    line1=f.readline()
    line1=int(line1)
    count = len(f.readlines())
    numberofmolecule=int(count/(line1+1))
    for i,line in enumerate(open('./scr/scan_optim.xyz', 'r')):
        filetowrite='./'+str(molecule)
        myfilename=(i)//(line1+2)
        if -1 < i <=(line1+2)*numberofmolecule:
            filetowrite=filetowrite+str(myfilename)+'.xyz'
            f2=open(filetowrite, 'a')
            f2.write(line)
    f2.close()
    pathofmylistofmolecule=open('./mylistest.txt','w')
    for i in range(numberofmolecule):
        mylistofmolecule=str(molecule)+str(i)
        pathofmylistofmolecule.write(mylistofmolecule)
        pathofmylistofmolecule.write('\n')  
    pathofmylistofmolecule.close()

def extractexcitation(idname,datafile,angle,typeE):
    idname='./slurm-'+str(idname)+'.out'
    path=open(idname)
    ii=1000000000
    mydatafile='./'+str(datafile)+'.txt'
    if os.path.exists(mydatafile):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not
    with open(mydatafile, append_write) as f:
        for i,line in enumerate(path):
            if line.__contains__("Final Excited State Results:"):
                ii=i
            if i==ii+4:
                line=re.split('\s+', line)
                line=str(line)
                line=line.split(',')
                lineE=line[3]
                lineO=line[4]
                f.write(str(typeE)+' , '+str(angle)+' , '+lineE+' , '+lineO)
                f.write('\n')
                print(line, i)

mybasis='def2-SVP'
myfilelist=['optsolar-cell-DBT1','optsolar-cell-DBT2','optsolar-cell-DBT3']
for myfile in myfilelist:
    w_final=gss(w_tuning,0.00,0.05,mybasis,myfile)
    make_ts_file(mybasis,myfile,w_final)
    make_sh_file(myfile)
    done=check_run_status()
    time.sleep(10)
    myco=myfile+'.xyz'
    mynewco=myfile+str(w_final)+'.xyz'
    os.rename(myco, mynewco)
