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
x=np.arange(len(y))*seedavg.stepsizeA
yerr=np.std(dat,axis=1)
print(dat)
print(x)
print(y)
print(yerr)
plt.subplot(2,1,1)
plt.plot(x,y,color="black")
plt.errorbar(x=x,y=y,yerr=yerr)
plt.xlabel("ketamine percentage of time")
plt.ylabel("average final weight change factor")
plt.title("effect of ketamine on weights, average over "+str(len(dat[0]))+" different seeds")

t=np.arange(len(Dat[0,0]))*10
plt.subplot(2,1,2)
y=np.average(Dat[0],axis=0)
yerr=np.std(Dat[0],axis=0)
plt.plot(t,y,label="0%",color="black")
plt.errorbar(x=t[::10],y=y[::10],yerr=yerr[::10],color="black")
y=np.average(Dat[1],axis=0)
yerr=np.std(Dat[1],axis=0)
plt.plot(t,y,label="33%",color="blue")
plt.errorbar(x=t[1::10],y=y[1::10],yerr=yerr[1::10],color="blue")
y=np.average(Dat[2],axis=0)
yerr=np.std(Dat[2],axis=0)
plt.plot(t,y,label="66%",color="purple")
plt.errorbar(x=t[2::10],y=y[2::10],yerr=yerr[2::10],color="purple")
y=np.average(Dat[3],axis=0)
yerr=np.std(Dat[3],axis=0)
plt.plot(t,y,label="99%",color="red")
plt.errorbar(x=t[3::10],y=y[3::10],yerr=yerr[3::10],color="red")
plt.title("avg weight factor over time")
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



