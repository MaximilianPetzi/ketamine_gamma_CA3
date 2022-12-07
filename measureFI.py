import numpy as np
import os
import sys
data=np.array([])
np.save("recfolder/FI",data)
for i in range(1):
    os.system("python2 my_mosinit.py")#script saves in .npy file the value
    #print("args:",sys.argv[1])
dat=np.load("recfolder/FI.npy")
print(dat)





