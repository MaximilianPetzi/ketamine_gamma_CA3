import numpy as np
from scipy import signal
from termcolor import colored
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
    
    inittime=0
    ltptime=0
    resttime=0
    measuretime=3
    second=1000
    #h.tstop = (inittime+2*measuretime+ltptime)*second
    h.tstop = (inittime+ltptime+resttime+measuretime)*second
    Run.olmWash =  [0, 1]
    Run.basWash =  [1, 1]
    Run.pyrWashA = [1, 1]
    Run.pyrWashB = [1, 1]
    Run.washinT  = 10000*second  #default 1e3
    Run.washoutT = 8*second  #2e3
    #Run.kT=(inittime)*second  

    Run.pwwext=1
    Run.pwwT=(inittime)*second
    #Run.pfout=30
    #Run.LTPonT=(inittime)*second  
    #Run.LTPoffT=(inittime+ltptime)*second

    myparams=np.load("recfolder/myparams.npy", allow_pickle=True)
    if myparams[0]:
        print("It's real!")
        #Run.LTPonT=(inittime)*second 
    else:
        print("It's a simulation!")
        if myparams[3]==0:
            print("SETTING TIME TO ",h.tstop)
            Run.kT=(inittime+ltptime+resttime)*second #if 0, control, never
        else: 
            print("SETTING TIME TO ",0)
            Run.kT=(0)*second                   #if 1, instantly

    Run.fiwash = h.FInitializeHandler(1,Run.setwash)

    #my advance:
    h('proc advance() {nrnpython("myadvance()")}') #overwrite the advancefunction

    recvars=["thekiii"] #"F","mytsyn","myt"]
    #net.pyr_olm_AM[0].weight[1]
    myrec=[]
    for recvar in recvars:
        myrec.append([])
    #myrec2=[]
    Karr=[]
    Karr2=[]
    Parr=[]
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
            Parr.append(np.average(pwwhist()))
            Karr.append(np.average(whist()[0]))
            Karr2.append(np.average(whist()[1]))
            
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
        ar=[] 
        for i in range(20000):
            ar.append(net.pyr_pyr_AM[i].weight[1])  #pyr to pyr
        start=net.pyr.ncsidx["Adend3AMPAf"]
        end=net.pyr.nceidx["Adend3AMPAf"]
        ar2=[]
        for i in range(start,end):
            ar2.append(net.ncl[i].weight[1])        #noise to pyr
        if plot:
            plt.hist(ar,bins=bins,label="recurrent weights")
            plt.hist(ar2,bins=bins,label="outside to pyr weights")
            plt.legend()
            plt.show()
        return ar,ar2
    
    def pwwhist(bins=200,plot=False):#das kann weg
        ar=[] 
        for c in net.pyr.cell:
            ar.append(-1)#c["Adend3AMPAf"].pww) #noise-pyr
        if plot:
            plt.hist(ar,bins=bins,label="outside to pyr weights")
            plt.legend()
            plt.show()
        return ar

    def bandpower(f,p,start, end):# integrates a spectral power (input freqs and powers) from start to end in frequenzy space
        bpow=0
        for i in range(len(p)):
            if start<f[i] and f[i]<end: bpow+=p[i]*(f[1]-f[0])
        return bpow 

    import time
    timea=time.time()
    h.run()
    timeb=time.time()
    print("simulation time: ",timeb-timea)
    myrec=np.array(myrec)
    myparams=np.load("recfolder/myparams.npy", allow_pickle=True)
    if myparams[0]: #if name==main
        #plt.plot(myrec[1,1:]-myrec[1,:-1],color="blue")
        plt.figure(1)
        for i in range(len(recvars)):
            plt.plot(myrec[i],label=recvars[i])
        plt.legend()
        plt.xlabel("timestep")
        plt.title("records")
        plt.figure(2)
        net.rasterplot()
        net.calc_lfp()
        #times=np.arange(seconds*1e4)/1e4   
        data=net.vlfp.to_python() 
        dataff=np.copy(data)
        #data=data[7000:]
        data1=data[int(10*second*(inittime+ltptime+resttime)):int(10*second*(inittime+ltptime+resttime+measuretime))]
        #data2=data[int((inittime+measuretime+ltptime)*10*second):int((inittime+measuretime+ltptime+measuretime)*10*second)]
        
        #to test fft accuracy dependent on data length: dataa=dataff[7500:-20000];f,p=signal.welch(dataa,1e4,nperseg=len(dataa));plt.plot(f,p);plt.text(10,1, r'theta power(3-12 Hz)='+str(round(bandpower(f,p,3,12),3)), color="red");plt.text(40,1, r'gamma power(30-100 Hz)='+str(round(bandpower(f,p,30,100),3)),color="red");plt.xlim((0,60));plt.show()
        
        f,p=signal.welch(data1,1e4,nperseg=len(data1))
        plt.grid(True)
        plt.plot(f,p)
        plt.text(10,1, r'theta power(3-12 Hz)='+str(round(bandpower(f,p,3,12),3)), color="red")
        plt.text(40,1, r'gamma power(30-100 Hz)='+str(round(bandpower(f,p,30,100),3)),color="blue")
        plt.legend()
        plt.xlim((0,100))
        plt.xlabel("f[Hz]")
        plt.title("spectral power of lfp")
        
        plt.figure(3)
        xKarr=np.arange(len(Karr))*10
        #plt.plot(xKarr,Karr,label='recurrent')
        plt.plot(xKarr,Karr2,label='outside')
        #plt.plot(xKarr,Parr,label="pww")
        plt.legend()
        plt.ylabel("avg weight")
        plt.xlabel("time[ms]")
        plt.show()
        #spectral power

        myg = h.Graph()
        net.vlfp.plot(myg,h.dt)
        myg.exec_menu("View = plot")
        myg.exec_menu("New Axis")
    else:
        #Data=np.load("recfolder/Data.npy",allow_pickle=True)
        #Data[myparams[1],myparams[2]]=Karr
        #np.save("recfolder/Data.npy",Data)
        #np.save("recfolder/oldData.npy",Data)#backup for accidental simulation restart
        
        net.calc_lfp()
        data=net.vlfp.to_python() 
        data1=data[int(10*second*(inittime+ltptime+resttime)):int(10*second*(inittime+ltptime+resttime+measuretime))]
        #data2=data[int((inittime+measuretime+ltptime)*10*second):int((inittime+measuretime+ltptime+measuretime)*10*second)]
        f1,p1=signal.welch(data1,1e4,nperseg=len(data1))
        #f2,p2=signal.welch(data2,1e4,nperseg=len(data2)) 

        Data=np.load("recfolder/Data.npy",allow_pickle=True)
        
        #print("myparams=",myparams)
        
        Data[myparams[1],myparams[2]]=[f1,p1,bandpower(f1,p1,3,12),bandpower(f1,p1,30,100)]
        #print("now dataij became",Data[myparams[1],myparams[2]])
        #Data[1,myparams[2]]=[f2,p2,bandpower(f2,p2,3,12),bandpower(f2,p2,30,100)]
        np.save("recfolder/Data.npy",Data)
        if myparams[1]==1 and myparams[2]==0:
            np.save("recfolder/firstsamplewithltp.npy",[data,whist()[1]])#also saves lfp over time and whist
        
        
        
