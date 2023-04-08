#install.packages("tidyverse")
#install.packages("ggplot2")
#install.packages("httpgd")

library(tidyverse)
library(ggplot2)

dat=read.csv("recfolder/oldData.csv")

model=lm(deltagamma=rec+ext,data=dat)
summary(model)
