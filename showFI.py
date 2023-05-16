import numpy as np
from measureFI import * #in order to access ncc (and n)
from my_mosinit import * #in order to access stim.dur and amplitude stepsize, and celltypes and comps
from matplotlib import pyplot as plt
plt.style.use("seaborn-darkgrid")

Data=np.load("recfolder/FI.npy")

freqs=np.copy(Data)
for j in range(len(Data[:,0])):
    for i in range(len(Data[0,:])):
        freqs[:,i]=Data[:,i]/stimdur*1000 #freq=count/stimdur
amparr=np.arange(len(Data[0]))*stepsize #amplitude=idx*stepsize

def curve(c=0):#FI curve for one cell
    #c is the cell plus compartment index (from 0 to 5, see measureFI for coding)
    plt.plot(amparr,freqs[c])

    plt.ylabel("number of spikes")
    plt.xlabel("input amplitude")
    plt.show()

def curves():#FI curve for all cells stacked
    fig, ax = plt.subplots(ncc,1)
    for c in range(ncc):
        ax[c].plot(amparr,freqs[c])
        ax[c].set_ylabel("Freq of "+celltypes[c]+"."+comps[c]+"                             ")
        y_label = ax[c].yaxis.get_label()
        y_label.set_rotation(0)
    fig.suptitle('FI curves of pyr,olm,basket')
    ax[-1].set_xlabel("I")
    plt.show()

curves()






if False:
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