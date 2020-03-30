"""
This file is for testing the effect of different parameter values on the output
from the data collectors, when running on the ICHEC cluster. In this script,
a value (prior) for separation is passed in from a defined gamma distribution
(from create_priors.py & sep_priors.txt).
"""

from shoal_model import *
import pandas as pd
import sys

# Fixed values for non-tested parameters
speed_fixed = 2
vision_fixed = 10


def run_sep_model(prior):
    """
    Runs the shoal model for a certain number of steps with separation distance
    varying while all other parameters are fixed. Returns a dataframe with the
    average per run of all data collectors (average of all steps) and columns
    with the parameter values for that run, including the varying & fixed
    parameters so all dataframes can be stacked together.
    """
    sep_parameter = []
    model = ShoalModel(n_fish=20,
                       width=50,
                       height=50,
                       speed=speed_fixed,
                       vision=vision_fixed,
                       separation=prior)
    for step in range(200):  # number of steps to run the model for
        model.step()  # run the model for certain number of steps
    data = model.datacollector.get_model_vars_dataframe()  # retrieve data from model
    data["speed"] = speed_fixed  # add speed value column
    data["vision"] = vision_fixed  # add vision column
    data["separation"] = prior  # add separation column
    data_trim = data.iloc[10:, ]  # remove some # of early runs
    return pd.DataFrame(data_trim.mean(axis=0)).T  # return means of all columns & transpose


# Run the model with value passed in from prior called in create_tasks.py
sep_data = run_sep_model(sys.argv[1])

# Re-name columns so all data will print & index with unique values for R.
sep_data.columns = ["polar", "nnd", "area", "cent", "speed", "vision", "sep"]

print(sep_data)  # printing makes the data accessible from the cluster.
