"""
Model of shoaling behavior based on the Boids model by Craig Reynolds in 1986,
using the basic code provided in the Flocker example of the Mesa framework for
agent-based modelling in Python. This model is based on 3 parameters that each
agent follows:
    1. Attraction to (coherence with) other agents,
    2. Avoidance of other agents,
    3. Alignment with other agents.

The model is based on a toroidal, 2D area.

This file is for creating a dataframe containing the position of each agent at
each step, using the data collector. The dataframe can then be exported as a
.csv file, or graphed using matplotlib.
"""

import pandas as pd
import itertools
from shoal_model import *
import os

# import matplotlib.pyplot as plt
# from matplotlib import animation


def positions(model):
    """
    Extracts xy coordinates for each agent to be used in the data collector,
    creates lists of tuples (for each agent) per step, which is then flattened
    into a simple list and made into a pandas series.
    """
    pos = [(agent.pos[0], agent.pos[1]) for agent in model.schedule.agents]
    pos = list(itertools.chain(*pos))
    return pos


# Collect the data from a single run with x number of steps into a dataframe
model = ShoalModel(initial_fish=50,
                   initial_obstruct=4000,
                   width=100,
                   height=100,
                   speed=1,
                   vision=10,
                   separation=2)
for i in range(100):
    model.step()
data = model.datacollector.get_model_vars_dataframe()

# Get DataFrame into a form that can be exported as .csv - remove nesting
data = np.asarray(data)
data = data.flatten()  # one set of brackets removed....
df = pd.DataFrame(data)
output = df[0].apply(pd.Series)  # removed another set of brackets
output[0].apply(pd.Series)  # removed last brackets
np_output = np.asarray(output)

# Column headers: x1, y1, x2, y2, etc.
nums = range(1, 8)  # list same length as # of agents (end value is num + 1)
list_x = ["x" + str(i) for i in nums]  # creates x1, x2, etc.
list_y = ["y" + str(j) for j in nums]  # same for y

# iterate between lists and assign as column names
output.columns = [item for sublist in zip(list_x, list_y) for item in sublist]

# Export data as .csv
path = "/Users/user/Desktop/Local/Mackerel/Mackerel_Data"
output.to_csv(os.path.join(path, r"position_data.csv"))


# # Visualization in matplotlib
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

