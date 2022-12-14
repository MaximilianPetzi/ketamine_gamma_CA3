import numpy as np
import os
import sys
n=3
data=np.zeros((n),dtype="object")
np.save("recfolder/FI",dict)
for i in range(n):
    I=i*.125
    print("python2 my_mosinit.py "+str(I))
    os.system("python2 my_mosinit.py "+str(I))#script saves in .npy file the value
    
    #print("args:",sys.argv[1])
#dat=np.load("recfolder/FI.npy")






