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
import multiprocessing
import time
import os

# path = "/Users/user/Desktop/Local/Mackerel/Mackerel Data"  # for desktop
path = "/Users/Sophie/Desktop/DO NOT ERASE/1NUIG/Mackerel/Mackerel Data"  # for laptop

s = 300  # number of steps to run the model for each time
runs = range(100)  # number of runs/iterations of the model for finding the mean
burn_in = 100  # number of steps to exclude at the beginning as collective behaviour emerges


def run_model(steps):
    """
    Runs the shoal model for a certain number of steps, returning a dataframe
    with all of the data collectors.
    """
    model = ShoalModel(n_fish=20,
                       width=50,
                       height=50,
                       speed=1,
                       vision=4.6,
                       separation=3.2,
                       cohere=0.47,
                       separate=0.31,
                       match=0.65)
    for step in range(steps):
        model.step()  # run the model for certain number of steps
    data = model.datacollector.get_model_vars_dataframe()  # retrieve data from model
    data_trim = data.iloc[burn_in:, ]  # remove early runs
    return data_trim.T  # data transposed to make means calculation easier


# RUN MODELS MANY TIMES, FIND MEAN FOR EACH STEP, EXPORT ----------------------
# Runs the model for as many times as defined above in "runs", using multiple
# cores. Number of processes is set to 10, but can be reduced if other work
# needs to be done on the computer that requires CPU space.
# Also prints how long it took, for reference.

if __name__ == '__main__':
    start = time.time()
    p = multiprocessing.Pool(processes=10)  # 10 processes seems to be a sweet spot
    polar = pd.concat([run_model(s).iloc[0:1, ] for r in runs])
    nnd = pd.concat([run_model(s).iloc[1:2, ] for r in runs])
    area = pd.concat([run_model(s).iloc[2:3, ] for r in runs])
    cent = pd.concat([run_model(s).iloc[3:4, ] for r in runs])
    step_means = pd.concat([polar.mean(axis=0),
                            nnd.mean(axis=0),
                            area.mean(axis=0),
                            cent.mean(axis=0)], axis=1)
    step_means.columns = ["cent", "nnd", "polar", "area"]
    print("Time taken = {} minutes".format((time.time() - start) / 60))  # print how long it took

# Export data
step_means.to_csv(os.path.join(path, "step_means_17June.csv"))
