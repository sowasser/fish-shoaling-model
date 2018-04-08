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


# Plotting
plt.style.use("dark_background")
# plt.style.use("ggplot")
# plt.style.use("seaborn-dark")
# plt.style.use("Solarize_Light2")

# Create multiplot
fig = plt.figure(figsize=(8, 6), dpi=300)

ax1 = plt.subplot(431)
plt.title("Mean Distance from Centroid (n=100)")
plt.ylabel("distance (mm)")
ax2 = plt.subplot(432)
plt.title("Mean Nearest Neighbour Distance (n=100)")
plt.ylabel("distance (mm)")
ax3 = plt.subplot(433)
plt.title("Polarization (n=100)")
plt.ylabel("Mean Absolute Deviation")
ax4 = plt.subplot(434)
plt.title("Shoal Area (n=100)")
plt.ylabel("area (mm2)")

ax5 = plt.subplot(435)
plt.title("Mean Distance from Centroid (n=50)")
plt.ylabel("distance (mm)")
ax6 = plt.subplot(436)
plt.title("Mean Nearest Neighbour Distance (n=50)")
plt.ylabel("distance (mm)")
ax7 = plt.subplot(437)
plt.title("Polarization (n=50)")
plt.ylabel("Mean Absolute Deviation")
ax8 = plt.subplot(438)
plt.title("Shoal Area (n=50)")
plt.ylabel("area (mm2)")

ax9 = plt.subplot(439)
plt.title("Mean Distance from Centroid (n=200)")
plt.ylabel("distance (mm)")
ax10 = plt.subplot(4310)
plt.title("Mean Nearest Neighbour Distance (n=200)")
plt.ylabel("distance (mm)")
ax11 = plt.subplot(4311)
plt.title("Polarization (n=200)")
plt.ylabel("Mean Absolute Deviation")
ax12 = plt.subplot(4312)
plt.title("Shoal Area (n=200)")
plt.ylabel("area (mm2)")

ax1.plot(cent_dist100)
ax2.plot(nnd100)
ax3.plot(polar100)
ax4.plot(area100)

ax5.plot(cent_dist50)
ax6.plot(nnd50)
ax7.plot(polar50)
ax8.plot(area50)

ax9.plot(cent_dist200)
ax10.plot(nnd200)
ax11.plot(polar200)
ax12.plot(area200)

plt.tight_layout()

plt.show()

plot_path = "/Users/user/Desktop/Local/Mackerel/Figures"
# Todo: CHANGE NAME OF FILE
fig.savefig(os.path.join(plot_path, r"sticklebacks1_300xstepwise.png"))

