#runs many my_mosinit.py scripts and saves results
#my_mosinit can also be called directly

#for Car freq gamma test, change Car, nC, stepsizeC, calcparams.Car(cc), cpfp.Car(cc) 
#                                and in my_mosinit: line 374 write to file a.freq()
withspec=False

nA=1 #control or not
nB=2 #seed    #if you change the number of parameters, also change the myparams seed index in net = Network... line accordingly 
#nC=8#REC    
nD=1#EXT and SOMA
nE=1#Loc or extinsteadofrec
stepsizeA=1 #0 for control, 1 for LTP
stepsizeB=1002 #Seed
#stepsizeC=2.
stepsizeD=1.
stepsizeE=1.
#Car=[1,6,11,16,21,26,31,36,36.5,37,37.5,38,38.5,39,39.5,40,41,42,43] #THIS OVERWRITES stepsize
#Car=[0,1,2,3,4,5,7,10,15]

#Car=[0,1,2,6,11,16,21,26,31,36,36.5,37,37.5,38,38.5,39,39.5,40,41,42,43]
#Car=[1,10,20,31,36,40]

Car=[1,2]#,4,8,12,16,20,24,28,32,36,40]
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

        myterminal=open('myterminal.txt', 'a')
        sys.stdout=myterminal
        print("\nI seedavg.py: ______________new simulation___________________________________")
        sys.stdout=sys.__stdout__
        myterminal.close()


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
                            print("after number")
                            print(a,b,c,d,e)
        Data=np.load("recfolder/Data.npy",allow_pickle=True)
        np.save("recfolder/oldData.npy",Data)#keeps the old data until new sim is finished

    #to automatically push after running the code
    #import os 
    #os.system("git add *")
    #os.system("git commit -m 'automatic'")
    #os.system(r'git push [copy repo link here.....MaximilianPetzi/my_neymotin.git] HEAD:master')
