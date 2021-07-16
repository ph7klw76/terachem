from ase import Atoms
from ase.optimize import BFGS
import torchani
from ase import units
from ase.md.langevin import Langevin
import mkl
mkl.set_num_threads(16)
import os
from shutil import copyfile

def atomicmass(a):
    if a=='H':
        a=1
    if a=='C':
        a=6
    if a=='N':
        a=7
    if a=='O':
        a=8
    if a=='F':
        a=9
    if a=='S':
        a=16
    return a

def convert(mypath):        
    mymolecule=[]
    myposition=[]
    myatom=[] 
    fp=open(mypath, 'r') #you can change the path pf oroginal file
    for i,line in enumerate(fp):
        line1=line.strip('\n')
        line1=line.split()
        if i>1:
            mymolecule.append(atomicmass(line1[0]))
            myatom.append(line1[0])
            atomposition=(float(line1[1]),float(line1[2]),float(line1[3]))
            myposition.append(atomposition)
        if i==0:
            line1=line.strip('\n')
            line1=int(line1)
            noatom=int(line1)
    return myatom,myposition,mymolecule,noatom

def storexyz(noatom,Z,m,path):
    myposition2=[]
    myposition2.append(str(noatom))
    with open(path, 'a') as f:
        f.write(str(noatom)+'\n')
    with open(path, 'a') as f:
        f.write(m+'\n')   
    myposition2.append(' ')
    for i,line in enumerate(Z):
        a,b,c=line[0],line[1],line[2]
        a=str(a)
        b=str(b)
        c=str(c)
        atomposition=str(myatom[i])+'   '+a+'   '+b+'   '+c
        with open(path, "a") as f:
            f.write(atomposition+'\n') 
        myposition2.append(atomposition)
    return myposition2
    
# def printenergy(a=molecule):
#    """Function to print the potential, kinetic and total energy."""
#    epot = a.get_potential_energy() / len(a)
#    ekin = a.get_kinetic_energy() / len(a)
#    print('Energy per atom: Epot = %.3feV  Ekin = %.3feV (T=%3.0fK)  '
#          'Etot = %.3feV' % (epot, ekin, ekin / (1.5 * units.kB), epot + ekin))
#    Z=molecule.get_positions()
#    m=('Energy per atom: Epot = %.3feV  Ekin = %.3feV (T=%3.0fK) '
#                   'Etot = %.3feV' % (epot, ekin, ekin / (1.5 * units.kB), epot + ekin)+'\n') 
#    storexyz(noatom,Z,m)
#    return
savepath='/scratch/woon/ML/data-opt/'
path='/scratch/woon/ML/data/'
for filename in os.listdir(path):
    if filename.endswith('.xyz'): 
        new_filename=filename.split('.')[0]
        mypath=os.path.join(path, filename)
        try:
            myatom,myposition,mymolecule,noatom=convert(mypath)
            print(myatom)
            molecule = Atoms(numbers=mymolecule,positions=myposition)
            print('Begin minimizing...')        
            calculator = torchani.models.ANI2x().ase()
            molecule.set_calculator(calculator)
            opt = BFGS(molecule)
            opt.run(fmax=0.0001)
            print()
            Z=molecule.get_positions()
            print(Z)
            mypath2=os.path.join(savepath, filename)
            storexyz(noatom,Z,'opt',mypath2)
        except:
            mypath2=os.path.join(savepath, filename)
            copyfile(mypath, mypath2)
