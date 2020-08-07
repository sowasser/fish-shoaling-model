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
model = ShoalModel(n_fish=100,
                   width=100,
                   height=100,
                   speed=2.7,
                   vision=10.8,
                   separation=7.3,
                   cohere=0.26,
                   separate=0.26,
                   match=0.59)
for i in range(200):
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

# Create unique names for each fish
list_fish = ["fish" + str(i) for i in range(1, 101)]

# Separate x and y columns into different dataframes & rename columns
x = pos_df.iloc[:, ::2]
x.columns = list_fish

y = pos_df.iloc[:, 1::2]
y.columns = list_fish

# Export to .csv for import into R
x.to_csv(os.path.join(path, r"heatmap_x.csv"))
y.to_csv(os.path.join(path, r"heatmap_y.csv"))
