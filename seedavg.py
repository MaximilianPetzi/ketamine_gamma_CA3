#runs many my_mosinit.py scripts and saves results
#my_mosinit can also be called directly

#for Car freq gamma test, change Car, nC, stepsizeC, calcparams.Car(cc), cpfp.Car(cc) 
#                                and in my_mosinit: line 374 write to file a.freq()
withspec=False

nA=1 #control or not
nB=16 #seed    #if you change the number of parameters, also change the myparams seed index in net = Network... line accordingly 
#nC=8#REC    
nD=1#EXT and SOMA

stepsizeA=1 #0 for control, 1 for LTP
stepsizeB=1002 #Seed
#stepsizeC=2.
stepsizeD=1.
stepsizeE=1.
#Car=[1,6,11,16,21,26,31,36,36.5,37,37.5,38,38.5,39,39.5,40,41,42,43] #THIS OVERWRITES stepsize
#Car=[0,1,2,3,4,5,7,10,15]
#Car=[15,20]
#Car=[0,1,2,6,11,16,21,26,31,36,36.5,37,37.5,38,38.5,39,39.5,40,41,42,43]


#Car=[1,11,21,31,36,41]
#Ear=[1,4,16,64]#Loc (Taufac)

#Car=[0,3,6,10,15,20,30,45,60,70,80,90,100,110,120,130,150,175,200,250,300,350,400,500]
#Ear=[.2,.4,.8,1.,2,5,12,30] #::tau=tau*taufac

#Car=[0,3,6,10,12,20,40,70,160,230]
#Ear=[1.0,0.75,0.50,0.25,0.001,-0.001,-0.125,-0.25,0.375,-0.5,0.75,-1] #Locations

Car=[0,3,6,10,12,20,40,70]
Ear=[0.001,0.125,0.25,0.375,0.5,0.75,1] #Locations
nC=len(Car)
nE=len(Ear)
#Loc goes from 1 .5 0 -.5 where -.5 changes tau1 and tau2 NMDAR as well


#0 entry is a flag for simulation or not, indexes of parameters are given in addition to the actual parameters for easier saving:
def calcparams(aa,bb,cc,dd,ee):#list of parameters calculated from indices
    pars=[None,aa,bb,cc,dd,ee,1+aa*stepsizeA ,1+bb*stepsizeB+cc*177+dd*178 , float(Car[cc]),1+dd*stepsizeD ,Ear[ee] ]  #1.75+cc*stepsizeC
    return pars
def cpfp(cc,dd,ee):#shorter list of parameters
    return [Car[cc] ,1+dd*stepsizeD ,1+ee*stepsizeE]
if __name__=="__main__":
    if True:
        from datetime import datetime
        import numpy as np
        import os
        import sys

        myterminal=open('myterminal.txt', 'a')
        sys.stdout=myterminal
        print("\nI seedavg.py: ______________new simulation at time "+str(datetime.now())+"___________")
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
