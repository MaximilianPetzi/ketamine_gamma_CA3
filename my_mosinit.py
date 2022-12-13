#let's start
if __name__ == "__main__":
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

    # setup washin,washout
    import run as Run
    Run.olmWash =  [0, 1]
    Run.basWash =  [1, 1]
    Run.pyrWashA = [1, 1]
    Run.pyrWashB = [1, 1]
    Run.washinT  = 0e55  #default 1e3
    Run.washoutT = 2e55  #2e3
    Run.fiwash = h.FInitializeHandler(1,Run.setwash)

    #my advance:
    h('proc advance() {nrnpython("myadvance()")}') #overwrite the advancefunction

    recvars=["thek"] #"F","mytsyn","myt"]
    #net.pyr_olm_AM[0].weight[1]
    myrec=[]
    for recvar in recvars:
        myrec.append([])
    #myrec2=[]

    def myadvance():
        #print('my advance, h.t = {}, rec= {}'.format(h.t,net.pyr.cell[0].somaAMPAf.syn.rec_k))
        #print('F={}'.format(net.pyr.cell[0].somaAMPAf.syn.F))
        for irec,recvar in enumerate(recvars):
            if recvar=="w":
                myrec[irec].append(net.pyr_pyr_AM[0].weight[0]) #getattr acts like ...syn.recvar
            if recvar=="thek":
                myrec[irec].append(net.pyr_pyr_AM[0].weight[1])
        #print('weight={}'.format(net.pyr_bas_NM[1].weight[0]))
        
        #myrec2.append([])  #for later , here , 
        #for iw in range(10):
        #    myrec2[-1].append(net.pyr_olm_AM[iw].weight[0])
        h.fadvance()
    
    seconds=6
    h.tstop = seconds*1000   #3e3
    h.run()

    from matplotlib import pyplot as plt
    plt.style.use("seaborn-darkgrid")
    import numpy as np
    myrec=np.array(myrec)
    #plt.plot(myrec[1,1:]-myrec[1,:-1],color="blue")
    plt.figure(1)
    for i in range(len(recvars)):
        pass
        #plt.plot(myrec[i],label=recvars[i])
    plt.legend()
    plt.title("record")
    #plt.figure(2)
    #plt.plot(myrec2)
    #plt.show()

    net.rasterplot()
    net.calc_lfp()
    from scipy import signal
    times=np.arange(seconds*1e4)/1e4   
    data=net.vlfp.to_python() 
    sin1=np.sin(2*np.pi*10*times) 
    f,p=signal.welch(data,1e4,nperseg=4000) 
    plt.plot(f,p);plt.show()
    #spectral power

    myg = h.Graph()
    net.vlfp.plot(myg,h.dt)
    
    #import numpy as np
    #lfpar=net.lfp
    
    #def movavg(inputar,kernellen):
    #    outputar=[]
    #    for i in range(len(inputar)-kernellen):
    #        outputar.append(np.average(inputar[i:i+kernellen]))
    #    return outputar

    #print np.average(lfpar[10000:50000])
    #print np.average(lfpar[50000:60000])
    #print np.average(lfpar[60000:70000])
    #print np.average(lfpar[70000:100000])
    #from matplotlib import pyplot as plt
    #plt.plot(movavg(lfpar,4500))
    #plt.show()
    myg.exec_menu("View = plot")
    myg.exec_menu("New Axis")
