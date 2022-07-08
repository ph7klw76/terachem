ffw=open('E:/test/bb.txt','w')
for i in range(59):
    fw=open('E:/test/'+str(i)+'.ts','w')
    ffw.write('terachem /home/user/woon/horizon/LS/LS19/excited/'+str(i)+'.ts'+'\n')
    fw.write('basis           cc-pvdz'+'\n')
    fw.write('coordinates     '+str(i)+'.pdb'+'\n')
    fw.write('charge     0'+'\n')     
    fw.write('spinmult 1'+'\n')
    fw.write('method          uwPBEh'+'\n')
    fw.write('rc_w 0.0425'+'\n')
    fw.write('pcm cosmo'+'\n')
    fw.write('epsilon 2.38'+'\n')
    fw.write('cis yes'+'\n')
    fw.write('cisnumstates 12'+'\n')
    fw.write('cismaxiter 100'+'\n')
    fw.write('run energy'+'\n')
    fw.close()
ffw.close()
