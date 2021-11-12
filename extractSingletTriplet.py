def extract_ST(file):
    S=[]
    T=[]
    with open(file,'r') as f1:
        for i, line in enumerate(f1):
            line=line.strip('\n')
            if '3  singlet' in line:
                S1=line.split()[4]
                S.append(float(S1))
            line=line.strip('\n')
            if '4  singlet' in line:
                S1=line.split()[4]
                S.append(S1)
            if '5  singlet'in line:
                S1=line.split()[4]
                S.append(float(S1))
            if '2  triplet' in line:
                T1=line.split()[4]
                T.append(float(T1))
            line=line.strip('\n')
            if '3  triplet' in line:
                T1=line.split()[4]
                T.append(T1)
            if '4  triplet'in line:
                T1=line.split()[4]
                T.append(float(T1))
    return min(S), min(T)
    f1.close()
