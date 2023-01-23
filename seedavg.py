#my_mosinit can also be called directly

nA=2
nB=2
stepsizeA=1 #Ket
stepsizeB=1 #Seed
import numpy as np
import os
import sys

if os.path.exists("recfolder/Data.npy"):
        os.remove("recfolder/Data.npy")

Data=np.zeros((nA,nB),dtype="object")
np.save("recfolder/Data",Data)
for j in range(nA):
    for i in range(nB):
        myparams=[None,i,j,stepsizeA*i,stepsizeA*j]  
        np.save("recfolder/myparams",myparams)  #set current params, also pass the indices for saving
        commandstring="python2 my_mosinit.py SIMUL"
        os.system(commandstring)    #do simulation (uses set params) (saves the recordings)




