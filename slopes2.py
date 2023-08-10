#this is to plot all gamma-krec slopes of big_delay simulations in one monstrous figure
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from seedavg import *
import seaborn as sns
import scipy.stats
import statsmodels.api as sm

nrows=4
Data=np.load("recfolder/Data.npy",allow_pickle=True)      #change back to oldData.npy
Caro=Car[:]
Data=Data[:,:,:,:,:-1]#HERE

DatShape=np.shape(Data)[0],np.shape(Data)[1],np.shape(Data)[2],np.shape(Data)[3],np.shape(Data)[4],1
DatShape2=np.shape(Data)[0],np.shape(Data)[1],np.shape(Data)[2],np.shape(Data)[3],np.shape(Data)[4],nrows


Dat=np.ones(DatShape)*-1      
Dat2=np.ones(DatShape2)*-1 

for a in range(len(Data)):
    for b in range(len(Data[0])):
        for c in range(len(Data[0,0])):
            for d in range(len(Data[0,0,0])):
                for e in range(len(Data[0,0,0,0])):     #build proper Tensor
                    Dat[a,b,c,d,e]=Data[a,b,c,d,e][1]      #full recordings, not saved anymore    
                    Dat2[a,b,c,d,e,:]=Data[a,b,c,d,e][4],Data[a,b,c,d,e][2],Data[a,b,c,d,e][7],Data[a,b,c,d,e][9]
#Data[myparams[1],myparams[2],myparams[3],myparams[4],myparams[5]]=[-1,-1,a.power(location="difference"),a.power(location="soma"),
#                a.freq(pop=net.pyr),a.freq(pop=net.bas),a.freq(pop=net.olm),a.rasterpower(pop=net.pyr),a.rasterpower(pop=net.bas),
#                a.synch(pop=net.pyr),a.synch(pop=net.pyr,binsize=10),a.synch(pop=net.pyr,binsize=20),a.synch(pop=net.bas),r["nTE_XY"],r] 
dat=np.array(Dat,dtype=float)
dat2=np.array(Dat2,dtype=float)



imax=len(dat2[0,0])
jmax=len(dat2[0,0,0])
kmax=len(dat2[0,0,0,0])
import matplotlib.colors
cmap = plt.get_cmap('jet')


def freqandgamma(): #plots avg over seeds, freq and gamma dependent on factor krec or kext, for rec and ext
    d=dat2[0,:,:,0,:,:]
    sh=np.shape(d)
    print(sh)
    da=np.average(d,axis=0)
    #now you have shape(da)=(seeds,Ca,rec/ext,f/gamma)
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))
    ax.set_ylabel(r'LFP $\gamma$')
    ax.set_xlabel(r'$k_{rec}$')
    for i in range(sh[2]):#=E=delay times
        #ax.scatter(Caro,da[:,i,1], s=2, c=color)
        #ax.plot(Caro,da[:,i,1], marker='o',markersize=2, color=color)
        mod = sm.OLS(Ear[i],da[:,i,1])
        res = mod.fit()
        print(res.)
    norm = mpl.colors.Normalize(vmin=0, vmax=45)#HERE
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    plt.colorbar(sm, ticks=Ear[:-1],label="delay [ms]")#HERE
    plt.show()

freqandgamma()


