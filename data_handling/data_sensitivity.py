"""
This file is for testing the effect of different parameter values on the output
from the data collectors. These tests are used for validating the model with
Approximate Bayesian Computation, in R. The data collectors are:
    1. Polarization: a function returning the median absolute deviation of
       agent heading from the mean heading of the group
    2. Nearest neighbour distance: the mean distance of the 5 nearest agents,
       determined using a k-distance tree.
    3. Shoal area: convex hull
    4. Mean distance from centroid

The model is run for x steps for x number of values in a lognormal distribution
of parameter values and then the mean of each data collector per run (average
of all steps) is calculated and added to a dataframe along with the values of
all parameters: the one being tested, and the ones remaining fixed.

At the moment, agent speed, vision radius, and separation distance are being
tested in separate functions. These parameters are defined in shoal_model.py.
In the future, other parameters can be added & tested.
"""

from shoal_model import *
import pandas as pd
import itertools
import os

# Paths for exporting the data
path = "/Users/user/Desktop/Local/Mackerel/Mackerel Data"  # for desktop
# path = "/Users/Sophie/Desktop/DO NOT ERASE/1NUIG/Mackerel/Mackerel Data"  # for laptop

s = 5  # number of steps to run the model for each time
r = 3  # number of runs of the model

# SET PARAMETER VALUES --------------------------------------------------------
# Todo: update these values for whatever parameter you want to test.

# Todo: figure out how to run the model from a list of randomly-selected values from a lognormal distribution
speed_distrib = [0.5, 2, 5, 10, 20]

vis_distrib = [10, 10, 10, 10, 10]

sep_distrib = [2, 2, 2, 2, 2]

# Fixed values for non-testing parameters
speed_fixed = 2
vision_fixed = 10
sep_fixed = 2
# these are returning very high values - I guess the sum of the whole distribution?
# speed_dist = np.random.lognormal(mean=2, sigma=1, size=None)
# vis_dist = np.random.lognormal(mean=10, sigma=1, size=None)
# sep_dist = np.random.lognormal(mean=2, sigma=1, size=None)


# RUN MODELS & COLLECT DATA ---------------------------------------------------

def run_speed_model(steps, speed):
    """
    Runs the shoal model for a certain number of steps with speed varying while
    all other parameters are fixed. Returns a dataframe with the average per
    run of all data collectors (average of all steps) and columns with the
    parameter values for that run, including the varying & fixed parameters so
    all dataframes can be stacked together.
    """
    speed_parameter = []
    model = ShoalModel(n_fish=50,
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
    return pd.DataFrame(data.mean(axis=0)).T  # means of all columns & new dataframe


speed_data = pd.concat([run_speed_model(s, i) for i in speed_distrib])  # s is number of steps
print(speed_data)

# Todo: repeat the above for vision and separation

# EXPORT DATA -----------------------------------------------------------------
# Todo: remove early steps (burn-in) where the fish haven't started to cohere.

# speed_data.to_csv(os.path.join(path, r"means_var-speed.csv"))
