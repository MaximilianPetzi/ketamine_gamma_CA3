#my_mosinit can also be called directly

nA=1
nB=4
stepsizeA=.5 #pww
stepsizeB=108 #Seed

def calcparams(ii,jj):
    pars=[None,ii,jj,ii*stepsizeA+1,jj*stepsizeB]  
    return pars

if __name__=="__main__":
    import numpy as np
    import os
    import sys

    if os.path.exists("recfolder/Data.npy"):
            os.remove("recfolder/Data.npy")

    Data=np.ones((nA*2,nB),dtype="object")
    np.save("recfolder/Data",Data)
    for i in range(nA):
        for j in range(nB):
            myparams=calcparams(i,j) 

            np.save("recfolder/myparams",myparams)  #set current params, also pass the indices for saving
            commandstring="python2 my_mosinit.py SIMUL"
            os.system(commandstring)    #do simulation (uses set params) (saves the recordings)
            print("after number ", i,j)



