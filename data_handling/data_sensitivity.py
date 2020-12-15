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
# path = "/Users/user/Desktop"  # for testing
path = "/Users/Sophie/Desktop/DO NOT ERASE/1NUIG/Mackerel/Mackerel Data"  # for laptop

# SET PARAMETER & MODEL VALUES ------------------------------------------------

runs = 100

# Fixed values for non-tested parameters
speed_fixed = 10
vision_fixed = 10
sep_fixed = 10
cohere_fixed = 0.5
separate_fixed = 0.5
match_fixed = 0.5


# Defines the distribution as a range of values. Size is # of variables (and
# therefore runs of the model), a is the number that the distribution is based
# around.
speed_dist = np.random.uniform(low=0, high=20, size=runs)
vision_dist = np.random.uniform(low=0, high=20, size=runs)
sep_dist = np.random.uniform(low=0, high=20, size=runs)
cohere_dist = np.random.uniform(low=0, high=1, size=runs)
separate_dist = np.random.uniform(low=0, high=1, size=runs)
match_dist = np.random.uniform(low=0, high=1, size=runs)

steps = 300  # number of steps to run the model for each time

burn_in = 200  # number of steps to exclude at the beginning as collective behaviour emerges


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
                       width=100,
                       height=100,
                       speed=speed,
                       vision=vision_fixed,
                       separation=sep_fixed,
                       cohere=cohere_fixed,
                       separate=separate_fixed,
                       match=match_fixed)
    for step in range(steps):
        model.step()  # run the model for certain number of steps
        speed_parameter.append(speed)  # create list of parameter values tested
    data = model.datacollector.get_model_vars_dataframe()  # retrieve data from model
    data["speed"] = speed_parameter  # add parameter value column
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
                       width=100,
                       height=100,
                       speed=speed_fixed,
                       vision=vision,
                       separation=sep_fixed,
                       cohere=cohere_fixed,
                       separate=separate_fixed,
                       match=match_fixed)
    for step in range(steps):
        model.step()  # run the model for certain number of steps
        vision_parameter.append(vision)  # create list of parameter values tested
    data = model.datacollector.get_model_vars_dataframe()  # retrieve data from model
    data["vision"] = vision_parameter  # add vision column
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
                       width=100,
                       height=100,
                       speed=speed_fixed,
                       vision=vision_fixed,
                       separation=separation,
                       cohere=cohere_fixed,
                       separate=separate_fixed,
                       match=match_fixed)
    for step in range(steps):
        model.step()  # run the model for certain number of steps
        sep_parameter.append(separation)  # create list of parameter values tested
    data = model.datacollector.get_model_vars_dataframe() # retrieve data from model
    data["separation"] = sep_parameter  # add separation column
    data_trim = data.iloc[burn_in:, ]  # remove early runs
    return pd.DataFrame(data_trim.mean(axis=0)).T  # return means of all columns & transposed

# Run the model as many times as there are parameter values, for # of steps in "s"
# sep_data = pd.concat([run_sep_model(s, i) for i in sep_dist])


def run_cohere_model(cohere):
    """
    Runs the shoal model for a certain number of steps with coherence vector
    varying while all other parameters are fixed. Returns a dataframe with the
    average per run of all data collectors (average of all steps) and columns
    with the parameter values for that run, including the varying & fixed
    parameters so all dataframes can be stacked together.
    """
    cohere_parameter = []
    model = ShoalModel(n_fish=20,
                       width=100,
                       height=100,
                       speed=speed_fixed,
                       vision=vision_fixed,
                       separation=sep_fixed,
                       cohere=cohere,
                       separate=separate_fixed,
                       match=match_fixed)
    for step in range(steps):
        model.step()  # run the model for certain number of steps
        cohere_parameter.append(cohere)  # create list of parameter values tested
    data = model.datacollector.get_model_vars_dataframe() # retrieve data from model
    data["cohere"] = cohere_parameter  # add cohere column
    data_trim = data.iloc[burn_in:, ]  # remove early runs
    return pd.DataFrame(data_trim.mean(axis=0)).T  # return means of all columns & transposed


def run_separate_model(separate):
    """
    Runs the shoal model for a certain number of steps with separate vector
    varying while all other parameters are fixed. Returns a dataframe with the
    average per run of all data collectors (average of all steps) and columns
    with the parameter values for that run, including the varying & fixed
    parameters so all dataframes can be stacked together.
    """
    separate_parameter = []
    model = ShoalModel(n_fish=20,
                       width=100,
                       height=100,
                       speed=speed_fixed,
                       vision=vision_fixed,
                       separation=sep_fixed,
                       cohere=cohere_fixed,
                       separate=separate,
                       match=match_fixed)
    for step in range(steps):
        model.step()  # run the model for certain number of steps
        separate_parameter.append(separate)  # create list of parameter values tested
    data = model.datacollector.get_model_vars_dataframe() # retrieve data from model
    data["separate"] = separate_parameter  # add separate column
    data_trim = data.iloc[burn_in:, ]  # remove early runs
    return pd.DataFrame(data_trim.mean(axis=0)).T  # return means of all columns & transposed


def run_match_model(match):
    """
    Runs the shoal model for a certain number of steps with separate vector
    varying while all other parameters are fixed. Returns a dataframe with the
    average per run of all data collectors (average of all steps) and columns
    with the parameter values for that run, including the varying & fixed
    parameters so all dataframes can be stacked together.
    """
    match_parameter = []
    model = ShoalModel(n_fish=20,
                       width=100,
                       height=100,
                       speed=speed_fixed,
                       vision=vision_fixed,
                       separation=sep_fixed,
                       cohere=cohere_fixed,
                       separate=separate_fixed,
                       match=match)
    for step in range(steps):
        model.step()  # run the model for certain number of steps
        match_parameter.append(match)  # create list of parameter values tested
    data = model.datacollector.get_model_vars_dataframe() # retrieve data from model
    data["match"] = match_parameter  # add match column
    data_trim = data.iloc[burn_in:, ]  # remove early runs
    return pd.DataFrame(data_trim.mean(axis=0)).T  # return means of all columns & transposed


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
    cohere_data = p.map(run_cohere_model, [i for i in cohere_dist])
    separate_data = p.map(run_separate_model, [i for i in separate_dist])
    match_data = p.map(run_match_model, [i for i in match_dist])
    p.close()
    speed_data = pd.concat(speed_data)  # change into data format for export
    vision_data = pd.concat(vision_data)
    sep_data = pd.concat(sep_data)
    cohere_data = pd.concat(cohere_data)
    separate_data = pd.concat(separate_data)
    match_data = pd.concat(match_data)
    print("Time taken = {} minutes".format((time.time() - start)/60))  # print how long it took

# EXPORT DATA -----------------------------------------------------------------

speed_data.to_csv(os.path.join(path, r"var-speed100.csv"), index=False)
vision_data.to_csv(os.path.join(path, r"var-vision100.csv"), index=False)
sep_data.to_csv(os.path.join(path, r"var-sep100.csv"), index=False)
cohere_data.to_csv(os.path.join(path, r"var-cohere100.csv"), index=False)
separate_data.to_csv(os.path.join(path, r"var-separate100.csv"), index=False)
match_data.to_csv(os.path.join(path, r"var-match100.csv"), index=False)
