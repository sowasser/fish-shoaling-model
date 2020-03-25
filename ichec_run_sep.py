"""
This file is for testing the effect of different parameter values on the output
from the data collectors, when running on the ICHEC cluster. In this script,
separation varies while speed and vision remain fixed.
"""

from shoal_model import *
import pandas as pd
from scipy.stats import gamma


# SET PARAMETER & MODEL VALUES ------------------------------------------------

# Fixed values for non-tested parameters
speed_fixed = 2
vision_fixed = 10

# Todo: figure out how to get the range we want. Must be non-negative!

# Defines the distribution as a range of values. Size is # of variables (and
# therefore runs of the model), a is the number that the distribution is based
# around.
sep_dist = gamma.rvs(size=300, a=2)

steps = 200  # number of steps to run the model for each time

burn_in = 10  # number of steps to exclude at the beginning as collective behaviour emerges


# RUN MODELS & COLLECT DATA ---------------------------------------------------
def run_sep_model(separation):
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
                       separation=separation)
    for step in range(steps):
        model.step()  # run the model for certain number of steps
        sep_parameter.append(separation)  # create list of parameter values tested
    data = model.datacollector.get_model_vars_dataframe() # retrieve data from model
    data["speed"] = speed_fixed  # add parameter value column
    data["vision"] = vision_fixed  # add vision column
    data["separation"] = sep_parameter  # add separation column
    data_trim = data.iloc[burn_in:, ]  # remove early runs
    return pd.DataFrame(data_trim.mean(axis=0)).T  # return means of all columns & transposed


# Run the model as many times as there are parameter values
sep_data = pd.concat([run_sep_model(i) for i in sep_dist])

# Re-name columns so all data will print & index with unique values for R.
sep_data.columns = ["polar", "nnd", "area", "cent", "speed", "vision", "sep"]
sep_data.index = list(range(len(sep_dist)))  # sequential numbers following # of runs
pd.set_option("display.max_rows", None)  # display all rows
pd.set_option("display.max_columns", None)  # display all columns

print(sep_data)  # printing makes the data accessible from the cluster.
