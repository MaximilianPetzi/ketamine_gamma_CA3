
# CA3 model 
Network mostly the same as in Neymotin et al. (2011)

runs on python 2, Linux
Dependencies: NEURON simulator (http://www.neuron.yale.edu) compiled with python enabled.
For other dependencies, see the .Dockerfile (actually using docker might work too)

my_mosinit.py is the file that executes a single simulation. seedavg.py or baronkenny.py are the files that run many of such simulations at once and save their data. separate functions then plot these, but these are different from branch to branch in order to make reproducing easier (although I am not so sure if this actually makes it easier) 

for running any simulations, first compile .mod files by runnig (in terminal):
 nrnivmodl
then, to execute a single simulation: 
 ./x86_64/special -python my_mosinit.py


Code to reproduce the figures of our paper is distributed on different branches (which are mostly the same to each other):
 
mediation analysis table: reproducable (stochastic) by checking out somasynch branch. execute baronkenny.py to run simulations and baron2.R to plot (data is in recfolder/barondata_ext_2)

graphs for scaling connection strenths: checkout Taufac_dend. to run simulations, run seedavg.py. plot data with plit_spec.py
to switch between kext vs. krec, you have to modify my_mosinit.py, and for plotting also in plit_spec.py (both krec and kext files available).
 
graphs for different synaptic delays: checkout Taufac_dend_delay. (a): execute slopes.py. (b): slopes.py automatically creates data for plot (b) too. slope.R then creates the plot and saves it as a pdf

to recreate voltage curve: run checkout delay, then ./x86_64/special -python my_mosinit.py , a.tvp2(). Look above definitions of functions volt and tvp in my_mosinit for instructions. 

The rasterplots are done with neurons plotting functions. should work on any branch, as long as my_mosinit doesn't have these function calls uncommented. 
