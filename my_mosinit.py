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
    Run.washinT  = 1e2  #default 1e3
    Run.washoutT = 2e2  #2e3
    Run.fiwash = h.FInitializeHandler(1,Run.setwash)


    h.tstop = 4e2   #3e3
    h.run()
    net.rasterplot()
    net.calc_lfp()
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
