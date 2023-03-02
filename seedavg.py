#my_mosinit can also be called directly
from termcolor import colored

nA=2 #control or not
nB=2 #seed
nC=1
nD=1
nE=2
nF=1
stepsizeA=1 #0 for control, 1 for LTP
stepsizeB=1002 #Seed
stepsizeC=.4
stepsizeD=.4
stepsizeE=.4
stepsizeF=.4

def calcparams(ii,jj):
    pars=[None,ii,jj,ii*stepsizeA,jj*stepsizeB]  
    return pars

if __name__=="__main__":
    import numpy as np
    import os
    import sys

    if os.path.exists("recfolder/Data.npy"):
            os.remove("recfolder/Data.npy")

    Data=np.ones((nA,nB,nC,nD),dtype="object")
    np.save("recfolder/Data",Data)
    for a in range(nA):
        for b in range(nB):
            for c in range(nC):
                for d in range(nD):
                    myparams=calcparams(a,b,c,d) 
                    np.save("recfolder/myparams",myparams)  #set current params, also pass the indices for saving
                    commandstring="python2 my_mosinit.py SIMUL"
                    os.system(commandstring)    #do simulation (uses set params) (saves the recordings)
                    print(colored("after number ","red"))
                    print(a,b,c,d)
    Data=np.load("recfolder/Data.npy",allow_pickle=True)
    np.save("recfolder/oldData.npy",Data)#keeps the old data until new sim is finished


