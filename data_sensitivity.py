"""
This file is for creating dataframes containing the results from the data
collectors in the model. These are:
    1. Polarization: a function returning the median absolute deviation of
       agent heading from the mean heading of the group
    2. Nearest neighbour distance: the mean distance of the 5 nearest agents,
       determined using a k-distance tree.
    3. Shoal area: convex hull
    4. Mean distance from centroid

These parameters all produce a single value per step in the model. The
dataframes created in this file are:
    1. The model run for X number of steps with set variables
    2. The model run for X times with X number of steps with set variables.
These dataframes can then be exported as .csv files to be further examined in R
or graphed with matplotlib.
"""

import os
from shoal_model import *
import matplotlib.pyplot as plt


# Data collection for debugging purposes
# model = ShoalModel(population=100, width=50, height=50, speed=1, vision=10, separation=2)
# for i in range(100):
#     model.step()
# data1 = model.datacollector.get_model_vars_dataframe()


# Collect the data from a single run with x number of steps into a dataframe
# path = "/Users/user/Desktop/Local/Mackerel/shoal-model-in-R"
# path_laptop = "/Users/Sophie/Desktop/DO NOT ERASE/1NUIG/Mackerel/Mackerel Data"

# 100 agents
model100 = ShoalModel(population=100, width=50, height=50, speed=1, vision=10, separation=2)
for i in range(500):
    model100.step()
data100 = model100.datacollector.get_model_vars_dataframe()
cent_dist100 = data100.columns[0]
nnd100 = data100.columns[1]
polar100 = data100.columns[2]
area100 = data100.columns[3]
# data100.to_csv(os.path.join(path, r"shoal_data_100.csv"), index=",")

# 50 agents
model50 = ShoalModel(population=50, width=50, height=50, speed=1, vision=10, separation=2)
for j in range(500):
    model50.step()
data50 = model50.datacollector.get_model_vars_dataframe()
cent_dist50 = data100.columns[0]
nnd50 = data50.columns[1]
polar50 = data50.columns[2]
area50 = data50.columns[3]
# data50.to_csv(os.path.join(path, r"shoal_data_50.csv"), index=",")

# # 200 agents
model200 = ShoalModel(population=200, width=50, height=50, speed=1, vision=10, separation=2)
for k in range(500):
    model200.step()
data200 = model200.datacollector.get_model_vars_dataframe()
cent_dist200 = data200.columns[0]
nnd200 = data200.columns[1]
polar200 = data200.columns[2]
area200 = data200.columns[3]
# data200.to_csv(os.path.join(path, r"shoal_data_200.csv"), index=",")




