import numpy as np

N=800
def embed(N,a,b):
    pos=list(np.zeros((0,2)))
    for k in range(N):
        pos.append([k%a,int(k/a)])
    return pos

print(embed(20,4,5))