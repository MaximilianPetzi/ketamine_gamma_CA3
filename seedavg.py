#my_mosinit can also be called directly
from termcolor import colored

nA=2 #control or not
nB=2 #seed    #if you change the number of parameters, also change the myparams seed index in net = Network... line accordingly 
nC=3#recurrent    
nD=1#external
nE=1#soma
stepsizeA=1 #0 for control, 1 for LTP
stepsizeB=1002 #Seed
stepsizeC=.5
stepsizeD=.5
stepsizeE=.5

#0 entry is a flag for simulation or not, indexes of parameters are given in addition to the actual parameters for easier saving:
def calcparams(aa,bb,cc,dd,ee):    
    pars=[None,aa,bb,cc,dd,ee,1+aa*stepsizeA ,1+bb*stepsizeB ,1+cc*stepsizeC ,1+dd*stepsizeD ,1+ee*stepsizeE ]  
    return pars

if __name__=="__main__":
    import numpy as np
    import os
    import sys

    if os.path.exists("recfolder/Data.npy"):
            os.remove("recfolder/Data.npy")

    Data=np.ones((nA,nB,nC,nD,nE),dtype="object")
    np.save("recfolder/Data",Data)
    for a in range(nA):
        for b in range(nB):
            for c in range(nC):
                for d in range(nD):
                    for e in range(nE):
                        myparams=calcparams(a,b,c,d,e) 
                        np.save("recfolder/myparams",myparams)  #set current params, also pass the indices for saving
                        commandstring="python2 my_mosinit.py SIMUL"
                        os.system(commandstring)    #do simulation (uses set params) (saves the recordings)
                        print(colored(r"after number ","red"))
                        print(a,b,c,d,e)
    Data=np.load("recfolder/Data.npy",allow_pickle=True)
    np.save("recfolder/oldData.npy",Data)#keeps the old data until new sim is finished


