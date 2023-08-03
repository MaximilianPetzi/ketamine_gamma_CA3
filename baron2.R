#install.packages("mediation")
#install.packages("lme4")###
#install.packages("sjPlot")
#install.packages("purrr")
library(sjPlot)
library(dplyr)
library(mediation)
library(purrr)
#warning: the nTE are not windowed, but just copied for each window
#run for example with Rscript baron.R
orig_data=read.csv("recfolder/barondata_rec")
data = orig_data
#View(data)
data=aggregate(.~ run, data=data, FUN=mean)

data=filter(data, kext < 20)
avgdata=aggregate(.~kext,data=data,FUN=mean)
vardata=aggregate(.~kext,data=data,FUN=var)

#________________kext:_______________#

#data=filter(data, kext == 1)
#data=filter(data, run != 1) #because it is measured twice

#plot(data$kext,data$pfreq,  col=factor(data$kext))
plot(data$gamma,data$pfreq,  col=factor(data$kext))

#plot(data$gamma,data$asynch)
#par(mfrow=c(1,2)) 
#plot(data$kext,data$psynch0)
#plot(data$kext,data$bsynch0)
#legend("topright", legend = unique(data$kext), col = unique(data$kext), pch = 1)

data$gamma = scale(data$gamma)
data$krec = scale(data$krec)
data$kext = scale(data$kext)
data$nTE = scale(data$nTE)
data$asynch = scale(data$asynch)
data$psynch0 = scale(data$psynch0)
data$psynch1 = scale(data$psynch1)
data$psynch2 = scale(data$psynch2)
data$psynch3 = scale(data$psynch3)
data$bsynch0 = scale(data$bsynch0)
data$bsynch1 = scale(data$bsynch1)
data$bsynch2 = scale(data$bsynch2)
data$bsynch3 = scale(data$bsynch3)
data$pfreq = scale(data$pfreq)
data$bfreq = scale(data$bfreq)

mediator=data$psynch0


firstmodel=lm(gamma~kext,data=data)
summary(firstmodel)
#model <- mediate(modelY = y ~ x, modelM = m ~ x, treat = "x", mediator = "asynch", boot = TRUE, sims = 1000,data=data)

mediate_model=lm(mediator~kext,data=data)
summary(mediate_model)

full_model=lm(gamma~kext+mediator,data=data)
summary(full_model)

tab_model(firstmodel, mediate_model, full_model)


results=mediate(mediate_model,full_model,treat="kext",mediator="mediator")#,boot=TRUE,sims=500)
summary(results)




