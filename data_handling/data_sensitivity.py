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

The model is run for x steps for x number of values in a gamma distribution
of parameter values and then the mean of each data collector per run (average
of all steps) is calculated and added to a dataframe along with the values of
all parameters: the one being tested, and the ones remaining fixed.

The distributions and their approximate shape can be checked and visualized in
the distributions.py file in the data_handling folder.

At the moment, agent speed, vision radius, and separation distance are being
tested in separate functions. These parameters are defined in shoal_model.py.
In the future, other parameters can be added & tested.
"""

from shoal_model import *
import pandas as pd
from scipy.stats import gamma
import multiprocessing
import time
import os


# Paths for exporting the data
# path = "/Users/user/Desktop/Local/Mackerel/Mackerel Data"  # for desktop
path = "/Users/user/Desktop"  # for testing
# path = "/Users/Sophie/Desktop/DO NOT ERASE/1NUIG/Mackerel/Mackerel Data"  # for laptop

# SET PARAMETER & MODEL VALUES ------------------------------------------------

# Fixed values for non-tested parameters
speed_fixed = 2
vision_fixed = 10
sep_fixed = 2

# Todo: figure out how to get the range we want. Must be non-negative!

# Defines the distribution as a range of values. Size is # of variables (and
# therefore runs of the model), a is the number that the distribution is based
# around.
speed_dist = gamma.rvs(size=10, a=2)
vision_dist = gamma.rvs(size=10, a=10)
sep_dist = gamma.rvs(size=10, a=2)

# Defines the distribution as a set of repeated values
# speed_params = [0.1, 0.5, 2, 5, 8]  # values to repeat & run
# speed_dist = np.repeat(speed_params, 10).tolist()  # repeats above list n times
#
# vision_params = [1, 5, 10, 15, 25]
# vision_dist = np.repeat(vision_params, 10).tolist()
#
# sep_params = [0.1, 0.5, 2, 5, 8]
# sep_dist = np.repeat(sep_params, 10).tolist()

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


# Run the model as many times as there are parameter values, for # of steps in "s"
# speed_data = pd.concat([run_speed_model(s, i) for i in speed_dist])


def run_vision_model(vision):
    """
    Runs the shoal model for a certain number of steps with vision radius
    varying while all other parameters are fixed. Returns a dataframe with the
    average per run of all data collectors (average of all steps) and columns
    with the parameter values for that run, including the varying & fixed
    parameters so all dataframes can be stacked together.
    """
    vision_parameter = []
    model = ShoalModel(n_fish=20,
                       width=50,
                       height=50,
                       speed=speed_fixed,
                       vision=vision,
                       separation=sep_fixed)
    for step in range(steps):
        model.step()  # run the model for certain number of steps
        vision_parameter.append(vision)  # create list of parameter values tested
    data = model.datacollector.get_model_vars_dataframe()  # retrieve data from model
    data["speed"] = speed_fixed  # add parameter value column
    data["vision"] = vision_parameter  # add vision column
    data["separation"] = sep_fixed  # add separation column
    data_trim = data.iloc[burn_in:, ]  # remove early runs
    return pd.DataFrame(data_trim.mean(axis=0)).T  # return means of all columns & transposed


# Run the model as many times as there are parameter values, for # of steps in "s"
# vision_data = pd.concat([run_vision_model(s, i) for i in vision_dist])


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


# Run the model as many times as there are parameter values, for # of steps in "s"
# sep_data = pd.concat([run_sep_model(s, i) for i in sep_dist])

# MULTIPROCESSING -------------------------------------------------------------
# Runs the model for as many times as is in the distribution of values above,
# using multiple cores. Number of processes is set to 10, but can be reduced
# if other work needs to be done on the computer that requires CPU space.
# Also prints how long it took, for reference.

if __name__ == '__main__':
    start = time.time()
    p = multiprocessing.Pool(processes=10)  # 10 processes seems to be a sweet spot
    speed_data = p.map(run_speed_model, [i for i in speed_dist])
    vision_data = p.map(run_vision_model, [i for i in vision_dist])
    sep_data = p.map(run_sep_model, [i for i in sep_dist])
    p.close()
    speed_data = pd.concat(speed_data)  # change into data format for export
    vision_data = pd.concat(vision_data)
    sep_data = pd.concat(sep_data)
    print("Time taken = {} minutes".format((time.time() - start)/60))  # print how long it took

# EXPORT DATA -----------------------------------------------------------------

speed_data.to_csv(os.path.join(path, r"var-speed.csv"), index=False)
vision_data.to_csv(os.path.join(path, r"var-vision.csv"), index=False)
sep_data.to_csv(os.path.join(path, r"var-sep.csv"), index=False)
