second=1000

import numpy as np
from matplotlib import pyplot as plt
dat=np.load("spiketrains.npy",allow_pickle=True)
dat=dat.item()
pspikes=dat["P"]
ospikes=dat["O"]
bspikes=dat["B"]

spiketss=bspikes

inittime=3
endtime=16
def trace(myfun,overlap=.5):
    gp=[]
    ts=np.arange(inittime,endtime,overlap)
    startts=ts
    endts=ts+overlap
    for i in range(len(ts)):
        fr=myfun(t1=startts[i],t2=endts[i])    
        gp.append(fr)
    gp=np.array(gp).T
    fig, axs = plt.subplots(4,1, figsize=(12, 3))
    for k in range(4):
        axs[k].plot(startts+overlap/2,gp[k])
    plt.show()
    return startts+overlap/2,gp 

#myfun:
def window(t1=0,t2=1):
    # to avoid nans
    # I do not add ISI of neurons that do not spike in the window
    # and drop nans in the variance arrays
    t1=float(t1)
    t2=float(t2)
    
    window=[]
    for j in range(len(spiketss)):
        spikets=spiketss[j]
        spikets=spikets[(spikets>t1*second) & (spikets<t2*second)]
        window.append(spikets)
    #window complete
    meanISIs=[] #mean of ISIs, then var
    meanFREQs=[] #same more freqs
    for j in range(len(window)):#for each neuron
        #get mean(ISI_j)
        num_spikes=len(window[j])
        freq=num_spikes/(t2-t1)
        if freq!=0:#avoid division by zero
            meanISIs.append(1/freq)
        meanFREQs.append(freq)
    varmeanISI=np.var(meanISIs)
    varmeanFREQ=np.var(meanFREQs)

    varISIs=[] #var of ISIs, then mean
    varFREQs=[] #same for 1/ISIs
    for j in range(len(window)):
        ISIs=np.diff(window[j])
        varISIs.append(np.var(ISIs))
        varFREQs.append(np.var(1/ISIs))
    varISIs=np.array(varISIs)
    varFREQs=np.array(varFREQs) 
    varISIs=varISIs[~np.isnan(varISIs)]#dop nans
    varFREQs=varFREQs[~np.isnan(varFREQs)]
    meanvarISI=np.mean(varISIs)
    meanvarFREQ=np.mean(varFREQs)
    #return meanISIs,varISIs,meanFREQs,varFREQs
    return varmeanISI,meanvarISI,varmeanFREQ,meanvarFREQ




