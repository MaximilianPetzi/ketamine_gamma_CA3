#my_mosinit can also be called directly

nA=2
nB=20
stepsizeA=0.5 #Ket
stepsizeB=1 #Seed

def calcparams(ii,jj):
     return [None,ii,jj,ii*stepsizeA,jj*stepsizeB]  

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
            myparams2=[None,i,j,stepsizeA*i,stepsizeB*j] 
            myparams=calcparams(i,j) 
            assert(myparams==myparams2)

            np.save("recfolder/myparams",myparams)  #set current params, also pass the indices for saving
            commandstring="python2 my_mosinit.py SIMUL"
            os.system(commandstring)    #do simulation (uses set params) (saves the recordings)




