#my_mosinit can also be called directly
from termcolor import colored

nA=2
nB=10
stepsizeA=1 #0 for control, 1 for LTP
stepsizeB=1002 #Seed

def calcparams(ii,jj):
    pars=[None,ii,jj,ii*stepsizeA,jj*stepsizeB]  
    return pars

if __name__=="__main__":
    import numpy as np
    import os
    import sys

    if os.path.exists("recfolder/Data.npy"):
            os.remove("recfolder/Data.npy")

    Data=np.ones((nA,nB),dtype="object")
    np.save("recfolder/Data",Data)
    for i in range(nA):
        for j in range(nB):
            myparams=calcparams(i,j) 

            np.save("recfolder/myparams",myparams)  #set current params, also pass the indices for saving
            commandstring="python2 my_mosinit.py SIMUL"
            os.system(commandstring)    #do simulation (uses set params) (saves the recordings)
            print(colored("after number ","red"))
            print(i,j)
    Data=np.load("recfolder/Data.npy",allow_pickle=True)
    np.save("recfolder/oldData.npy",Data)#keeps the old data until new sim is finished


