#experiment branch

#ltp notes: somaAMPAf synapses are also used for noise it seems, synapse changes change presynaptic neuron spikes too
#ltp happens in NMDA, not in AMPA, i think, check where im supposed to include it

#noise sends events to somaAMPAf mechanisms. to prevent LTP, manage the events accordingly
#read netcon documentation and think about the LTP rule and when events should be triggered
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
    Run.washinT  = 1e50  #default 1e3
    Run.washoutT = 2e50  #2e3
    Run.fiwash = h.FInitializeHandler(1,Run.setwash)

#todo:
    # access weights: print(net.pyr_bas_NM[i].weight[0])
    # access pre and postsynaptic activity for weight


####################################################
#my event:
    Run.mystuff = h.FInitializeHandler(1,myevent_eventcallingfunction)
    ####################################################
    #my event:
    def myevent_eventcallingfunction():
        h.CVode().event(0.7,my_event)
    def my_event():
        #print("hi from",h.t)
        #(see run)
        pass
    #access weight: print(net.pyr_bas_NM[i].weight[0])  (connection i)
    #access voltage: net.pyr.cell[j].Adend3_volt[4000]  (cell j, 4000ms)
    #need to capture spike with stdp learning rule
        ###################################################
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
            if recvar!="thek":
                myrec[irec].append(getattr(net.pyr.cell[0].somaAMPAf.syn,recvar)) #getattr acts like ...syn.recvar
            if recvar=="thek":
                myrec[irec].append(net.pyr_olm_AM[0].weight[1])
        #print('weight={}'.format(net.pyr_bas_NM[1].weight[0]))
        
        #myrec2.append([])  #for later , here , 
        #for iw in range(10):
        #    myrec2[-1].append(net.pyr_olm_AM[iw].weight[0])
        h.fadvance()


###################################################
    h.tstop = 300   #3e3
    stimp=[]#Pyramidal 
    for i in range(5):
        stimp.append(h.IClamp(net.pyr.cell[0].soma(.5)))
        stimp[i].delay = 100+4*i
        stimp[i].dur = 3
        stimp[i].amp = 0

    stimp0=h.IClamp(net.pyr.cell[0].soma(.5))
    stimp0.delay = 100
    stimp0.dur = 50
    stimp0.amp = .1

    stimo=[]#OLM
    for i in range(5):
        stimo.append(h.IClamp(net.olm.cell[0].soma(.5)))
        stimo[i].delay = 100+10*i+50
        stimo[i].dur = 3
        stimo[i].amp = 0

    h.run()
    #net.rasterplot()
    from matplotlib import pyplot as plt
    plt.style.use("seaborn-darkgrid")
    import numpy as np
    myrec=np.array(myrec)
    #plt.plot(myrec[1,1:]-myrec[1,:-1],color="blue")
    plt.figure(1)
    for i in range(len(recvars)):
        plt.plot(myrec[i],label=recvars[i])
    plt.legend()
    plt.title("record")
    #plt.figure(2)
    #plt.plot(myrec2)
    plt.show()
    net.calc_lfp()
    net.calc_myvolt_pyr()
    net.calc_myvolt_olm()   #soma testen und mit pyr spikes vergleichen

    myg = h.Graph()
    myg2= h.Graph()
    #myg2.color(2)
    net.vmyvolt_array_pyr[0].plot(myg,h.dt)
    net.vmyvolt_array_olm[0].plot(myg2,h.dt)
    
    #myg2.label(80, 30, "g2")

##ctr+K+C/U
# myg = h.Graph()
# net.calc_lfp()
# net.vlfp.plot(myg,h.dt)
# myg2=h.Graph()
# myg.color(3) 
# net.calc_myvolt()
# net.vmyvolt_array[5].plot(myg,h.dt)



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
