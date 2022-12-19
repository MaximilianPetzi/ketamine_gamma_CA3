    


n=10
stepsize=[0.25,0.25,1]
if __name__ == "__main__":
    import numpy as np
    import os
    import sys

    if os.path.exists("recfolder/FI.npy"):
        os.remove("recfolder/FI.npy")
    cells=["pyr","bas","olm"]

    Data=np.zeros((len(cells)),dtype="object")
    np.save("recfolder/FI",Data)
    for j in range(len(cells)):
        Data=np.load("recfolder/FI.npy",allow_pickle=True)
        data=np.zeros((n),dtype="object")
        Data[j]=data
        np.save("recfolder/FI",Data)
        for i in range(n):
            I=i*stepsize[j]
            commandstring="python2 my_mosinit.py "+str(I)+" "+cells[j]
            print(commandstring)
            os.system(commandstring)#script saves in .npy file the value
        
        #print("args:",sys.argv[1])
    #dat=np.load("recfolder/FI.npy")






