"""
Code for creating a heatmap of density factors from runs of the shoaling model.
The data is collected, when running the Shoal Model, with the functions
outlined in data_collectors.py. Here, they are separated and manipulated to
create more simple outputs
"""

# Todo: try to create animated heatmaps for density:
# https://www.kaggle.com/jaeyoonpark/heatmap-animation-us-drought-map/code

from shoal_model import *
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import animation


# Collect the data from a single run with x number of steps into a dataframe
model = ShoalModel(initial_fish=50,
                   initial_obstruct=4000,
                   width=100,
                   height=100,
                   speed=1,
                   vision=10,
                   separation=10)
for i in range(10):
    model.step()
data = model.datacollector.get_model_vars_dataframe()

# Separate data from data collectors into numpy arrays so they can be accessed more easily
np_data = np.asarray(data)
# polar = np_data[:, 0]
# nnd = np_data[:, 1]
# area = np_data[:, 2]
# centroid_dist = np_data[:, 3]

# Flatten Positions so it is more accessible & add column names
position = pd.DataFrame(np_data[:, 4].flatten())  # remove one set of brackets & make a dataframe
pos_df = pd.DataFrame(position)
pos_df = pos_df[0].apply(pd.Series)  # remove another set of brackets
pos_df[0].apply(pd.Series)  # remove last set of brackets
np_pos = np.asarray(pos_df)  # back to numpy array

nums = range(1, 51)  # list same length as # of agents (end value is num + 1)
list_x = ["x" + str(i) for i in nums]  # creates x1, x2, etc.
list_y = ["y" + str(j) for j in nums]  # same for y
# iterate between lists and assign as column names
pos_df.columns = [item for sublist in zip(list_x, list_y) for item in sublist]


# Flatten Mean Position so it is more accessible & add column names
mean_pos = pd.DataFrame(np_data[:, 5])
mean_pos_df = mean_pos[0].apply(pd.Series)  # removed a set of brackets
mean_pos_df.columns = ["x", "y"]



# # Plotting
# plt.style.use("dark_background")
# fig, ax = plt.subplots()
# ax.scatter(data[0], data[1])
#
# plt.tight_layout()
# plt.show()

# # Animation in matplotlib
# plt.style.use('dark_background')
#
# # Set up figure, axes, and plot element
# fig = plt.figure()
# ax = plt.axes(xlim=(0, 100), ylim=(0, 100))
# scatter,  = ax.plot([], [], markersize=2)
#
#
# # Initialization function - background of frames
# def init():
#     scatter.set_data([], [])
#     return scatter,
#
#
# # Animation function - called sequentially
# def animate(i):
#     x = output[i, ::2]
#     y = output[i, 1::2]
#     scatter.set_data(x, y)
#     return scatter,
#
#
# # Call the animator
# anim = animation.FuncAnimation(fig, animate, init_func=init,
#                                frames=100, interval=20)
# plt.show()
#
# # Save the animation - need FFmpeg to save as mp4
# # anim.save('basic_animation.mp4', fps=30)
