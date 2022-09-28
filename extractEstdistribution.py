@author: ph7klw
"""
f=open('F:/LS-QMD/LS19/second/result.txt','r')
f2=open('F:/LS-QMD/LS19/second/result2.txt','w')
mydataS=[]
mydataT=[]
for i, line in enumerate(f):
    line=line.split()
    if int(line[1])==1:
        print(line[1])
        fff=line[0]  
        ST=float(line[5])
        a=int(line[7])
        b=int(line[9])
        E=float(line[3])
        if i!=0:
            for dataT in mydataT:
                a1=dataT[0]
                b1=dataT[1]
                for dataS in mydataS:
                    a2=dataS[0]
                    b2=dataS[1]   
                    if a1==a2 and b1==b2:
                        deltaE=dataS[2]-dataT[2]
                        f2.write(str(fff)+','+str(a1)+'->'+str(b1)+','+str(deltaE)+','+str(dataS[2])+'\n')
        mydataS,mydataT=[],[]
        if ST<0.05:
            mydataS=[(a,b,E)]
        if ST>1.95:
            mydataT=[(a,b,E)]
    if int(line[1])!=1:
        ST=float(line[5])
        a=int(line[7])
        b=int(line[9])
        E=float(line[3])
        if ST<0.05:
            mydataS.append((a,b,E))
        if ST>1.95:
            mydataT.append((a,b,E))
f.close()
f2.close()
