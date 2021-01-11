"""
Code for exporting the heading of each agent for each step of a model run to
represent the tilt angle of the fish, when the model is viewed side-on / as a
cross-section of the water column.

The data is collected, when running the Shoal Model, with the functions
outlined in data_collectors.py. Here, they are separated and manipulated to
create more simple outputs
"""

# Todo: try to create animated heatmaps (or, rather, pcolormesh) for density:
# https://www.kaggle.com/jaeyoonpark/heatmap-animation-us-drought-map/code
# https://www.programcreek.com/python/example/102329/matplotlib.pyplot.pcolormesh

from shoal_model_heading import *
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib import animation

# path = "/Users/user/Desktop/Local/Mackerel/Mackerel Data"
path = "/Users/Sophie/Desktop/DO NOT ERASE/1NUIG/Mackerel/Mackerel Data"  # for laptop

n = 30  # number of fish

# Collect the data from a single run with x number of steps into a dataframe
model = ShoalModel(n_fish=n,
                   width=50,
                   height=50,
                   speed=10,
                   vision=10,
                   separation=2,
                   cohere=0.25,
                   separate=0.025,
                   match=0.3)
for i in range(4):
    model.step()
data = model.datacollector.get_model_vars_dataframe()

# Separate data from data collectors into numpy arrays so they can be accessed more easily
np_data = np.asarray(data)

# Flatten Positions so it is more accessible & add column names
h = np_data.flatten()  # remove one set of brackets & make a dataframe
head_df = pd.DataFrame(h.flatten())  # remove one set of brackets & make a dataframe
head_df = head_df[0].apply(pd.Series)  # remove another set of brackets
head_df[0].apply(pd.Series)  # remove last set of brackets

# Create unique names for each fish
list_fish = ["fish" + str(i) for i in range(1, (n + 1))]

# Separate x and y columns into different dataframes & rename columns
head_df.columns = list_fish

# Export to .csv for import into R
head.to_csv(os.path.join(path, r"headings_300.csv"))