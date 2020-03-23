"""
This file is for testing the effect of different parameter values on the output
from the data collectors, when running on the ICHEC cluster. In this script,
speed varies while vision and separation remain fixed.
"""

from shoal_model import *
import pandas as pd
from scipy.stats import gamma


# SET PARAMETER & MODEL VALUES ------------------------------------------------

# Fixed values for non-tested parameters
vision_fixed = 10
sep_fixed = 2

# Todo: figure out how to get the range we want. Must be non-negative!

# Defines the distribution as a range of values. Size is # of variables (and
# therefore runs of the model), a is the number that the distribution is based
# around.
speed_dist = np.random.lognormal(mean=2, sigma=1, size=10000)

steps = 200  # number of steps to run the model for each time

burn_in = 10  # number of steps to exclude at the beginning as collective behaviour emerges


# RUN MODELS & COLLECT DATA ---------------------------------------------------
def run_speed_model(speed):
    """
    Runs the shoal model for a certain number of steps with agent speed varying
    while all other parameters are fixed. Returns a dataframe with the average
    per run of all data collectors (average of all steps) and columns with the
    parameter values for that run, including the varying & fixed parameters so
    all dataframes can be stacked together.
    """
    speed_parameter = []
    model = ShoalModel(n_fish=20,
                       width=50,
                       height=50,
                       speed=speed,
                       vision=vision_fixed,
                       separation=sep_fixed)
    for step in range(steps):
        model.step()  # run the model for certain number of steps
        speed_parameter.append(speed)  # create list of parameter values tested
    data = model.datacollector.get_model_vars_dataframe()  # retrieve data from model
    data["speed"] = speed_parameter  # add parameter value column
    data["vision"] = vision_fixed  # add vision column
    data["separation"] = sep_fixed  # add separation column
    data_trim = data.iloc[burn_in:, ]  # remove early runs
    return pd.DataFrame(data_trim.mean(axis=0)).T


# Run the model as many times as there are parameter values
speed_data = pd.concat([run_speed_model(i) for i in speed_dist])

# Re-name columns so all data will print & index with unique values for R.
speed_data.columns = ["polar", "nnd", "area", "cent", "speed", "vision", "sep"]
speed_data.index = list(range(len(speed_dist)))  # sequential numbers following # of runs
pd.set_option("display.max_rows", None)  # display all rows
pd.set_option("display.max_columns", None)  # display all columns

print(speed_data)  # printing makes the data accessible from the cluster.
