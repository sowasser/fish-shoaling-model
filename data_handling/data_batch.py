"""
This file is for running multiple iterations of the shoal model under set
conditions, rather than individual runs for looking at sensitivity, as housed
in the data_sensitivity.py file.

The Mesa batch runner allows you to change some of the variables and run
the model multiple times, but it's only capable of returning a single data
point, not one per step, like with the data collectors when the model is run
once.

In this code, the model is run within a function that can be called as many
times as needed. Then the means of each data collector are taken across all
of the model runs, for each step of the model.

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

path = "/Users/user/Desktop/Local/Mackerel/Mackerel Data"  # for desktop
# path = "/Users/Sophie/Desktop/DO NOT ERASE/1NUIG/Mackerel/Mackerel Data"  # for laptop

s = 200  # number of steps to run the model for each time
runs = range(100)  # number of runs/iterations of the model for finding the mean


def run_model(steps):
    """
    Runs the shoal model for a certain number of steps, returning a dataframe
    with all of the data collectors.
    """
    model = ShoalModel(n_fish=50,
                       width=50,
                       height=50,
                       speed=2,
                       vision=10,
                       separation=2)
    for step in range(steps):
        model.step()  # run the model for certain number of steps
    data = model.datacollector.get_model_vars_dataframe()  # retrieve data from model
    return data.T  # data transposed to make means calculation easier


# RUN MODELS MANY TIMES, FIND MEAN FOR EACH STEP, EXPORT ----------------------

polar = pd.concat([run_model(s).iloc[0:1, ] for r in runs])
nnd = pd.concat([run_model(s).iloc[1:2, ] for r in runs])
area = pd.concat([run_model(s).iloc[2:3, ] for r in runs])
cent = pd.concat([run_model(s).iloc[3:4, ] for r in runs])

step_means = pd.concat([polar.mean(axis=0),
                        nnd.mean(axis=0),
                        area.mean(axis=0),
                        cent.mean(axis=0)], axis=1)
step_means.columns = ["polar", "nnd", "area", "centroid"]

step_means.to_csv(os.path.join(path, "step_means.csv"))
