#run for example with Rscript baron.R
data=read.csv("recfolder/barondata")
print(data)#run actually means run. only the same during a simulation
#install.packages("mediation")
library(mediation)
firstmodel=lm(gamma~krec,data=data)
#summary(firstmodel)
#model <- mediate(modelY = y ~ x, modelM = m ~ x, treat = "x", mediator = "asynch", boot = TRUE, sims = 1000,data=data)
mediate_model=lm(asynch~krec + (1 | run),data=data)
#summary(mediate_model)
full_model=lm(gamma~krec+asynch + (1 | run),data=data)
#summary(full_model)
results=mediate(mediate_model,full_model,treat="krec",mediator="asynch",boot=TRUE,sims=500)
summary(results)

average <- mean(data$asynch[data$krec == 1], na.rm = TRUE)

print("avg=")
print(average)
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