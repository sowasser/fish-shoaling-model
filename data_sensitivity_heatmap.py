"""
Code for creating a heatmap of density factors from runs of the shoaling model.
"""

# Todo: try to create animated heatmaps for density:
# https://matplotlib.org/examples/images_contours_and_fields/interpolation_methods.html
# https://stackoverflow.com/questions/33742845/seaborn-animate-heatmap-correlation-matrix?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa

from shoal_model import *
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import animation


# Collect the data from a single run with x number of steps into a dataframe
model = ShoalModel(initial_fish=50,
                   initial_obstruct=4000,
                   width=100,
                   height=100,
                   speed=1,
                   vision=10,
                   separation=10)
for i in range(2):
    model.step()
data = model.datacollector.get_model_vars_dataframe()

# Separate data from data collectors into numpy arrays so they can be accessed more easily
np_data = np.asarray(data)
polar = np_data[:, 0]
nnd = np_data[:, 1]
area = np_data[:, 2]
centroid_dist = np_data[:, 3]
mean_pos = np_data[:, 4]
# Todo: flatten the mean_pos array or otherwise change it to be more simple

print(mean_pos)

# Plotting
plt.style.use("dark_background")
fig, ax = plt.subplots()
ax.scatter(data[0], data[1])

plt.tight_layout()
plt.show()
