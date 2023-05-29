import seedavg
withspec=seedavg.withspec #with or without saving f and p for full spectrum

multiplesims=False #set to True, if this is to be called by multiplesims.py, otherwise False
import numpy as np

from scipy import signal
from termcolor import colored
import pywt
import sys
import os
myterminal=open('myterminal.txt', 'a')
#sys.stdout=myterminal #set std output to file instead of terminal
#sys.stdout=sys.__stdout__ #set std out to terminal again

myparams=np.load("recfolder/myparams.npy", allow_pickle=True)


myparams[0]=True
if len(sys.argv)>1 and sys.argv[1]=="SIMUL":
    myparams[0]=False
np.save("recfolder/myparams.npy", myparams)

if True:
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
    
    inittime=3. #back to 3
    ltptime=0
    resttime=0
    measuretime=3. #should be fine ca
    second=1000.
    endtime=inittime+ltptime+resttime+measuretime
    #h.tstop = (inittime+2*measuretime+ltptime)*second
    h.tstop = (inittime+ltptime+resttime+measuretime)*second
    Run.olmWash =  [0, 1]
    Run.basWash =  [1, 1]
    Run.pyrWashA = [1, 1]
    Run.pyrWashB = [1, 1]
    Run.washinT  = 80*second  #default 1e3
    Run.washoutT = 90*second  #2e3
    #Run.kT=(inittime)*second  
    #Run.kout=2
    #Run.LTPonT=(inittime)*second  
    #Run.LTPoffT=(inittime+ltptime)*second

    myparams=np.load("recfolder/myparams.npy", allow_pickle=True)
    
    if myparams[0]:
        print("It's real!")
        Run.pwwT=0
        #Run.pwwT2=8000
        #Run.pwwT3=10000
        Run.pwwext=1
        Run.pwwrec=38.5          #25 normal, 28 seizure   38: breaks 20% of the time- 39: breaks always
        #Run.pww2ext=2.7
        #Run.pww3ext=3.5
    else:
        print("It's a simulation!")
        if myparams[1]==1 or seedavg.nA==1:#ketamine trial  bit of a weird way of fixing accidentally only doing control trials
            Run.pwwT=0 #pww changed from beginning
            Run.pwwrec=myparams[5+3]
            Run.pwwext=myparams[5+4]
            #Run.pwwsom=myparams[5+4]  
            pass
        else: #control trail
            pass #change nothing

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
               
        if net.nnn%1000==0:
            Parr.append(np.average(a.pwwhist()))
            Karr.append(np.average(a.whist()[0]))
            Karr2.append(np.average(a.whist()[1]))
            
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

    class A:#methods that can be used after net is run. some may be used internally too. 

        def calc_volt(self,pop=net.pyr,comp="soma",plot=False):#trace of population average membrane potential at specific compartment. not sure if useful, but hey
            #returns voltage trace to plot with matplotlib
            volts = h.Vector(pop.cell[0].soma_volt.size()) #lets see if this works lol
            for cell in pop.cell: 
                volts.add(getattr(cell,comp+"_volt"))
            volts.div(len(pop.cell)) # normalize by amount of pyr cells
            voltage_trace=numpy.array(volts.to_python())
            if plot:plt.plot(voltage_trace);plt.show()
            return voltage_trace
        
        def volt(self,pop=net.pyr,comp="soma",plot=False,i=0):#trace of population average membrane potential at specific compartment. not sure if useful, but hey
            #returns voltage trace to plot with matplotlib
            volts = h.Vector(pop.cell[i].soma_volt.size())
            volts.add(getattr(pop.cell[i],comp+"_volt"))
            voltage_trace=numpy.array(volts.to_python())
            if plot:plt.plot(voltage_trace);plt.show()
            return voltage_trace
        
        def volts(self,pop=net.pyr,comp="soma",i1=0,i2=7,linewidth=.5,offset=20):
            #plots a bunch of voltage traces at once, from index i1 to i2
            for i in range(i1,i2):
                plt.plot(offset*(i-i1)+np.clip(a.volt(pop=pop,comp=comp,plot=False,i=i),-110,-40),linewidth=linewidth) #add different number to each trace
            plt.show()

        def raster(self,pop=net.pyr,maxtick=20,my_s=.5):
            spikets=pop.spiketimes()
            for i in range(len(spikets)):
                if len(spikets)>0:  
                    idxar=np.ones(len(spikets[i]))*i
                    plt.scatter(spikets[i],idxar,s=my_s,color="red")
            plt.xlabel("time")
            plt.ylabel("neuron index")
            plt.title("my rasterplot")
            ax = plt.gca()#gets current axis
            
            ax.yaxis.set_ticks(range(0,maxtick))#set ticks at every integer (every neuron id)
            # enable the horizontal grid
            plt.grid(axis='y', linestyle='-')

            plt.show()
            return spikets #list of lists of spikes
    
        def count(self,pop=net.pyr,t1=inittime+ltptime+resttime,t2=inittime+ltptime+resttime+measuretime,idx=None):
            #counts number of spikes between times, almost superfluous because of freq
            #BUT note, that they calculate slightly different things, hence the difference in results
            #default: count pyr spikes during measuretime
            #if idx is not set, count all spikes of population
            #if idx is set, count only spikes of neuron with given index
            spts=pop.spiketimes()
            count=0
            for i in range(len(spts)):#neuron i
                for j in range(len(spts[i])):
                    if len(spts[i])>0:#if the neuron spikes
                        if spts[i][j]>int(second*t1) and spts[i][j]<int(second*t2):  #count only spikes with time after t1 and before t2
                            if idx==None or i==idx:
                                count+=1
            return count

        def freq(self,t1=inittime+ltptime+resttime,t2=inittime+ltptime+resttime+measuretime,pop=net.pyr,): 
            # prints avg spiking frequency of given population, 
            # between times t1 and t2 (default: pyr freq during measure time
            spikets=pop.spiketimes()
            spikets=spikets #only take ones between t1 and t2
            for i in range(len(spikets)):
                spi=spikets[i]
                spikets[i]=spi[spi>t1*second]
                spi=spikets[i]
                spikets[i]=spi[spi<t2*second]
            seconds=float(t2-t1)/1000*second
            nspikes=np.array([len(spiket) for spiket in spikets])/seconds
            n=len(spikets)
            mu=np.mean(nspikes)
            #sys.stdout=myterminal #set std output to file instead of terminal
            print("avg freq=",mu,"+/-", numpy.std(nspikes)*n/(n-1)/(n)**.5) #gets printed to file
            #sys.stdout=sys.__stdout__ #set std out to terminal again
            #return nspikes
            return mu

        def whist(self,bins=200,plot=False):
            #plots histogram of pyr weights, if plot=True. 
            #returns list of recurrent and external weights
            ar=[] 
            for i in range(20000):#number of connections (multiply convergence nr with number of cells)
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
        
        def pwwhist(self,bins=200,plot=False):#not used i think
            ar=[] 
            for c in net.pyr.cell:
                ar.append(-1)#c["Adend3AMPAf"].pww) #noise-pyr
            if plot:
                plt.hist(ar,bins=bins,label="outside to pyr weights")
                plt.legend()
                plt.show()
            return ar

        def bandpower(self,f,p,start, end):#using calcbandpower is simpler 
            #integrates a spectral power (input freqs and powers) from start to end in frequency space
            bpow=0
            for i in range(len(p)):
                if start<f[i] and f[i]<end: bpow+=p[i]*(f[1]-f[0])
            return bpow 
        
        def gammatrace(self,overlap=.6):
            gp=[]
            #default overlap is .25 in seconds, goes both ways

            x=np.linspace(overlap,endtime-overlap,endtime*10)#times
            for i in range(len(x)):
                gp.append(a.power(x[i]-overlap,x[i]+overlap))
            plt.plot(x,gp);plt.show()
            return x,gp

        def freqtrace(self,overlap=.6,pop=net.pyr):
            gp=[]
            #default overlap is .25 in seconds, goes both ways

            x=np.linspace(overlap,endtime-overlap,endtime*10)#times
            for i in range(len(x)):
                fr=a.freq(x[i]-overlap,x[i]+overlap,pop=pop)
                gp.append(fr)
            plt.plot(x,gp);plt.show()
            return x,gp
        
        def spectrum(self):
            pass
            #f, t, Sxx = signal.spectrogram(x, fs, return_onesided=False)
            #plt.pcolormesh(t, fftshift(f), fftshift(Sxx, axes=0), shading='gouraud')
            #plt.ylabel('Frequency [Hz]')
            #plt.xlabel('Time [sec]')
            #plt.show()

        def power(self,t1=inittime+ltptime+resttime,t2=inittime+ltptime+resttime+measuretime,f1=30,f2=100):#calculates band power of pyr population
            #default: gamma power during measuretime
            #t1,t2: start and end time of LFP
            #f1,f2: frequency limit of power spectrum integration
            datac=data[int(10*second*t1):int(10*second*t2)]
            f,p=signal.welch(datac,1e4,nperseg=len(datac))
            return a.bandpower(f,p,f1,f2)
    a=A()#creates analysis instance
    import time
    timea=time.time()
    h.run()
    timeb=time.time()
    print("simulation time: ",timeb-timea)
    myrec=np.array(myrec)
    myparams=np.load("recfolder/myparams.npy", allow_pickle=True)

    #uncomment for multiplesims.py:
    

    if myparams[0]: #if name==main
        #plt.plot(myrec[1,1:]-myrec[1,:-1],color="blue")
        if False:
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
        
        
        if multiplesims:#print to file
            myfreq=a.freq(3,6)
            mygamma=a.power(3,6)
            myterminal=open('myterminal.txt', 'a')
            sys.stdout=myterminal
            print(myfreq,mygamma)
            myterminal.close()
            sys.stdout=sys.__stdout__
            sys.exit()

        f,p=signal.welch(data1,1e4,nperseg=len(data1))
        plt.grid(True)
        plt.plot(f,p)
        plt.text(10,1, r'theta power(3-12 Hz)='+str(round(a.bandpower(f,p,3,12),3)), color="red")
        plt.text(40,1.2, r'gamma power(30-100 Hz)='+str(round(a.bandpower(f,p,30,100),3)),color="blue")
        plt.legend()
        plt.xlim((0,100))
        plt.xlabel("f[Hz]")
        plt.title("spectral power of lfp")
        
        #plt.figure(3)
        xKarr=np.arange(len(Karr))*10
        #plt.plot(xKarr,Karr,label='recurrent')
        #plt.plot(xKarr,Karr2,label='outside')
        #plt.plot(xKarr,Parr,label="pww")
        #plt.legend()
        #plt.ylabel("avg weight")
        #plt.xlabel("time[ms]")
        plt.show()
        #spectral power

        myg = h.Graph()
        net.vlfp.plot(myg,h.dt)
        myg.exec_menu("View = plot")
        myg.exec_menu("New Axis")
    else:
        net.calc_lfp()
        data=net.vlfp.to_python() 
        data1=data[int(10*second*(inittime+ltptime+resttime)):int(10*second*(inittime+ltptime+resttime+measuretime))]
        #data2=data[int((inittime+measuretime+ltptime)*10*second):int((inittime+measuretime+ltptime+measuretime)*10*second)]
        f1,p1=signal.welch(data1,1e4,nperseg=len(data1))
        #f2,p2=signal.welch(data2,1e4,nperseg=len(data2)) 
        Data=np.load("recfolder/Data.npy",allow_pickle=True)
        
        #print("myparams=",myparams)
        if withspec:
            Data[myparams[1],myparams[2],myparams[3],myparams[4],myparams[5]]=[f1,p1,a.bandpower(f1,p1,3,12),a.bandpower(f1,p1,30,100)]
        else:
            Data[myparams[1],myparams[2],myparams[3],myparams[4],myparams[5]]=[-2,-3,a.bandpower(f1,p1,3,12),a.bandpower(f1,p1,30,100)]
        #print("now dataij became",Data[myparams[1],myparams[2]])
        #Data[1,myparams[2]]=[f2,p2,bandpower(f2,p2,3,12),bandpower(f2,p2,30,100)]
        np.save("recfolder/Data.npy",Data)
        if myparams[1]==1 and myparams[2]==0:
            np.save("recfolder/firstsamplewithltp.npy",[data,a.whist()[1]])#also saves lfp over time and whist
        
        
        
