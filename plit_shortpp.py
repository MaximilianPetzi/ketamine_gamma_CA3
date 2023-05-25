#plots data from seedavg.py simulation
import numpy as np
from matplotlib import pyplot as plt
from seedavg import *
import seaborn as sns
import scipy.stats

Data=np.load("recfolder/oldData.npy",allow_pickle=True)      #change back to oldData.npy
DatShape=np.shape(Data)[0],np.shape(Data)[1],np.shape(Data)[2],np.shape(Data)[3],np.shape(Data)[4],1
DatShape2=np.shape(Data)[0],np.shape(Data)[1],np.shape(Data)[2],np.shape(Data)[3],np.shape(Data)[4],2
Dat=np.ones(DatShape)*-1      
Dat2=np.ones(DatShape2)*-1 
print("shape of Dat2 and therefore dat2 is: \n ",np.shape(Dat2))

for a in range(len(Data)):
    for b in range(len(Data[0])):
        for c in range(len(Data[0,0])):
            for d in range(len(Data[0,0,0])):
                for e in range(len(Data[0,0,0,0])):     #build proper Tensor
                    Dat[a,b,c,d,e]=Data[a,b,c,d,e][1]      #full recordings, not saved anymore    
                    Dat2[a,b,c,d,e,:]=Data[a,b,c,d,e][2:4]  #theta and gamma power
dat=np.array(Dat,dtype=float)
dat2=np.array(Dat2,dtype=float)
dat2=np.transpose(dat2,axes=[0,1,2,4,3,5])
imax=len(dat2[0,0])
jmax=len(dat2[0,0,0])
kmax=len(dat2[0,0,0,0])
import matplotlib.colors

def difs():
    dif2=dat2[1]-dat2[0]
    for i in range(imax):#rec, each a different figure
        fig=plt.figure(i,figsize=(3,3),dpi=80)
        for j in range(jmax):
            for k in range(kmax):
                #j is ext, row? in subplot
                #k is soma, column in subplot
                pows=np.average(dif2,axis=1)
                pows_std=np.std(dif2,axis=1)/(len(dif2[0])-1)**.5 #sample error estimate or whatever
                x=np.arange(len(pows))/1.+1.
                cmap = plt.cm.rainbow
                norm = matplotlib.colors.Normalize(vmin=2, vmax=4)
                #jlist=1+np.arange(0,4)*0.25
                #klist=1+np.arange(0,4)*0.25
                plt.scatter(j,k,color=cmap(norm(pows[i,j,k,1])),label="gamma power(30-100 Hz)")#first index=0 means control trial, last index=1 means gamma
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])  # only needed for matplotlib < 3.1
        fig.colorbar(sm)
        plt.title("rec="+str(i))
    plt.show()

def allplots(boxplot=True):

    pows=np.average(dat2,axis=1)
    pows_std=np.std(dat2,axis=1)/(len(dat2[0])-1)**.5 #sample error estimate or whatever
    x=np.arange(len(pows))/1.
    for k in range(kmax):#each a different figure #E
        fig, ax = plt.subplots(nrows=4, ncols=4, figsize=(10, 10))
        for nn in range(4):
            ax[3,nn].set_xlabel('control vs. ketamine')
            ax[nn,0].set_ylabel('gamma power')
        for j in range(jmax):# #D
            for i in range(imax):# #C
                #plt.subplot(imax,jmax,1+i+imax*j)
                if boxplot==False:
                    ax[i,j].plot(x,pows[:,i,j,k,1],label="gamma power(30-100 Hz)", color="black")#first index=0 means control trial, last index=1 means gamma
                    ax[i,j].errorbar(x=x,y=pows[:,i,j,k,1],yerr=pows_std[:,i,j,k,1],color="grey",fmt=".")
                else:
                    ax[i,j].boxplot([dat2[0,:,i,j,k,1]],positions=[0]) #for control trial, insert back: ,dat2[1,:,i,j,k,1]  and  # positions=[0,1] and
                sns.stripplot(data=[dat2[0,:,i,j,k,1]], jitter=.08, color='black', ax=ax[i,j],size=3) #,dat2[1,:,i,j,k,1]
                ax[i,j].set_ylim([1.5,4.5])
                #plt.xlabel("ctrl. vs. ket.")
                #ax[i,j].text(0.2,4.3,str(i)+str(j)+str(k))#rec,ext,som=xxx
                ax[i,j].text(-0.4,4.3,"rec:"+str(cpfp(i,j,k)[0])+", Loc:"+str(cpfp(i,j,k)[1]))
                #presult=scipy.stats.ttest_rel(a=dat2[0,:,i,j,k,1],b=dat2[1,:,i,j,k,1], axis=0)  for control trial, uncomment this and
                #ax[i,j].text(-0.4,4.1,"p="+"{:.1e}".format(presult.pvalue/2.))                     
        plt.subplots_adjust(left=None, bottom=None, right=1., top=1., wspace=None, hspace=None)
    
    fig.tight_layout(pad=2.0)
    plt.show()

allplots()

#transform into r readable format (CSV?)

gc=[]
gk=[]
rec=[]
ext=[]
for b in range(nB):#seed
    for c in range(nC):#rec
        for d in range(nD):#ext           check this again, questionable
            gc.append(dat2[0,b,c,d,0][1])
            gk.append(dat2[1,b,c,d,0][1])
            rec.append(cpfp(c,d,1)[0])
            ext.append(cpfp(c,d,1)[1])

import pandas as pd
df=pd.DataFrame({})
df["gammacontrol"]=gc
df["gammaketamine"]=gk
df["deltagamma"]=gk-gc
df["rec"]=rec
df["ext"]=ext
df.to_csv('recfolder/oldData.csv', index=True)
