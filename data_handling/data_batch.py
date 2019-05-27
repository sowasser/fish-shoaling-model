"""
This file is for running multiple iterations of the shoal model under set
conditions, rather than individual runs for looking at sensitivity, as housed
in the data_sensitivity.py file.

The Mesa batch runner allows you to change some of the variables and run
the model multiple times, but it's only capable of returning a single data
point, not one per step, like with the data collectors when the model is run
once.

In this code, the model is run within a function that can be called as many
times as needed...manually, unfortunately. The different data collectors Then the means are taken across all
of the model runs, for each step of the model.

# Todo: find some way to avoid doing this manually!
# Todo: find if there's some consistent amount of burn-in for shoal formation

Data are collected in the data_collectors.py script and are:
    1. Polarization: a function returning the median absolute deviation of
       agent heading from the mean heading of the group
    2. Nearest neighbour distance: the mean distance of the 5 nearest agents,
       determined using a k-distance tree.
    3. Shoal Area: convex hull
    4. Mean Distance From Centroid
"""

from shoal_model import *
import pandas as pd
import os
import matplotlib.pyplot as plt

path = "/Users/user/Desktop/Local/Mackerel/Mackerel Data"
# path = "/Users/Sophie/Desktop/DO NOT ERASE/1NUIG/Mackerel/Mackerel Data"  # for laptop


def run_model(steps):
    """
    Runs the shoal model for a certain number of steps, returning a dataframe
    with all of the data collectors.
    """
    model = ShoalModel()
    for j in range(steps):
        model.step()
    data = model.datacollector.get_model_vars_dataframe()
    return data


s = 10  # number of steps to run the model for each time
r = 10  # number of runs of the model


# Isolate the polarization data from many runs of the model
p = pd.DataFrame()
for run in range(r):
    p = p.append(run_model(s).iloc[:, 0])  # add each run to data frame
p = p.T  # transpose dataframe so each column is a run & each row is a step
# p.to_csv(os.path.join(path, r"polar_batch.csv"))  # save data to use in R


# Isolate the nearest neighbour distance data from many runs of the model
n = pd.DataFrame()
for run in range(r):
    n = n.append(run_model(s).iloc[:, 1])
n = n.T
# n.to_csv(os.path.join(path, r"nnd_batch.csv"))


# Isolate the shoal area data from many runs of the model
a = pd.DataFrame()
for run in range(r):
    a = a.append(run_model(s).iloc[:, 2])
a = a.T
# a.to_csv(os.path.join(path, r"area_batch.csv"))

# Isolate the mean distance from the centroid data from many runs of the model
c = pd.DataFrame()
for run in range(r):
    c = c.append(run_model(s).iloc[:, 3])
c = c.T
# c.to_csv(os.path.join(path, r"cent_batch.csv"))


# CALCULATE MEANS -------------------------------------------------------------

# For each step over all runs
mean_runs = pd.concat([p.mean(axis=1), n.mean(axis=1), a.mean(axis=1), c.mean(axis=1)], axis=1)
mean_runs.columns = ["polar", "nnd", "area", "centroid"]

# For each run over all steps
# TODO: find a way to do this that is more helpful, if it's actually needed
# mean_steps = pd.concat([p.mean(axis=0), n.mean(axis=0), a.mean(axis=0), c.mean(axis=0)], axis=0)

# For all steps and all runs
overall_mean = pd.DataFrame(mean_runs.mean(axis=0))  # mean of each data collector for all steps and all runs

# mean_runs.to_csv(os.path.join(path, r"batch_means.csv"))
# overall_mean.to_csv(os.path.join(path, r"overall_means.csv"))
