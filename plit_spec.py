import numpy as np
from matplotlib import pyplot as plt
import seedavg

x=np.arange(2)/2.+1.

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
                for e in range(len(Data[0,0,0,0])):
                    Dat[a,b,c,d,e]=Data[a,b,c,d,e][1]          #build proper Tensor
                    Dat2[a,b,c,d,e,:]=Data[a,b,c,d,e][2:4]
dat=np.array(Dat,dtype=float)
dat2=np.array(Dat2,dtype=float)
#dat=dat[:,:,0,0,0]
#dat2=dat2[:,:,0,0,0]
ps=np.average(dat,axis=1)
for i in range(len(dat2)):#rec, each a different figure
    for j in range(len(dat2[0])):#ext, row? in subplot
        for k in range(len(dat2[1])):#soma column in subplot
            plt.subplot(2,2,1+k+2*j)
            pows=np.average(dat2,axis=1)
            pows_std=np.std(dat2,axis=1)/(len(dat2[0])-1)**.5
            plt.plot(x,pows[:,i,j,k,1],label="gamma power(30-100 Hz)", color="black")#first index=0 means control trial, last index=1 means gamma
            plt.errorbar(x=x,y=pows[:,i,j,k,1],yerr=pows_std[:,i,j,k,1],color="grey",fmt=".")

            plt.xlabel("ctrl. vs. ket.")
            plt.ylabel("spectral power, rec,ext,som="+str(i)+str(j)+str(k))
    plt.subplots_adjust(left=None, bottom=None, right=1., top=1., wspace=None, hspace=None)
    plt.show()



