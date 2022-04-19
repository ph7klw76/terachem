
"""
Created on Tue Apr 19 12:48:46 2022
simulate absortion curve from Teracham MD
@author: User
"""
import numpy as np
import matplotlib.pyplot as plt
#  lamda in nm and sigma in eV lamda0 is the excitation wavelength
def ei(lamda0,lamda1,f,sigma):
    sigma=1239.84/sigma
    ei=1.3062974e8*f/(1e7/sigma)
    e=((1.0/lamda1-1.0/lamda0)/(1.0/sigma))**2
    ei=ei*np.exp(-e)
    return ei/1e10

readfile=open('E:/LS11.txt','r')  
n=10000
sigma=0.05
absorption=[0]*n
absorption=np.asarray(absorption)
lamda1=[(x+250)/10 for x in range(n)]
lamda1=np.asarray(lamda1)
for i, line in enumerate(readfile):
    line1=line.split()
    f=float(line1[4])
    if f==0.0000:
        f=0.000025
    lamda0=1239.84/float(line1[3])
    absorption=absorption+ei(lamda0,lamda1,f,sigma)
plt.plot(lamda1,absorption)
plt.show()
