import seedavg
withspec=seedavg.withspec #with or without saving f and p for full spectrum
multiplesims=False #set to True, if this is to be called by multiplesims.py, otherwise False
baronkenny=True
if True: #imports:
    import numpy as np
    from PyCausality.TransferEntropy import TransferEntropy
    import pandas as pd
    from scipy import signal
    import sys
    import os
    import pandas as pd
myterminal=open('myterminal.txt', 'a')
#sys.stdout=myterminal #set std output to file instead of terminal
#sys.stdout=sys.__stdout__ #set std out to terminal again
myparams=np.load("recfolder/myparams.npy", allow_pickle=True)
myparams[0]=True
if len(sys.argv)>1 and sys.argv[1]=="SIMUL":
    myparams[0]=False
np.save("recfolder/myparams.npy", myparams)
if True:
    if True: #imports

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
    
    inittime=3 #back to 3
    ltptime=0
    resttime=0
    measuretime=7#should be fine ca
    second=1000.
    endtime=inittime+ltptime+resttime+measuretime
    h.tstop = (inittime+ltptime+resttime+measuretime)*second
    Run.olmWash =  [0, 1]
    Run.basWash =  [1, 1]
    Run.pyrWashA = [1, 1]
    Run.pyrWashB = [1, 1]
    Run.washinT  = 1111*second  #default 1e3
    Run.washoutT = 1111*second  #2e3
    #Run.kT=(inittime)*second  
    #Run.kout=2
    #Run.LTPonT=(inittime)*second  
    #Run.LTPoffT=(inittime+ltptime)*second
    myparams=np.load("recfolder/myparams.npy", allow_pickle=True)

    if myparams[0]:
        print("It's real!")
        Run.pwwT=0
        Run.pwwext=1                
        Run.pwwrec=1     #was: 25 normal, 28 seizure   is: 38: breaks 20% of the time- 39: breaks always  
        #Run.pwwsom=1
        #Run.pww2ext=10
        #Run.pww2ext=1
        #Run.pww2rec=1  
    else:
        print("It's a simulation!")
        myterminal=open('myterminal.txt', 'a')
        sys.stdout=myterminal
        print(myparams[1:6])
        myterminal.close()
        sys.stdout=sys.__stdout__
        if myparams[1]==1 or seedavg.nA==1:#ketamine trial  bit of a weird way of fixing accidentally only doing control trials
            Run.pwwT=0 #pww changed from beginning
            if myparams[5+5]==1:
                Run.pwwrec=1#myparams[5+3] ###change back for kext krec sim
                Run.pwwext=myparams[5+3]
                pass
                
            if myparams[5+5]==2: #if E=2: change ext instead of rec
                Run.pwwext=myparams[5+3]
                Run.pwwrec=1 
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
            #print("avg freq=",mu,"+/-", numpy.std(nspikes)*n/(n-1)/(n)**.5) #gets printed to file
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
        
        def gammatrace(self,windowsize=.6):
            gp=[]
            #default windowsize is .25 in seconds, goes both ways

            x=np.linspace(windowsize,endtime-windowsize,endtime*10)#times
            for i in range(len(x)):
                gp.append(a.power(x[i]-windowsize,x[i]+windowsize))
            plt.plot(x,gp);plt.show()
            return x,gp

        def freqtrace(self,windowsize=.6,pop=net.pyr):
            gp=[]
            #default windowsize is .25 in seconds, goes both ways

            x=np.linspace(windowsize,endtime-windowsize,endtime*10)#times
            for i in range(len(x)):
                fr=a.freq(x[i]-windowsize,x[i]+windowsize,pop=pop)
                gp.append(fr)
            plt.plot(x,gp);plt.show()
            return x,gp

        #lfp-type variable here:
        def power(self,t1=inittime+ltptime+resttime,t2=inittime+ltptime+resttime+measuretime,f1=30,f2=100,location="difference",pop=net.pyr):
            #calculates band power of pyr population 
            #default: gamma power of Adend3-Bdend lfp during measuretime
            #location="soma" to use only soma potential instead of difference
            #t1,t2: start and end time of LFP
            #f1,f2: frequency limit of power spectrum integration
            if not pop==net.pyr:
                print("watch out, pyr used")
            if location=="difference":
                ddata=data    
            if location=="soma":
                ddata=datasoma
            datac=ddata[int(10*second*t1):int(10*second*t2)]
            f,p=signal.welch(datac,1e4,nperseg=len(datac))
            return a.bandpower(f,p,f1,f2)
        
        #pop variable here:
        def rasterpower(self,t1=inittime+ltptime+resttime,t2=inittime+ltptime+resttime+measuretime,f1=30,f2=100,pop=net.pyr):#calculates band power of pyr population
            #like a.power, but doesnt use pyr lfp, but uses spiketimes (specifically kernel density estimate for spike frequency)
            datar=a.spikefreq(pop=pop)
            
            datac=datar[int(10*second*t1):int(10*second*t2)] #now cut to only measured time
            f,p=signal.welch(datac,1e4,nperseg=len(datac))
            return a.bandpower(f,p,f1,f2)

        def spikefreq(self,pop=net.pyr):#similar to freqtrace, this is used for rasterpower
            spikets=np.concatenate(pop.spiketimes())
            xlength=len(data)#sets time length to full data in a.power()
            datar=np.zeros(xlength)#initialize smoothened spike density
            kernlen=50 #ms*10
            for i in range(len(spikets)):
                ri=int(10*spikets[i])
                if ri+kernlen<xlength:
                    datar[ri:ri+kernlen]+=1./kernlen
            #datar represents avg number of spikes per millisecond, estimated by rectangular kernel convolution
            return datar
        
        def binnedspikes(self,location=net.pyr,binsize=5,t1=inittime+ltptime+resttime,t2=inittime+ltptime+resttime+measuretime): #for Transfer Entropy, similar to spikefreq
            #counts spikes per bin, over whole population
            
            if isinstance(location,str): #if location is a string (meaning it is a synapse)
                pop=net.pyr  
                spiketss=pop.spiketimes_ext(syn=location)
            else:                        #if location is a population
                pop=location
                spiketss=pop.spiketimes()

            spikets=np.concatenate(spiketss)
            spikets=spikets[(spikets>t1*second) & (spikets<t2*second)] #only count the spikes between t1 and t2
            xlength=len(data)/binsize/10 #want only one entry per bin, not 50 (kernlen) like in spikefreq
            datar=np.zeros(xlength+1) #initialize binned spikes
            for i in range(len(spikets)):
                ri=int(spikets[i]/binsize) #up to 5ms first bin, up to 10ms second bin etc. 
                datar[ri]+=1
            datar=datar[int(t1*second/binsize):int(t2*second/binsize)] #only return the bins between t1 and t2
            return datar
        
        def binnedspikes_unavg(self,location=net.pyr,binsize=15,t1=inittime+ltptime+resttime,t2=inittime+ltptime+resttime+measuretime): 
            #un-averaged version of a.binnedspikes(), returns 2d array instead of 1d
            
            if isinstance(location,str): #if location is a string (meaning it is a synapse)
                pop=net.pyr  
                spiketss=pop.spiketimes_ext(syn=location)
            else:                        #if location is a population
                pop=location
                spiketss=pop.spiketimes()
            xlength=len(data[int(t1*second/binsize):int(t2*second/binsize)])              #a.binnedspikes_unavg()
            datarr=np.zeros((len(spiketss),xlength))
            
            for j in range(len(spiketss)):#for each neuron
                spikets=spiketss[j] #instead of concatenate, like above
                ###like above:##
                spikets=spikets[(spikets>t1*second) & (spikets<t2*second)]
                datar=np.zeros(len(data)/binsize/10+1) #i added one, because it sometimes tried accessing that index
                for i in range(len(spikets)):
                    ri=int(spikets[i]/binsize) 
                    datar[ri]+=1
                    # Traceback (most recent call last):
                    # File "stdin", line 1, in <module>
                    # File "my_mosinit.py", line 396, in te2
                    #     Xs=a.binnedspikes_unavg(location="Adend3AMPAf",t1=t1,t2=t2)
                    # File "my_mosinit.py", line 354, in binnedspikes_unavg
                    #     datar[ri]+=1
                    # IndexError: index 2133 is out of bounds for axis 0 with size 2133
                datar=datar[int(t1*second/binsize):int(t2*second/binsize)] 
                ################
                datarr[j,:]=datar
            return datarr
          
        
        def spec(self,datar,t1=inittime+ltptime+resttime,t2=inittime+ltptime+resttime+measuretime):
            datac=datar[int(10*second*t1):int(10*second*t2)]
            f,p=signal.welch(datac,1e4,nperseg=len(datac))
            plt.grid(True)
            plt.plot(f,p)
            plt.text(10,0.1, r'theta power(3-12 Hz)='+str(round(a.bandpower(f,p,3,12),3)), color="red")
            plt.text(40,0.1, r'gamma power(30-100 Hz)='+str(round(a.bandpower(f,p,30,100),3)),color="blue")
            plt.legend()
            plt.xlim((0,100))
            plt.xlabel("f[Hz]")
            plt.title("spectral power")
            plt.show()
        


        def te(self,pop1=net.bas,pop2=net.pyr,n_shuffles=30,lag=7,binsize=5,t1=inittime+ltptime+resttime,t2=inittime+ltptime+resttime+measuretime,bins=None):
            #uses max lag only
            #from pop1 to pop2 I think. default bas to pyr
            #switch X and Y
            
            X=a.binnedspikes(location=pop2,t1=t1,t2=t2,binsize=binsize)
            Y=a.binnedspikes(location=pop1,t1=t1,t2=t2,binsize=binsize)
            index=np.arange(len(X))
            df=pd.DataFrame({"xt":X,"yt":Y},index=index)
            causality = TransferEntropy(DF = df,
                                        endog = 'yt',          # Dependent Variable
                                        exog = 'xt',           # Independent Variable
                                        lag = lag
            )
            #TE = causality.nonlinear_TE(n_shuffles=n_shuffles,bins=bins)
            TE = causality.linear_TE(n_shuffles=n_shuffles)
            return causality.results
        
        #a.te2(pop1="somaAMPAf",pop2=net.pyr,n_shuffles=30,lag=1,nneurons=10,binsize=5)
        def te2(self,pop1="Adend3AMPAf",pop2=net.pyr,nneurons=800,n_shuffles=3,lag=1,binsize=15,t1=inittime+ltptime+resttime,t2=inittime+ltptime+resttime+measuretime,bins=None):
            #supposed to calculate te from external inputs, for each neuron. not sure if it detects anything
            tt=time.time()
            #calculates individual tes and then averages
            Xs=a.binnedspikes_unavg(location=pop1,t1=t1,t2=t2,binsize=binsize)
            Ys=a.binnedspikes_unavg(location=pop2,t1=t1,t2=t2,binsize=binsize)
            for i in range(nneurons):#for each neuron
                if i%10==0:print(i)
                X=Xs[i]
                Y=Ys[i]
                index=np.arange(len(X))
                df=pd.DataFrame({"xt":X,"yt":Y},index=index)
                causality = TransferEntropy(DF = df,
                                            endog = 'yt',          # Dependent Variable
                                            exog = 'xt',           # Independent Variable
                                            lag = lag
                )
                TE = causality.nonlinear_TE(n_shuffles=n_shuffles,bins=bins)
                if i==0:rdf=pd.DataFrame(causality.results)
                else:
                    rdf=rdf.append(causality.results)
                print(causality.results)
            print("te2 ran for "+str(time.time()-tt)+"seconds")
            return rdf,X,Y
            

        def lagcurve(self,lag1=1,lag2=30,pop1=net.pyr,pop2=net.olm,n_shuffles=50,t1=inittime+ltptime+resttime,t2=inittime+ltptime+resttime+measuretime):
            #plots TE dependent on lag, to find best lag
            TEs=np.zeros((lag2-lag1,2))#each entry is [TE(XZ),TE(YX)] for the current lag
            nTEs=np.zeros((lag2-lag1,2))#nTE
            for i in range(lag2-lag1):
                LAG=lag1+i
                res=a.te(lag=LAG,pop1=pop1,pop2=pop2,t1=t1,t2=t2,n_shuffles=n_shuffles)
                TEs[i,:]=res[["TE_XY","TE_YX"]]
                #nTEs[i,:]=res["r"][["nTE_XY","nTE_YX"]]
            plt.plot(TEs[:,0],label="X-->Y")
            plt.plot(TEs[:,1],label="Y-->X")
            #plt.plot(nTEs[:,0],label="X-->Y,normalized",alpha=.5)
            #plt.plot(nTEs[:,1],label="Y-->X,normalized",alpha=.5)
            plt.legend()
            plt.show()
            return TEs

        def trace(self,myfun,windowsize=.5,plot=False,pop=net.pyr): #trace of function asynch. windowsize in seconds
            gp=[]
            ts=np.arange(inittime,endtime,windowsize)
            startts=ts
            endts=ts+windowsize
            for i in range(len(ts)):
                fr=myfun(t1=startts[i],t2=endts[i],pop=pop)    
                gp.append(fr)
            gp=np.array(gp).T

            if plot:
                plt.plot(startts+windowsize/2,gp)
                plt.show()

            return startts+windowsize/2,gp #returns centers of sliding windows, and corresponding value

        #myfun:
        def asynch(self,t1=0,t2=1,pop=net.pyr): #returns 4 measures of asynchrony
            # to avoid nans,
            # I do not add ISI of neurons that do not spike in the window
            # and drop nans in the variance arrays
            t1=float(t1)
            t2=float(t2)
            spiketss=pop.spiketimes()
            
            window=[]
            for j in range(len(spiketss)):
                spikets=spiketss[j]
                spikets=spikets[(spikets>t1*second) & (spikets<t2*second)]
                window.append(spikets)
            #window complete
            meanISIs=[] #mean of ISIs, then var
            meanFREQs=[] #same more freqs
            for j in range(len(window)):#for each neuron
                #get mean(ISI_j)
                num_spikes=len(window[j])
                freq=num_spikes/(t2-t1)
                if freq!=0:#avoid division by zero
                    meanISIs.append(1/freq)
                meanFREQs.append(freq)
            varmeanISI=np.var(meanISIs)
            varmeanFREQ=np.var(meanFREQs)

            varISIs=[] #var of ISIs, then mean
            varFREQs=[] #same for 1/ISIs
            for j in range(len(window)):
                ISIs=np.diff(window[j])
                varISIs.append(np.var(ISIs))
                varFREQs.append(np.var(1/ISIs))
            varISIs=np.array(varISIs)
            varFREQs=np.array(varFREQs) 
            varISIs=varISIs[~np.isnan(varISIs)]#dop nans
            varFREQs=varFREQs[~np.isnan(varFREQs)]
            meanvarISI=np.mean(varISIs)
            meanvarFREQ=np.mean(varFREQs) 
            #return meanISIs,varISIs,meanFREQs,varFREQs
            results=varmeanISI,meanvarISI,varmeanFREQ,meanvarFREQ
            return results[3]

        def binvolts(self,pop=net.pyr,comp="soma",binsize=5,t1=inittime+ltptime+resttime,t2=inittime+ltptime+resttime+measuretime): #puts voltages of neurons in bins, returns matrix, for synch
            bar=np.zeros((len(pop.cell),int(len(a.volt(pop=pop,comp=comp,plot=False,i=0)[int(10000.0*t1):int(10000.0*t2)])/binsize)))
            for i in range(len(pop.cell)):#over all 800 pyr cells
                volt=a.volt(i=i)
                volt=volt[int(10000.0*t1):int(10000.0*t2)]
                for j in range(np.shape(bar)[1]):
                    bar[i,j]=np.mean(volt[binsize*j:(j+1)*binsize])
            return bar
        
        def synch(self,pop=net.pyr,comp="soma",binsize=5,t1=inittime+ltptime+resttime,t2=inittime+ltptime+resttime+measuretime):
            bar=a.binvolts(pop=pop,comp=comp,binsize=binsize,t1=t1,t2=t2)
            squaredsynch=np.var(np.mean(bar,axis=0))/np.mean(np.var(bar,axis=1))
            synch=squaredsynch**.5
            return synch
        
        def synchcurve(self,plot=False,pop=net.pyr,comp="soma",t1=inittime+ltptime+resttime,t2=inittime+ltptime+resttime+measuretime):
            xar=[5,10,20,40] #if you change that, change also the columns saved into dataframe in baronkenny part below
            Nsteps=len(xar)
            yar=np.ones(Nsteps)
            for i in range(Nsteps):
                yar[i]=a.synch(binsize=int(xar[i]),pop=pop,comp=comp,t1=t1,t2=t2)
            if plot==True:
                plt.plot(xar,yar,"b.")
                plt.xlabel(r"bin size (in $10^{-4}$s)")
                plt.ylabel("Synchrony")
                plt.show()
            return xar,yar


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
        net.calc_soma_lfp()
        #times=np.arange(seconds*1e4)/1e4   
        data=net.vlfp.to_python() 
        datasoma=net.vlfp_soma.to_python() 
        dataff=np.copy(data)
        #data=data[7000:]
        data1=data[int(10*second*(inittime+ltptime+resttime)):int(10*second*(inittime+ltptime+resttime+measuretime))]
        #data2=data[int((inittime+measuretime+ltptime)*10*second):int((inittime+measuretime+ltptime+measuretime)*10*second)]
        
        #to test fft accuracy dependent on data length: dataa=dataff[7500:-20000];f,p=signal.welch(dataa,1e4,nperseg=len(dataa));plt.plot(f,p);plt.text(10,1, r'theta power(3-12 Hz)='+str(round(bandpower(f,p,3,12),3)), color="red");plt.text(40,1, r'gamma power(30-100 Hz)='+str(round(bandpower(f,p,30,100),3)),color="red");plt.xlim((0,60));plt.show()
        
        
        if multiplesims:#print to file
            myfreq=a.freq()
            mygamma=a.power()
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
        net.calc_soma_lfp()
        data=net.vlfp.to_python() 
        datasoma=net.vlfp_soma.to_python() 
        data1=data[int(10*second*(inittime+ltptime+resttime)):int(10*second*(inittime+ltptime+resttime+measuretime))]
        #data2=data[int((inittime+measuretime+ltptime)*10*second):int((inittime+measuretime+ltptime+measuretime)*10*second)]
        f1,p1=signal.welch(data1,1e4,nperseg=len(data1))
        #f2,p2=signal.welch(data2,1e4,nperseg=len(data2)) 
        Data=np.load("recfolder/Data.npy",allow_pickle=True)
        
        #print("myparams=",myparams)
        if withspec:
            Data[myparams[1],myparams[2],myparams[3],myparams[4],myparams[5]]=[f1,p1,a.bandpower(f1,p1,3,12),a.bandpower(f1,p1,30,100)]
        else:
            r=a.te(pop1=net.bas,pop2=net.pyr)
            Data[myparams[1],myparams[2],myparams[3],myparams[4],myparams[5]]=[-1,-1,a.power(location="difference"),a.power(location="soma"),a.freq(pop=net.pyr),a.freq(pop=net.bas),a.freq(pop=net.olm),a.rasterpower(pop=net.pyr),a.rasterpower(pop=net.bas),r["nTE_XY"],r] 
            
            myterminal=open('myterminal.txt', 'a')
            sys.stdout=myterminal
            print("at ",myparams[3],myparams[5],"and ext/rec=",Run.pwwext,Run.pwwrec, "\nI measured freq/gamma=",a.freq(),a.bandpower(f1,p1,30,100))
            myterminal.close()
            sys.stdout=sys.__stdout__
        if baronkenny:
            res1=a.trace(a.asynch)
            res2=a.trace(a.power)
            asynch_col=res1[1]
            time_col=res1[0]
            gamma_col=res2[1]
            pfreq_col=a.trace(a.freq,pop=net.pyr)[1]
            bfreq_col=a.trace(a.freq,pop=net.bas)[1]
            ofreq_col=a.trace(a.freq,pop=net.olm)[1]
            rasterpower_col=a.trace(a.rasterpower,pop=net.pyr)[1]
            krec_col=np.ones(len(time_col))*Run.pwwrec
            kext_col=np.ones(len(time_col))*Run.pwwext
            nTE_col=np.ones(len(time_col))*float(r["nTE_XY"])
            pval_col=np.ones(len(time_col))*float(r["p_value_XY"])

            psynchx,psynchy=a.synchcurve(pop=net.pyr)
            psynch0_col=np.ones(len(time_col))*psynchy[0]     #gotta change that every time you change bins
            psynch1_col=np.ones(len(time_col))*psynchy[1]
            psynch2_col=np.ones(len(time_col))*psynchy[2]
            psynch3_col=np.ones(len(time_col))*psynchy[3]

            bsynchx,bsynchy=a.synchcurve(pop=net.bas)
            bsynch0_col=np.ones(len(time_col))*bsynchy[0]     #gotta change that every time you change bins
            bsynch1_col=np.ones(len(time_col))*bsynchy[1]
            bsynch2_col=np.ones(len(time_col))*bsynchy[2]
            bsynch3_col=np.ones(len(time_col))*bsynchy[3]
            msgain_col=np.ones(len(time_col))*float(net.OLMGain)

            brasterpower_col=a.trace(a.rasterpower,pop=net.bas)[1]
            if not os.path.exists("recfolder/barondata"):#first iteration creates new data file
                run_col=np.ones(len(time_col))*1
                mydf=pd.DataFrame({"bsynch0":bsynch0_col,"bsynch1":bsynch1_col,"bsynch2":bsynch2_col,"bsynch3":bsynch3_col,"psynch0":psynch0_col,"psynch1":psynch1_col,"psynch2":psynch2_col,"psynch3":psynch3_col,"msgain":msgain_col,"nTE":nTE_col,"pval":pval_col,"pfreq":pfreq_col,"bfreq":bfreq_col,"ofreq":ofreq_col,"gamma":gamma_col,"rasterpower":rasterpower_col,"asynch":asynch_col,"kext":kext_col,"krec":krec_col,"time":time_col,"run":run_col,"brasterpower":brasterpower_col})
                mydf.to_csv("recfolder/barondata",index=False)
                print("saved first dataframe:")
                print(mydf)
            else: #consecutive iterations append data
                prevdf=pd.read_csv("recfolder/barondata")
                run_col=np.ones(len(time_col))*(prevdf["run"].iloc[-1]+1)
                mydf=pd.DataFrame({"bsynch0":bsynch0_col,"bsynch1":bsynch1_col,"bsynch2":bsynch2_col,"bsynch3":bsynch3_col,"psynch0":psynch0_col,"psynch1":psynch1_col,"psynch2":psynch2_col,"psynch3":psynch3_col,"msgain":msgain_col,"nTE":nTE_col,"pval":pval_col,"pfreq":pfreq_col,"bfreq":bfreq_col,"ofreq":ofreq_col,"gamma":gamma_col,"rasterpower":rasterpower_col,"asynch":asynch_col,"kext":kext_col,"krec":krec_col,"time":time_col,"run":run_col,"brasterpower":brasterpower_col})
                newdf=prevdf.append(mydf, ignore_index=True)
                newdf.to_csv("recfolder/barondata",index=False)
                print(newdf)
        #print("now dataij became",Data[myparams[1],myparams[2]])
        #Data[1,myparams[2]]=[f2,p2,bandpower(f2,p2,3,12),bandpower(f2,p2,30,100)]
        np.save("recfolder/Data.npy",Data)
        if myparams[1]==1 and myparams[2]==0:
            np.save("recfolder/firstsamplewithltp.npy",[data,a.whist()[1]])#also saves lfp over time and whist
        
        
        
