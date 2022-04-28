#""
import numpy as np
import matplotlib.pyplot as plt
#  lamda in nm and sigma in eV lamda0 is the excitation wavelength
def ei(lamda0,lamda1,f,sigma):
    sigma=1239.84/sigma
    ei=1.3062974e8*f/(1e7/sigma)
    e=((1.0/lamda1-1.0/lamda0)/(1.0/sigma))**2
    ei=ei*np.exp(-e)
    return ei

readfile=open('F:/LS12/MD/result.txt','r')  
n=6000
sigma=0.20
absorption=[0]*n
absorption=np.asarray(absorption)
lamda1=[(x+2207)/10 for x in range(n)]
lamda1=np.asarray(lamda1)
for i, line in enumerate(readfile):
    line1=line.split()
    f=float(line1[4])
    if f==0.0000:
        f=0.0000
    lamda0=1239.84/(float(line1[3]))
    absorption=absorption+ei(lamda0,lamda1,f,sigma)
data=np.stack((lamda1, absorption),axis=1)

#normalizing to experimental data
readfile=open('F:/LS12/MD/result.txt','r')  
absorption=[0]*n
absorption=np.asarray(absorption)
location=np.where(data == np.max(data))[0][0]
wavemax=data[int(location)][0]
shift=1239.84/252.53-1239.84/wavemax
for i, line in enumerate(readfile):
    line1=line.split()
    f=float(line1[4])
    if f==0.0000:
        f=0.0000
    lamda00=1239.84/(float(line1[3])+shift)
    absorption=absorption+ei(lamda00,lamda1,f,sigma)

absorption=absorption/np.max(data)
plt.plot(lamda1,absorption)
plt.show()
data=np.stack((lamda1, absorption),axis=1)
savefile=open('F:/LS12-absorption.txt','w') 
np.savetxt(savefile, data)
savefile.close()
readfile.close()
