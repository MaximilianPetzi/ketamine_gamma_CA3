import numpy as np
import os
import sys
n=3
os.remove("recfolder/FI.npy")
data=np.zeros((n),dtype="object")
np.save("recfolder/FI",data)
cells=["pyr","bas","olm"]
for i in range(n):
    I=i*.125
    print("python2 my_mosinit.py "+str(I)+" "+cells[i])
    os.system("python2 my_mosinit.py "+str(I)+" "+cells[i])#script saves in .npy file the value
    
    #print("args:",sys.argv[1])
#dat=np.load("recfolder/FI.npy")






