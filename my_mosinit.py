

#ltp notes: somaAMPAf synapses are also used for noise it seems, synapse changes change presynaptic neuron spikes too

#noise sends events to somaAMPAf mechanisms. to prevent LTP, manage the events accordingly
#read netcon documentation and think about the LTP rule and when events should be triggered

solo=True

##############################################################################################
stimdur=150 
stepsize=.05 #stepsize of stimulus amplitudes
celltypes=["pyr","pyr","pyr","pyr","pyr","bas","olm"]
comps=["soma","Adend1","Adend2","Adend3","Bdend","soma","soma"]
if __name__ == "__main__":
    import os
    import string
    import sys
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
    Run.washinT  = 1e50  #default 1e3
    Run.washoutT = 2e50  #2e3
    Run.fiwash = h.FInitializeHandler(1,Run.setwash)

    class A:
        def volt(self,pop=net.pyr,comp="soma",plot=False,i=0):#trace of population average membrane potential at specific compartment. not sure if useful, but hey
            #returns voltage trace to plot with matplotlib
            volts = h.Vector(pop.cell[i].soma_volt.size())
            volts.add(getattr(pop.cell[i],comp+"_volt"))
            voltage_trace=numpy.array(volts.to_python())
            if plot:plt.plot(np.arange(len(voltage_trace))/10.,voltage_trace)
            plt.ylabel("voltage")
            plt.xlabel("t[ms]")
            plt.show()
            return voltage_trace
                
        def count(self,pop=net.pyr,t1=0.,t2=9999999999.,idx=None):
            spts=pop.spiketimes()
            second=1000.
            count=0
            for i in range(len(spts)):#neuron i
                for j in range(len(spts[i])):
                    if len(spts[i])>0:#if the neuron spikes
                        if spts[i][j]>int(second*t1) and spts[i][j]<int(second*t2):  #count only spikes with time after t1 and before t2
                            if idx==None or i==idx:
                                count+=1
            return count

    a=A()#creates analysis instance
    ####################################################
    #my event:
    Run.mystuff = h.FInitializeHandler(1,myevent_eventcallingfunction)
    ####################################################
    #my event:
    def myevent_eventcallingfunction():
        pass
        #h.CVode().event(0.7,my_event)
    def my_event():
        #print("hi from",h.t)
        #(see run)
        pass
    #h('proc advance() {nrnpython("myadvance()")}') #overwrite the advancefunction
 
    recvars=["rec_k","rec_k1"] #"F","mytsyn","myt"]
    myrec=[]
    for recvar in recvars:
        myrec.append([])
    #myrec2=[]
    def myadvance():
        #print('my advance, h.t = {}, rec= {}'.format(h.t,net.pyr.cell[0].somaAMPAf.syn.rec_k))
        #print('F={}'.format(net.pyr.cell[0].somaAMPAf.syn.F))
        for irec,recvar in enumerate(recvars):
            myrec[irec].append(99)#getattr(net.pyr.cell[0].somaAMPAf.syn,recvar)) #getattr acts like ...syn.recvar
        #print('weight={}'.format(net.pyr_bas_NM[1].weight[0]))
        
        #myrec2.append([])  #for later , here , 
        #for iw in range(10):
        #    myrec2[-1].append(net.pyr_olm_AM[iw].weight[0])
        h.fadvance()


    ###################################################
    from matplotlib import pyplot as plt
    plt.style.use("seaborn-darkgrid")
    import numpy as np
    if solo:
        stimamp=20.
        celltype="olm"
        comp="soma"
    
    else: #if simulation
        stimidx=int(sys.argv[1])
        stimamp=stimidx*stepsize
        cellidx=int(sys.argv[2])
        celltype=celltypes[cellidx]
        comp=comps[cellidx]
    
    net.celltype=celltype
    
    stim = h.IClamp(getattr(getattr(net,celltype).cell[0],comp)(.5)) #PAY ATTENTION TO WHERE IN THE SEGMENT YOU INJECT (.5??)
    stim.delay = 50
    stim.dur = stimdur
    h.tstop = stim.dur+stim.delay+50
    stim.amp = stimamp

    h.run()
    
    if solo:
        a.volt(pop=getattr(net,celltype),plot=True)
    else:
        Data=np.load("recfolder/FI.npy")
        Data[cellidx,stimidx]=a.count(pop=getattr(net,celltype))
        np.save("recfolder/FI",Data)


