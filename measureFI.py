import numpy as np
import os
import sys
data=np.array([])

np.save("recfolder/FI",data)
for i in range(50):
    I=i*0.02
    print("python2 my_mosinit.py "+str(I))
    os.system("python2 my_mosinit.py "+str(I))#script saves in .npy file the value
    
    #print("args:",sys.argv[1])
dat=np.load("recfolder/FI.npy")

print(dat)





