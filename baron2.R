#install.packages("mediation")
#install.packages("lme4")###
#install.packages("sjPlot")
install.packages("purrr")
library(sjPlot)
library(dplyr)
library(mediation)
library(purrr)
#warning: the nTE are not windowed, but just copied for each window
#run for example with Rscript baron.R
orig_data=read.csv("recfolder/barondata")
data = orig_data
data=aggregate(.~ run, data=data, FUN=mean)
data=filter(data, krec < 35)
#data=filter(data, kext < 27)

avgdata=aggregate(.~krec,data=data,FUN=mean)
vardata=aggregate(.~krec,data=data,FUN=var)

#________________kext:_______________#

data=filter(data, kext == 1)
data=filter(data, run != 1) #because it is measured twice
#View(data)
#plot(data$nTE,data$gamma)
#plot(avgdata$nTE,avgdata$gamma)
#plot(data$krec,data$nTE)
plot(data$gamma,data$nTE,  col=factor(data$krec))

#legend("topright", legend = unique(data$kext), col = unique(data$kext), pch = 1)

data$gamma = scale(data$gamma)
data$krec = scale(data$krec)
data$kext = scale(data$kext)
data$nTE = scale(data$nTE)
data$asynch = scale(data$asynch)

firstmodel=lm(gamma~krec,data=data)
summary(firstmodel)
#model <- mediate(modelY = y ~ x, modelM = m ~ x, treat = "x", mediator = "asynch", boot = TRUE, sims = 1000,data=data)

mediate_model=lm(nTE~krec,data=data)
summary(mediate_model)

full_model=lm(gamma~krec+nTE,data=data)
summary(full_model)

tab_model(firstmodel, mediate_model, full_model)


results=mediate(mediate_model,full_model,treat="krec",mediator="nTE")#,boot=TRUE,sims=500)
summary(results)

