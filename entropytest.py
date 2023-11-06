import numpy as np
from PyCausality.TransferEntropy import TransferEntropy
import pandas as pd


yt=np.zeros(1000)
xt=np.zeros(1000)

idx=np.random.randint(0,990,100)
yt[idx]=np.random.randint(0,10,len(idx))
xt[idx+3]=yt[idx]


#yt=np.array([0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,2,0,0,0])
#xt=np.array([0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,2,0])
print(xt[:20])
print(yt[:20])
#yt=yt[:500]
#xt=xt[:500]
index=np.arange(len(xt))#array of times (in seconds)
df=pd.DataFrame({"xt":xt,"yt":yt},index=index)
#df.index = pd.to_datetime(df.index, unit='s') #this converts index into datetime units, 
#necessary to use window size and stride options 

causality = TransferEntropy(DF = df,
                                endog = 'yt',          # Dependent Variable
                                exog = 'xt',           # Independent Variable
                                lag = 3
)

TE = causality.nonlinear_TE(n_shuffles=100)
print("here",causality.results["TE_XY"])
print(TE)
#print(TE.results["TE_XY"])


