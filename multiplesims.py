import os,sys
commandstring="python2 my_mosinit.py"
myterminal=open('myterminal.txt', 'a')
sys.stdout=myterminal
print("")
print("multiplesims starting...\n")
myterminal.close()
sys.stdout=sys.__stdout__

for i in range(20):
    os.system(commandstring)

