import numpy as np
import sys
myparams=np.load("recfolder/myparams.npy", allow_pickle=True)
myparams[0]=True
if len(sys.argv)>1 and sys.argv[1]=="SIMUL":
    myparams[0]=False
np.save("recfolder/myparams.npy", myparams)

if True:
    import sys
    import os
    import string

    from neuron import *
    h("strdef simname, allfiles, simfiles, output_file, datestr, uname, osname, comment")
    h.simname=simname = "mtlhpc"
    h.allfiles=allfiles = "geom.hoc pyinit.py geom.py network.py params.py run.py"
    h.simfiles=simfiles = "pyinit.py geom.py network.py params.py run.py"
    h("runnum=1")
    runnum = 1.0
    h.datestr=datestr = "11may20"
    h.output_file=output_file = "data/11may20.05"
    h.uname=uname = "x86_64"
    h.osname=osname="linux"
    h("templates_loaded=0")
    templates_loaded=0
    h("xwindows=1.0")
    xwindows = 1.0

    h.xopen("nrnoc.hoc")
    h.xopen("init.hoc")

    from pyinit import *
    from geom import *
    from network import *
    
    from params import *
    from run import *

    # experiment setup
    import run as Run
    Run.olmWash =  [0, 1]
    Run.basWash =  [1, 1]
    Run.pyrWashA = [1, 1]
    Run.pyrWashB = [1, 1]
    Run.washinT  = 0e3  #default 1e3
    Run.LTPonT=0*1000
    Run.LTPoffT=10*1000
    
    
    h.tstop = 2*1000   #3e3

    myparams=np.load("recfolder/myparams.npy", allow_pickle=True)
    if myparams[0]:
        Run.washoutT = h.tstop*0  #2e3
    else:
        #that means that a myparams file exists and this is part of a seedavg simulation
        Run.washoutT = h.tstop*float(myparams[3])  #2e3

    Run.fiwash = h.FInitializeHandler(1,Run.setwash)

    #my advance:
    h('proc advance() {nrnpython("myadvance()")}') #overwrite the advancefunction

    recvars=["thekl"] #"F","mytsyn","myt"]
    #net.pyr_olm_AM[0].weight[1]
    myrec=[]
    for recvar in recvars:
        myrec.append([])
    #myrec2=[]
    Karr=[]
    net.nnn=0

    def myadvance():
        #print('my advance, h.t = {}, rec= {}'.format(h.t,net.pyr.cell[0].somaAMPAf.syn.rec_k))
        #print('F={}'.format(net.pyr.cell[0].somaAMPAf.syn.F))
        for irec,recvar in enumerate(recvars):
            if recvar=="w":
                myrec[irec].append(net.pyr_pyr_AM[0].weight[0]) #getattr acts like ...syn.recvar
                #net.pyr_pyr_AM[0].weight[0]
            if recvar=="thek":
                myrec[irec].append(net.pyr_pyr_AM[0].weight[1])
        if net.nnn%100==0:
            Karr.append(np.average(whist()))
        net.nnn=net.nnn+1
        #print('weight={}'.format(net.pyr_bas_NM[1].weight[0]))
        #myrec2.append([])  #for later , here , 
        #for iw in range(10):
        #    myrec2[-1].append(net.pyr_olm_AM[iw].weight[0])
        h.fadvance()

    Run.mystuff = h.FInitializeHandler(1,myevent_eventcallingfunction) #(see run.py, myevent)



    from matplotlib import pyplot as plt
    plt.style.use("seaborn-darkgrid")
    import numpy as np

    def whist(bins=200,plot=False):#number of connections (multiply convergence nr with number of cells)
        ar=[]; 
        for i in range(20000):
            ar.append(net.pyr_pyr_AM[i].weight[1])
        if plot:
            plt.hist(ar,bins=bins)
            plt.show()
        return ar


    import time
    timea=time.time()
    h.run()
    timeb=time.time()
    print("simulation time: ",timeb-timea)
    myrec=np.array(myrec)
    myparams=np.load("recfolder/myparams.npy", allow_pickle=True)
    if myparams[0]: #if name==main
        #plt.plot(myrec[1,1:]-myrec[1,:-1],color="blue")
        #plt.figure(1)
        #for i in range(len(recvars)):
        #    plt.plot(myrec[i],label=recvars[i])
        #plt.legend()
        #plt.xlabel("timestep")
        #plt.title("records")
        #plt.figure(2)
        net.rasterplot()
        net.calc_lfp()
        from scipy import signal

        #times=np.arange(seconds*1e4)/1e4   
        data=net.vlfp.to_python() 
        data1=data[:5000]
        data2=data[10000:]
        #data1=data[:halflen]
        #sin1=np.sin(2*np.pi*10*times) 
        print("signal length is ", len(data))
        f1,p1=signal.welch(data,1e4,nperseg=len(data)) 
        #f2,p2=signal.welch(data2,1e4,nperseg=len(data2)) 
        plt.plot(f1,p1,label="before")
        #plt.plot(f2,p2,label="after")
        plt.legend()
        plt.xlim((0,60))
        plt.xlabel("f[Hz]")
        plt.title("spectral power of lfp")

        plt.figure(3)
        plt.plot(Karr)
        plt.title("avg weight over time")
        plt.show()
        #spectral power

        myg = h.Graph()
        net.vlfp.plot(myg,h.dt)
        myg.exec_menu("View = plot")
        myg.exec_menu("New Axis")
    else:
        Data=np.load("recfolder/Data.npy",allow_pickle=True)
        #print(myparams)
        #print(myparams[1],myparams[2])
        #print(Data)
        #print(Data[myparams[1],myparams[2]])
        
        Data[myparams[1],myparams[2]]=Karr
        np.save("recfolder/Data.npy",Data)
        np.save("recfolder/oldData.npy",Data)#backup for accidental simulation restart
        
