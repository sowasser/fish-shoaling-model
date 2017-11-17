setwd("~/Desktop/Local/Mackerel/Mackerel_Data")
# shoal_data <- read.csv("shoal_data.csv")
pos <- read.csv("position_data.csv")

# Change column names. This is NOT sustainable for larger datasets, however.
colnames(pos) <- c("step", "x1", "y1", "x2", "y2", "x3", "y3", "x4", "y4",
                   "x5", "y5", "x6", "y6", "x7", "y7")


#find max and min for axes in matplotlib plot
max(pos)
min(pos)
