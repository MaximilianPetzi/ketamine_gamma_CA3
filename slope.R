#install.packages("sjPlot")
#install.packages("lme4")###
library(sjPlot)
library(lme4)
data=read.csv("recfolder/slopedata")
delaylevels=[0,5,10,15,20,25,30,35,40,45,60]
data$delay=factor(data,levels=delaylevels)
View(data)
m<-lmer(gamma~krec+(1+krec|delay),data) #this fits a 
#mixed effects model with krec as fixed effect, 
#random intercepts (1) for each delay, and 
#random krec-effect slopes for each delay. 
#in (A|B), A are the random effects causing extra variability, 
#and B is the grouping variable 
#(here: different effect for each delay)

#plot_model(m,type="re") #doesnt work
random_effect_slopes=ranef(m)$delay$krec  #this are the
#delay-dependent krec effects. 1d array

plot(random_effect_slopes,data$delaylevel,xlab="delay",ylab="effect")

