import numpy as np
from matplotlib import pyplot as plt
import seedavg

Data=np.load("recfolder/oldData.npy",allow_pickle=True)
DatShape=np.shape(Data)[0],np.shape(Data)[1],len(Data[0,0][0])
DatShape2=np.shape(Data)[0],np.shape(Data)[1],2
Dat=np.ones(DatShape)*-1      
Dat2=np.ones(DatShape2)*-1 
f=Data[0,0][0]
for i in range(len(Data)):
    for j in range(len(Data[0])):
        Dat[i,j]=Data[i,j][1]          #build proper Tensor
        Dat2[i,j,:]=Data[i,j][2:4]
dat=np.array(Dat,dtype=float)
dat2=np.array(Dat2,dtype=float)
ps=np.average(dat,axis=1)
plt.subplot(1,2,1)
for i in range(len(ps)):
    plt.plot(f,ps[i],label="pww "+str((1+i/2.)))
plt.legend()
plt.grid(True)        
plt.xlim((0,60))
plt.xlabel("f[Hz]")
plt.title("spectral power of lfp")

plt.subplot(1,2,2)
pows=np.average(dat2,axis=1)
plt.plot(pows[:,0],label="theta power(3-12 Hz")
plt.plot(pows[:,1],label="gamma power(30-100 Hz")
plt.legend()
plt.xlabel("pww value number")


plt.show()



