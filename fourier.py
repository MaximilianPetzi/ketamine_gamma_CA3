
#plots data from seedavg.py simulation

import numpy as np
from matplotlib import pyplot as plt
from seedavg import *

Data=np.load("recfolder/Data.npy",allow_pickle=True)      #change back to oldData.npy
data=Data[0,:,0,0,0]
pows=[]
freqs=data[0][0]
for i in range(len(data)):
    pows.append(data[i][1])
pows=np.array(pows)

fig,ax=plt.subplots()
y=np.average(pows,axis=0)
ax.plot(freqs,y,color="black",linewidth=.5)
print(len(pows))
error=np.std(pows,axis=0)/(len(pows)-1)**.5
ax.fill_between(freqs, y-error, y+error,color="black",alpha=.3)
ax.set_xlim(0,100)

plt.show()