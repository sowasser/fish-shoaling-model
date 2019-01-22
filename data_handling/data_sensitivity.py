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

# Paths for exporting the data, rather than graphing
path = "/Users/user/Desktop/Local/Mackerel/Mackerel Data"
# path_laptop = "/Users/Sophie/Desktop/DO NOT ERASE/1NUIG/Mackerel/Mackerel Data"

model50 = ShoalModel(initial_fish=50,
                     initial_obstruct=4000,
                     width=100,
                     height=100,
                     speed=1,
                     vision=10,
                     separation=2)
for j in range(150):
    model50.step()
data50 = model50.datacollector.get_model_vars_dataframe()
# data50.to_csv(os.path.join(path, r"shoal_data_50.csv"), index=",")

model100 = ShoalModel(initial_fish=100,
                      initial_obstruct=4000,
                      width=100,
                      height=100,
                      speed=1,
                      vision=10,
                      separation=2)
for j in range(150):
    model100.step()
data100 = model100.datacollector.get_model_vars_dataframe()
# data100.to_csv(os.path.join(path, r"shoal_data_100.csv"), index=",")

model200 = ShoalModel(initial_fish=200,
                      initial_obstruct=4000,
                      width=100,
                      height=100,
                      speed=1,
                      vision=10,
                      separation=2)
for j in range(150):
    model200.step()
data200 = model200.datacollector.get_model_vars_dataframe()
# data200.to_csv(os.path.join(path, r"shoal_data_200.csv"), index=",")


############
# Plotting #
############

plt.style.use("dark_background")
# # plt.style.use("ggplot")
# # plt.style.use("seaborn-dark")
# # plt.style.use("Solarize_Light2")

# Mean distance from centroid multiplot
dist_fig = plt.figure(figsize=(5, 9), dpi=300)
ax1 = plt.subplot(3, 1, 1)
plt.title("Mean Distance from Centroid", fontsize="x-large")
plt.xlabel("(n=50)")
plt.ylabel("mm")
ax2 = plt.subplot(3, 1, 2)
plt.xlabel("(n=100)")
plt.ylabel("mm")
ax3 = plt.subplot(3, 1, 3)
plt.xlabel("(n=200)")
plt.ylabel("mm")

ax1.plot(data50["Mean Distance from Centroid"])
ax2.plot(data100["Mean Distance from Centroid"])
ax3.plot(data200["Mean Distance from Centroid"])

plt.tight_layout()
plt.show()

# Nearest neighbour distance multiplot
nnd_fig = plt.figure(figsize=(5, 9), dpi=300)
ax4 = plt.subplot(3, 1, 1)
plt.title("Mean Nearest Neighbour Distance", fontsize="x-large")
plt.xlabel("(n=50)")
plt.ylabel("mm")
ax5 = plt.subplot(3, 1, 2)
plt.xlabel("(n=100)")
plt.ylabel("mm")
ax6 = plt.subplot(3, 1, 3)
plt.xlabel("(n=200)")
plt.ylabel("mm")

ax4.plot(data50["Nearest Neighbour Distance"])
ax5.plot(data100["Nearest Neighbour Distance"])
ax6.plot(data200["Nearest Neighbour Distance"])

plt.tight_layout()
plt.show()

# Polarization multiplot
polar_fig = plt.figure(figsize=(5, 9), dpi=300)
ax7 = plt.subplot(3, 1, 1)
plt.title("Polarization", fontsize="x-large")
plt.xlabel("(n=50)")
plt.ylabel("median absolute deviation")
ax8 = plt.subplot(3, 1, 2)
plt.xlabel("(n=100)")
plt.ylabel("median absolute deviation")
ax9 = plt.subplot(3, 1, 3)
plt.xlabel("(n=200)")
plt.ylabel("median absolute deviation")

ax7.plot(data50["Polarization"])
ax8.plot(data50["Polarization"])
ax9.plot(data50["Polarization"])

plt.tight_layout()
plt.show()

# Create shoal area multiplot
area_fig = plt.figure(figsize=(5, 9), dpi=300)
ax10 = plt.subplot(3, 1, 1)
plt.title("Shoal Area", fontsize="x-large")
plt.xlabel("(n=50)")
plt.ylabel("mm2")
ax11 = plt.subplot(3, 1, 2)
plt.xlabel("(n=100)")
plt.ylabel("mm2")
ax12 = plt.subplot(3, 1, 3)
plt.xlabel("(n=200)")
plt.ylabel("mm2")

ax10.plot(data50["Shoal Area"])
ax11.plot(data100["Shoal Area"])
ax12.plot(data200["Shoal Area"])

plt.tight_layout()
plt.show()


# # Export figures
# plot_path = "/Users/user/Desktop/Local/Mackerel/Figures"
# # plot_path_laptop = "/Users/Sophie/Desktop/DO NOT ERASE/1NUIG/Mackerel"
#
# dist_fig.savefig(os.path.join(plot_path, r"dist_sensitivity.png"))
# nnd_fig.savefig(os.path.join(plot_path, r"nnd_sensitivity.png"))
# polar_fig.savefig(os.path.join(plot_path, r"polar_sensitivity.png"))
# area_fig.savefig(os.path.join(plot_path, r"area_sensitivity.png"))
