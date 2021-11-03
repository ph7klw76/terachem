# for terachem 1.5

def extract_optsim(myfile):
    myfile1='./scr.'+myfile+'/'+'optim.xyz'
    myco='./'+myfile+'.xyz'
    fline=open(myco,'r').readline().rstrip()
    fline=int(fline)
    read_file3=open(myfile1)
    write_newxyz=open(myco, 'w')
    for line in (read_file3.readlines() [-fline-2:]):
        line1=line.rstrip('/n')
        write_newxyz.write(line1)
    write_newxyz.close()

myfilelist=['opt1','opt2','opt2Cz3DPhCzBN','opt2CzBN','opt36-DPXZ-AD','opt3Cz2DMeCzBN','opt3Cz2DPhCzBN','opt4CzBN','opt5CzBN','optbis-PXZ-TRZ-73','optBPPZ-PXZ','optDMAC-DPS-116','optDMAC-TRZ','optDPO-TXO2','optm-3CzBN','optm-ATP-PXZ-89','optm-DAz-TXO2','optmDPBPZ-PXZ','opto-3CzBN','optoDTBPZ-DPXZ','optp-DAz-TXO2','optpDBBPZ-DPXZ','optpDTBPZ-DPXZ','optPXZ-ph-TRZ','optTCA-C4','optTOAT-Cz','optTOAT-TRZ']
for file in myfilelist:
    extract_optsim(file)
