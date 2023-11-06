#install.packages("sjPlot")
#install.packages("lme4")###
#install.packages("latex2exp")
library(latex2exp)
library(sjPlot)
library(lme4)
data=read.csv("recfolder/slopedata")
delaylevels= c(0,5,10,15,20,25,30,35,40,45)
data$delay=factor(data$delay,levels=delaylevels)
#View(data)
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

pdf("myplot.pdf", width=6, height=6)
par(mar=c(5,6,4,1)+.1) #more margin because its cut off
plot(delaylevels,y=random_effect_slopes, type="l",
    xlab="Delay [ms]", 
    ylab=TeX(r'($\gamma-k_{rec}$ effect)'), 
    cex.lab=1.3, cex.axis=1.3)
dev.off()





