setwd("~/Desktop/Local/Mackerel/Mackerel_Data")
shoal_data <- read.csv("shoal_data.csv")
pos_data <- read.csv("position_data.csv")

#find max and min for axes in matplotlib plot
max(pos_data)
min(pos_data)
