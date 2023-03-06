import numpy as np
from matplotlib import pyplot as plt
import seedavg



Data=np.load("recfolder/oldData.npy",allow_pickle=True)
DatShape=np.shape(Data)[0],np.shape(Data)[1],np.shape(Data)[2],np.shape(Data)[3],np.shape(Data)[4],len(Data[0,0,0,0,0][0])
DatShape2=np.shape(Data)[0],np.shape(Data)[1],np.shape(Data)[2],np.shape(Data)[3],np.shape(Data)[4],2
Dat=np.ones(DatShape)*-1      
Dat2=np.ones(DatShape2)*-1 
f=Data[0,0,0,0,0][0]
for a in range(len(Data)):
    for b in range(len(Data[0])):
        for c in range(len(Data[0,0])):
            for d in range(len(Data[0,0,0])):
                for e in range(len(Data[0,0,0,0])):     #build proper Tensor
                    Dat[a,b,c,d,e]=Data[a,b,c,d,e][1]      #full recordings, not saved anymore    
                    Dat2[a,b,c,d,e,:]=Data[a,b,c,d,e][2:4]  #theta and gamma power
dat=np.array(Dat,dtype=float)
dat2=np.array(Dat2,dtype=float)
#dat=dat[:,:,0,0,0]
#dat2=dat2[:,:,0,0,0]
imax=len(dat2[0,0])
jmax=len(dat2[0,0,0])
kmax=len(dat2[0,0,0,0])

def difs():

    for i in range(imax):#rec, each a different figure
        plt.figure(i,figsize=(12,10), dpi=80)

        for j in range(jmax):#ext, row? in subplot
            for k in range(kmax):#soma column in subplot
                plt.subplot(kmax,jmax,1+k+kmax*j)
                pows=np.average(dat2,axis=1)
                pows_std=np.std(dat2,axis=1)/(len(dat2[0])-1)**.5 #sample error estimate or whatever
                x=np.arange(len(pows))/1.+1.
                plt.plot(x,pows[:,i,j,k,1],label="gamma power(30-100 Hz)", color="black")#first index=0 means control trial, last index=1 means gamma
                plt.errorbar(x=x,y=pows[:,i,j,k,1],yerr=pows_std[:,i,j,k,1],color="grey",fmt=".")
                plt.ylim(1,5)
                #plt.xlabel("ctrl. vs. ket.")
                plt.text(1,4,str(i)+str(j)+str(k))#rec,ext,som=xxx
        plt.subplots_adjust(left=None, bottom=None, right=1., top=1., wspace=None, hspace=None)
        plt.title("rec="+str(i))
    plt.show()

def allplots():
    difs=0
    pows=np.average(dat2,axis=1)
    pows_std=np.std(dat2,axis=1)/(len(dat2[0])-1)**.5 #sample error estimate or whatever
    x=np.arange(len(pows))/1.+1.
    print("seeds sims", dat2[:,:,0,3,0,1])
    print("firsterrval", pows_std[:,0,3,0,1])
    import sys
    sys.exit()
    for i in range(imax):#rec, each a different figure
        plt.figure(i,figsize=(12,10), dpi=80)

        for j in range(jmax):#ext, row? in subplot
            for k in range(kmax):#soma column in subplot
                plt.subplot(kmax,jmax,1+k+kmax*j)
                plt.plot(x,pows[:,i,j,k,1],label="gamma power(30-100 Hz)", color="black")#first index=0 means control trial, last index=1 means gamma
                plt.errorbar(x=x,y=pows[:,i,j,k,1],yerr=pows_std[:,i,j,k,1],color="grey",fmt=".")
                plt.ylim(1,5)
                #plt.xlabel("ctrl. vs. ket.")
                plt.text(1,4,str(i)+str(j)+str(k))#rec,ext,som=xxx
        plt.subplots_adjust(left=None, bottom=None, right=1., top=1., wspace=None, hspace=None)
        plt.title("rec="+str(i))
    plt.show()

allplots()




