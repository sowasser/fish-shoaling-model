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
    model = ShoalModel(n_fish=20,
                       width=50,
                       height=50,
                       speed=speed_fixed,
                       vision=vision_fixed,
                       separation=prior)
    for step in range(200):  # number of steps to run the model for
        model.step()
    data = model.datacollector.get_model_vars_dataframe()  # retrieve data from model
    data_trim = data.iloc[10:, ]  # remove some # of early runs
    # Condense data collectors into summary stats
    min = data_trim.min(axis=0)
    max = data_trim.max(axis=0)
    mean = data_trim.mean(axis=0)
    std = data_trim.std(axis=0)
    all_data = pd.concat([min, max, mean, std], axis=0)
    all_data["speed"] = speed_fixed  # add speed value column
    all_data["vision"] = vision_fixed  # add vision columnm
    all_data["separation"] = prior  # add separation column
    return pd.DataFrame(all_data).T


# Run model with prior called in create_tasks.py, as a float
sep_data = run_sep_model(float(sys.argv[1]))

# Re-name columns so all data will print & index with unique values for R.
sep_data.columns = ["cent_min", "nnd_min", "polar_min", "area_min",
                    "cent_max", "nnd_max", "polar_max", "area_max",
                    "cent_mean", "nnd_mean", "polar_mean", "area_mean",
                    "cent_std", "nnd_std", "polar_std", "area_std",
                    "speed", "vision", "sep"]

pd.set_option("display.max_columns", None)  # display all columns
pd.set_option("display.width", 1000)  # stop print from splitting columns on to new lines

print(sep_data)  # printing makes the data accessible from the cluster.
