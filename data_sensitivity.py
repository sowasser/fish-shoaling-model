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
import pandas as pd

# Data collection for debugging purposes
# model = ShoalModel(population=100, width=50, height=50, speed=1, vision=10, separation=2)
# for i in range(100):
#     model.step()
# data1 = model.datacollector.get_model_vars_dataframe()


# Collect the data from a single run with x number of steps into a dataframe
# path = "/Users/user/Desktop/Local/Mackerel/shoal-model-in-R"
# path_laptop = "/Users/Sophie/Desktop/DO NOT ERASE/1NUIG/Mackerel/Mackerel Data"

steps = list(range(10))

# 100 agents
model100 = ShoalModel(population=100, width=50, height=50, speed=1, vision=10, separation=2)
for i in range(10):
    model100.step()
data100 = model100.datacollector.get_model_vars_dataframe()
data100.insert(loc=0, column='steps', value=steps)

# data100.to_csv(os.path.join(path, r"shoal_data_100.csv"), index=",")

# 50 agents
model50 = ShoalModel(population=50, width=50, height=50, speed=1, vision=10, separation=2)
for j in range(10):
    model50.step()
data50 = model50.datacollector.get_model_vars_dataframe()
data50.insert(loc=0, column='steps', value=steps)
# data50.to_csv(os.path.join(path, r"shoal_data_50.csv"), index=",")

# # 200 agents
model200 = ShoalModel(population=200, width=50, height=50, speed=1, vision=10, separation=2)
for k in range(10):
    model200.step()
data200 = model200.datacollector.get_model_vars_dataframe()
data200.insert(loc=0, column='steps', value=steps)

# data200.to_csv(os.path.join(path, r"shoal_data_200.csv"), index=",")


# Plotting
plt.style.use("dark_background")
# plt.style.use("ggplot")
# plt.style.use("seaborn-dark")
# plt.style.use("Solarize_Light2")

# Create mean distance from centroid multiplot
dist_fig = plt.figure(figsize=(5, 9), dpi=300)
ax1 = plt.subplot(3, 1, 1)
plt.title("Mean Distance from Centroid (n=50)")
plt.ylabel("(mm)")
ax2 = plt.subplot(3, 1, 2)
plt.title("Mean Distance from Centroid (n=100)")
plt.ylabel("(mm)")
ax3 = plt.subplot(3, 1, 3)
plt.title("Mean Distance from Centroid (n=200)")
plt.ylabel("(mm)")

ax1.plot(cent_dist50)
ax2.plot(cent_dist100)
ax3.plot(cent_dist200)

plt.tight_layout()
plt.show()

# Create nearest neighbour distance multiplot
nnd_fig = plt.figure(figsize=(5, 9), dpi=300)
ax4 = plt.subplot(3, 1, 1)
plt.title("Mean Nearest Neighbour Distance (n=50)")
plt.ylabel("(mm)")
ax5 = plt.subplot(3, 1, 2)
plt.title("Mean Nearest Neighbour Distance (n=100)")
plt.ylabel("(mm)")
ax6 = plt.subplot(3, 1, 3)
plt.title("Mean Nearest Neighbour Distance (n=200)")
plt.ylabel("(mm)")

ax4.plot(nnd50)
ax5.plot(nnd100)
ax6.plot(nnd200)

plt.tight_layout()
plt.show()

# Create polarization multiplot
polar_fig = plt.figure(figsize=(5, 9), dpi=300)
ax7 = plt.subplot(3, 1, 1)
plt.title("Polarization (n=50)")
ax8 = plt.subplot(3, 1, 2)
plt.title("Polarization (n=100)")
ax9 = plt.subplot(3, 1, 3)
plt.title("Polarization (n=200)")

ax7.plot(polar50)
ax8.plot(polar100)
ax9.plot(polar200)

plt.tight_layout()
plt.show()

# Create shoal area multiplot
area_fig = plt.figure(figsize=(5, 9), dpi=300)
ax10 = plt.subplot(3, 1, 1)
plt.title("Shoal Area (n=50)")
plt.ylabel("(mm2)")
ax11 = plt.subplot(3, 1, 2)
plt.title("Shoal Area (n=100)")
plt.ylabel("(mm2)")
ax12 = plt.subplot(3, 1, 3)
plt.title("Shoal Area (n=200)")
plt.ylabel("(mm2)")

ax10.plot(area50)
ax11.plot(area100)
ax12.plot(area200)

plt.tight_layout()
plt.show()


# Export figures
plot_path = "/Users/user/Desktop/Local/Mackerel/Figures"
# plot_path_laptop = "/Users/Sophie/Desktop/DO NOT ERASE/1NUIG/Mackerel"

dist_fig.savefig(os.path.join(plot_path, r"dist_sensitivity.png"))
nnd_fig.savefig(os.path.join(plot_path, r"nnd_sensitivity.png"))
polar_fig.savefig(os.path.join(plot_path, r"polar_sensitivity.png"))
area_fig.savefig(os.path.join(plot_path, r"area_sensitivity.png"))
