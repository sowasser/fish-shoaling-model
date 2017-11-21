setwd("~/Desktop/Local/Mackerel/Mackerel_Data")
# shoal_data <- read.csv("shoal_data.csv")
pos <- read.csv("position_data.csv")

# Change first column name
colnames(pos)[1] <- "step"

#find max and min for axes in matplotlib plot
max(pos)
min(pos)
