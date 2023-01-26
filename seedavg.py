#my_mosinit can also be called directly

nA=8
nB=8
stepsizeA=.5 #pww
stepsizeB=101 #Seed

def calcparams(ii,jj):
     return [None,ii,jj,ii*stepsizeA+1,jj*stepsizeB]  

if __name__=="__main__":
    import numpy as np
    import os
    import sys

    if os.path.exists("recfolder/Data.npy"):
            os.remove("recfolder/Data.npy")

    Data=np.zeros((nA,nB),dtype="object")
    np.save("recfolder/Data",Data)
    for i in range(nA):
        for j in range(nB):
            myparams=calcparams(i,j) 

            np.save("recfolder/myparams",myparams)  #set current params, also pass the indices for saving
            commandstring="python2 my_mosinit.py SIMUL"
            os.system(commandstring)    #do simulation (uses set params) (saves the recordings)
            print("after number ", i,j)



