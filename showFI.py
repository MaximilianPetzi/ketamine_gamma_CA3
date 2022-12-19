import numpy as np
import measureFI #just to access stepsize and n
from matplotlib import pyplot as plt
plt.style.use("seaborn-darkgrid")
Data=np.load("recfolder/FI.npy", allow_pickle=True)

position=1
for k in range(Data.size):
    spiketimes=Data[k]
    Farr=[]
    lengths=[]
    scatterdata=[]
    for i in range(spiketimes.size):
        if spiketimes[i].size>1:
            Fvalue=len(spiketimes[i])/(spiketimes[i][-1]-spiketimes[i][0])
        else:   Fvalue=0
        if spiketimes[i].size==1: Fvalue=-1
        Farr.append(Fvalue)
        lengths.append(spiketimes[i].size)#number of spikes
        for j in range(spiketimes[i].size):
                scatterdata.append([i,spiketimes[i][j]])
    scatterdata=np.array(scatterdata)

    Farr1=[]
    last_usable_idx=len(Farr)
    for i in range(len(Farr)):
        if i>1:
            if lengths[i]<lengths[i-1]:
                last_usable_idx=i
                break
        Farr1.append(Farr[i])

    Farr2=Farr[last_usable_idx:]
    print("number of spikes:")
    print(lengths)
    plt.subplot(3,2,1+2*k)
    plt.ylim(ymax=.3,ymin=0)
    xvals1=np.arange(0,last_usable_idx)*measureFI.stepsize[k]
    xvals2=np.arange(last_usable_idx,len(Farr))*measureFI.stepsize[k]
    plt.plot(xvals1,Farr1,"green")
    plt.plot(xvals2,Farr2,"red")
    plt.xlabel("$I_{inj}$")
    plt.ylabel("F")
    plt.subplot(3,2,2+2*k)
    plt.scatter(scatterdata[:,1],scatterdata[:,0],s=.1,c="black")
    plt.xlabel("time in ms")

plt.show()