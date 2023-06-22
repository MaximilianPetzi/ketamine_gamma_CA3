#collects dataframe for baron and kenny mediation analysis, specifically:
# does gamma power decrease with higher krec because more asynchronous phases, or because of krec directly? OR:
# For each window, Is gamma power dependency on krec mediated ONLY by asynch(window), or is there a direct influence of krec on gamma?
withspec=False

nA=1 #control or not
nB=4 #seed    #if you change the number of parameters, also change the myparams seed index in net = Network... line accordingly 
#nC=8#REC    
nD=1#EXT and SOMA
nE=1#Loc or extinsteadofrec or Lesion
stepsizeA=1 #0 for control, 1 for LTP
stepsizeB=1002 #Seed
#stepsizeC=2.
stepsizeD=1.
stepsizeE=1.
#Car=[1,1.5,2,3,4,5,8,11,14,17,20,24,28,32,36,40]
Car=[0.,0.25,0.5,0.75,1.]
nC=len(Car)
#Loc goes from 1 .5 0 -.5 where -.5 changes tau1 and tau2 NMDAR as well


#0 entry is a flag for simulation or not, indexes of parameters are given in addition to the actual parameters for easier saving:
def calcparams(aa,bb,cc,dd,ee):#list of parameters calculated from indices
    pars=[None,aa,bb,cc,dd,ee,1+aa*stepsizeA ,1+bb*stepsizeB+cc*177+dd*178 , Car[cc],1+dd*stepsizeD ,1+ee*stepsizeE ]  #1.75+cc*stepsizeC
    return pars
def cpfp(cc,dd,ee):#shorter list of parameters
    return [Car[cc] ,1+dd*stepsizeD ,1+ee*stepsizeE]
if __name__=="__main__":
    if True:
        import numpy as np
        import os
        import sys
        import pandas as pd
        myterminal=open('myterminal.txt', 'a')
        sys.stdout=myterminal
        print("\nI seedavg.py: ______________new simulation___________________________________")
        sys.stdout=sys.__stdout__
        myterminal.close()


        if os.path.exists("recfolder/barondata"):
                os.remove("recfolder/barondata")

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
                            print("after number")
                            print(a,b,c,d,e)
        Data=pd.read_csv("recfolder/barondata")
        Data.to_csv("recfolder/oldbarondata")#keeps the old data until new sim is finished

    #to automatically push after running the code
    #import os 
    #os.system("git add *")
    #os.system("git commit -m 'automatic'")
    #os.system(r'git push [copy repo link here.....MaximilianPetzi/my_neymotin.git] HEAD:master')
