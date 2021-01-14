"""
Code for creating a heatmap of density factors from runs of the shoaling model.
The data is collected, when running the Shoal Model, with the functions
outlined in data_collectors.py. Here, they are separated and manipulated to
create more simple outputs
"""

# Todo: select model type to match & make sure to select the correct .csv output
# from shoal_model_pos import *
from shoal_model_obstruct import *

import pandas as pd
import os

# path = "/Users/user/Desktop/Local/Mackerel/Mackerel Data"
path = "/Users/Sophie/Desktop/DO NOT ERASE/1NUIG/Mackerel/Mackerel Data"  # for laptop

n = 300  # number of fish

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
for i in range(400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()

# Separate data from data collectors into numpy arrays so they can be accessed more easily
np_data = np.asarray(data)

# Separate position & heading data
positions = np_data[:, 1]
headings = np_data[:, 0]

# Create unique names for each fish
list_fish = ["fish" + str(i) for i in range(1, (n + 1))]

# Manage position data --------------------------------------------------------
# Flatten positions so it is more accessible & add column names
p = positions.flatten()  # remove one set of brackets & make a dataframe
pos_df = pd.DataFrame(p.flatten())  # remove one set of brackets & make a dataframe
pos_df = pos_df[0].apply(pd.Series)  # remove another set of brackets
pos_df[0].apply(pd.Series)  # remove last set of brackets
pos = np.asarray(pos_df)  # back to numpy array

# Separate x and y columns into different dataframes & rename columns
x = pos_df.iloc[:, ::2]
x.columns = list_fish

y = pos_df.iloc[:, 1::2]
y.columns = list_fish

# Manage heading data ---------------------------------------------------------
# Flatten headings so it is more accessible & add column names
h = headings.flatten()  # remove one set of brackets & make a dataframe
head_df = pd.DataFrame(h.flatten())  # remove one set of brackets & make a dataframe
head_df = head_df[0].apply(pd.Series)  # remove another set of brackets
head_df[0].apply(pd.Series)  # remove last set of brackets

# Separate x and y columns into different dataframes & rename columns
head_df.columns = list_fish

# Todo: select data output to match the version of the model run
# Export normal run to .csv for import into R ---------------------------------
# Todo: increase number to save a new version of the data
# head_df.to_csv(os.path.join(path, r"headings_300_4.csv"))  # heading data
#
# x.to_csv(os.path.join(path, r"heatmap_x_300_4.csv"))  # x position
# y.to_csv(os.path.join(path, r"heatmap_y_300_4.csv"))  # y position

# Export thermocline run to .csv for import into R ----------------------------
# Todo: increase number to save a new version of the data
# head_df.to_csv(os.path.join(path, r"headings_cline.csv"))  # heading data
#
# x.to_csv(os.path.join(path, r"heatmap_x_cline.csv"))  # x position
# y.to_csv(os.path.join(path, r"heatmap_y_cline.csv"))  # y position

# Export thermocline run to .csv for import into R ----------------------------
# Todo: increase number to save a new version of the data
head_df.to_csv(os.path.join(path, r"headings_slope.csv"))  # heading data

x.to_csv(os.path.join(path, r"heatmap_x_slope.csv"))  # x position
y.to_csv(os.path.join(path, r"heatmap_y_slope.csv"))  # y position



