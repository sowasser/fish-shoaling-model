"""
Code for creating a heatmap of density factors from runs of the shoaling model.
The data is collected, when running the Shoal Model, with the functions
outlined in data_collectors.py. They are separated and manipulated to create
more simple outputs.

This script is a version of data_sensitivity_heatmap.py altered to run on the
ICHEC cluster.
"""

from shoal_model_pos import *
import pandas as pd
import os

# path = "/Users/user/Desktop/Local/Mackerel/Mackerel Data"
path = "/Users/Sophie/Desktop/DO NOT ERASE/1NUIG/Mackerel/Mackerel Data"  # for laptop

n = 50  # number of fish


def run_model(width_prior, vision_prior, separation_prior):
    """
    Runs the shoal model for a certain number of steps with varying
    parameteters and returns two data frames with the average for the runs
    when shoaling behaviour has been established, so all dataframes can be
    stacked together.
    """
    model = ShoalModel(n_fish=n,
                       width=width_prior,
                       height=50,
                       speed=1,
                       vision=vision_prior,
                       separation=separation_prior,
                       cohere=0.25,
                       separate=0.25,
                       match=0.3)
    for i in range(20):  # number of steps to run the model for
        model.step()
    data = model.datacollector.get_model_vars_dataframe()  # retrieve data from model
    data_trim = data.iloc[18:19, ]  # remove early runs
    np_data = np.asarray(data_trim)
    # Flatten Positions so it is more accessible & add column names
    p = np_data.flatten()  # remove one set of brackets & make a dataframe
    pos_df = pd.DataFrame(p.flatten())  # remove one set of brackets & make a dataframe
    pos_df = pos_df[0].apply(pd.Series)  # remove another set of brackets
    pos_df[0].apply(pd.Series)  # remove last set of brackets
    pos = np.asarray(pos_df)  # back to numpy array
    return pos_df


# Run model with priors
positions = run_model(50, 50, 2)

# Create unique names for each fish
list_fish = ["fish" + str(i) for i in range(1, (n + 1))]

# Separate x and y columns into different dataframes & rename columns
x = positions.iloc[:, ::2]
x.columns = list_fish

y = positions.iloc[:, 1::2]
y.columns = list_fish

print(x)
