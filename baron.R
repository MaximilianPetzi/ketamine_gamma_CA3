#install.packages("mediation")
#install.packages("lme4")###
#install.packages("sjPlot")
library(sjPlot)
library(dplyr)
library(mediation)
#warning: the nTE are not windowed, but just copied for each window
#run for example with Rscript baron.R
unscaled_data=read.csv("recfolder/barondata")
data = unscaled_data
data=filter(data, krec < 30)

data = merge(
    merge(
        aggregate(krec ~ run, data=data, FUN=mean), 
        aggregate(gamma ~ run, data=data, FUN=mean), 
        by="run"), 
    aggregate(asynch ~ run, data=data, FUN=mean), 
    by="run")

#print(data)#run actually means run. only the same during a simulation


data$gamma = scale(data$gamma )
data$krec = scale(data$krec)
data$asynch = scale(data$asynch)

firstmodel=lm(gamma~krec,data=data)
summary(firstmodel)
#model <- mediate(modelY = y ~ x, modelM = m ~ x, treat = "x", mediator = "asynch", boot = TRUE, sims = 1000,data=data)

mediate_model=lm(asynch~krec,data=data)
summary(mediate_model)

full_model=lm(gamma~krec+asynch,data=data)
summary(full_model)

tab_model(firstmodel, mediate_model, full_model)


results=mediate(mediate_model,full_model,treat="krec",mediator="asynch")#,boot=TRUE,sims=500)
summary(results)


# average <- mean(data$asynch[data$krec == 1], na.rm = TRUE)
# print("avg=")
# print(average)

###########################################
# now mediaton analysis. look here:
# https://cran.r-project.org/web/packages/mediation/vignettes/mediation.pdf

# and chatgpt says (same package i think):
# install.packages("mediation")
# library(mediation)

# # Load your dataset
# data <- read.csv("your_dataset.csv")

# # Specify the variables in your dataset
# x <- data$x
# m <- data$m
# y <- data$y

# # Fit the mediation model using the Baron and Kenny approach
# model <- mediate(modelY = y ~ x, modelM = m ~ x, treat = "x", mediator = "m", boot = TRUE, sims = 1000)

# # Print the mediation results
# summary(model)
data=unscaled_data
dat=data[data$krec==1,]
plot(dat$asynch, dat$gamma,col="orange")
dat=data[data$krec==11,]
#points(dat$asynch, dat$gamma,col="red")
dat=data[data$krec==21,]
#points(dat$asynch, dat$gamma,col="purple")
dat=data[data$krec==31,]
points(dat$asynch, dat$gamma,col="blue")



