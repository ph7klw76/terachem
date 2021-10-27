import subprocess
import time

def cancel_job():
    f=open('./cancel2.txt','r')
    for i, compound in enumerate(f):
        compound=compound.strip('\n')
        compound=str(compound)
        subprocess.run(['scancel', compound])
        time.sleep(1)
    return

cancel_job()
