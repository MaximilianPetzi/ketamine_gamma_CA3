import numpy as np
from matplotlib import pyplot as plt
plt.style.use("seaborn-darkgrid")
spiketimes=np.load("recfolder/FI.npy")

Farr=[]
lengths=[]
for i in range(spiketimes.size):
    if spiketimes[i].size>1:
        Fvalue=len(spiketimes[i])/(spiketimes[i][-1]-spiketimes[i][0])
    else:   Fvalue=0
    if spiketimes[i].size==1: Fvalue=-1
    Farr.append(Fvalue)
    lengths.append(spiketimes[i].size)#number of spikes

print("number of spikes:")
print(lengths)
plt.plot(Farr)
plt.show()