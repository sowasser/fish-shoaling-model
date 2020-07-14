"""
Code for creating a heatmap of density factors from runs of the shoaling model.
The data is collected, when running the Shoal Model, with the functions
outlined in data_collectors.py. Here, they are separated and manipulated to
create more simple outputs
"""

# Todo: try to create animated heatmaps (or, rather, pcolormesh) for density:
# https://www.kaggle.com/jaeyoonpark/heatmap-animation-us-drought-map/code
# https://www.programcreek.com/python/example/102329/matplotlib.pyplot.pcolormesh

from shoal_model_pos import *
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib import animation

# path = "/Users/user/Desktop/Local/Mackerel/Mackerel Data"
path = "/Users/Sophie/Desktop/DO NOT ERASE/1NUIG/Mackerel/Mackerel Data"  # for laptop

# Collect the data from a single run with x number of steps into a dataframe
model = ShoalModel(n_fish=20,
                   width=100,
                   height=100,
                   speed=2.7,
                   vision=10.8,
                   separation=7.3,
                   cohere=0.26,
                   separate=0.26,
                   match=0.59)
for i in range(10):
    model.step()
data = model.datacollector.get_model_vars_dataframe()

# Separate data from data collectors into numpy arrays so they can be accessed more easily
np_data = np.asarray(data)

# Flatten Positions so it is more accessible & add column names
p = np_data.flatten()  # remove one set of brackets & make a dataframe
pos_df = pd.DataFrame(p.flatten())  # remove one set of brackets & make a dataframe
pos_df = pos_df[0].apply(pd.Series)  # remove another set of brackets
pos_df[0].apply(pd.Series)  # remove last set of brackets
pos = np.asarray(pos_df)  # back to numpy array

nums = range(1, 21)  # list same length as # of agents (end value is num + 1)
list_x = ["x" + str(i) for i in nums]  # creates x1, x2, etc.
list_y = ["y" + str(j) for j in nums]  # same for y

# iterate between lists and assign as column names
pos_df.columns = [item for sublist in zip(list_x, list_y) for item in sublist]

# Separate x and y columns into different dataframes
x = pos_df.iloc[:, ::2]
y = pos_df.iloc[:, 1::2]

# Export to .csv for import into R
x.to_csv(os.path.join(path, r"heatmap_x.csv"))
y.to_csv(os.path.join(path, r"heatmap_y.csv"))

# # isolate position data for first step
# x1 = pos[0, 0::2].tolist()
# y1 = pos[0, 1::2].tolist()
# agent = [1] * 20
# step = [1] * 20
# step1 = pd.DataFrame(list(zip(x1, y1, agent, step)),
#                      columns=["x", "y", "agent", "step"])


# # Flatten Mean Position so it is more accessible & add column names
# mean_pos = pd.DataFrame(np_data[:, 5])
# mean_pos_df = mean_pos[0].apply(pd.Series)  # removed a set of brackets
# mean_pos_df.columns = ["x", "y"]


# # Plotting
# plt.style.use("dark_background")
#
# x = range(100)
# y = range(100)
#
# fig = plt.figure(figsize=(6, 6))
# ax = fig.add_subplot(111)
# plt.title("Position of Fish")  # Todo: figure out sequential step numbering
#
# scatter = ax.scatter(x=x1, y=y1)
# plt.show()
