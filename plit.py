import numpy as np
from matplotlib import pyplot as plt
import seedavg

Data=np.load("recfolder/oldData.npy",allow_pickle=True)
DatShape=np.shape(Data)[0],np.shape(Data)[1],len(Data[0,0])
Dat=np.ones(DatShape)*-1      

for i in range(len(Data)):
    for j in range(len(Data[0])):
        Dat[i,j]=Data[i,j]          #build proper Tensor

dat=Dat[:,:,-1]

dat=np.array(dat,dtype=float)
y=np.average(dat,axis=1)
x=np.arange(len(y))*1
yerr=np.std(dat,axis=1)

t=np.arange(len(Dat[0,0]))*10
y=np.average(Dat[0],axis=0)
yerr=np.std(Dat[0],axis=0)
plt.plot(t,y,label="0%",color="black")
plt.errorbar(x=t[::10],y=y[::10],yerr=yerr[::10],color="black",ls='none')
y=np.average(Dat[1],axis=0)
yerr=np.std(Dat[1],axis=0)
plt.plot(t,y,label="100%",color="blue")
plt.errorbar(x=t[1::10],y=y[1::10],yerr=yerr[1::10],color="blue",ls='none')

plt.title("weight factor over time (errorbars are std, "+str(len(Dat[0]))+" seeds averaged)")
plt.xlabel("time[ms]")
plt.ylabel("average weight factor")
plt.legend()


plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.4,
                    hspace=0.4)
plt.show()



