"""
This file is for running multiple iterations of the shoal model under set
conditions, rather than individual runs for looking at sensitivity, as housed
in the data_sensitivity.py file.

The Mesa batch runner allows you to change some of the variables and run
the model multiple times, but it's only capable of returning a single data
point, not one per step, like with the data collectors when the model is run
once.

In this code, the model is run within a function that can be called as many
times as needed...manually, unfortunately. Then the means are taken across all
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

path = "/Users/user/Desktop/Local/Mackerel/Mackerel Data"


def run_model(steps):
    """
    Runs the shoal model for a certain number of steps, returning a dataframe
    with all of the data collectors.
    """
    model = ShoalModel(initial_fish=38,
                       initial_obstruct=4000,
                       width=100,
                       height=100,
                       speed=1,
                       vision=10,
                       separation=2)
    for j in range(steps):
        model.step()
    data = model.datacollector.get_model_vars_dataframe()
    return data


s = 150  # number of steps to run the model for each time

# Isolate the polarization data from many runs of the model
p = pd.DataFrame([list(run_model(s).iloc[:, 0]), list(run_model(s).iloc[:, 0]), list(run_model(s).iloc[:, 0]),
                  list(run_model(s).iloc[:, 0]), list(run_model(s).iloc[:, 0]), list(run_model(s).iloc[:, 0]),
                  list(run_model(s).iloc[:, 0]), list(run_model(s).iloc[:, 0]), list(run_model(s).iloc[:, 0]),
                  list(run_model(s).iloc[:, 0])])
polar_mean = p.mean(axis=0)
polar_mean.to_csv(os.path.join(path, r"polar_mean.csv"))  # save data to use in R

# Isolate the nearest neighbour distance data from many runs of the model
n = pd.DataFrame([list(run_model(s).iloc[:, 1]), list(run_model(s).iloc[:, 1]), list(run_model(s).iloc[:, 1]),
                  list(run_model(s).iloc[:, 1]), list(run_model(s).iloc[:, 1]), list(run_model(s).iloc[:, 1]),
                  list(run_model(s).iloc[:, 1]), list(run_model(s).iloc[:, 1]), list(run_model(s).iloc[:, 1]),
                  list(run_model(s).iloc[:, 1])])
nnd_mean = n.mean(axis=0)
nnd_mean.to_csv(os.path.join(path, r"nnd_mean.csv"))

# Isolate the shoal area data from many runs of the model
a = pd.DataFrame([list(run_model(s).iloc[:, 2]), list(run_model(s).iloc[:, 2]), list(run_model(s).iloc[:, 2]),
                  list(run_model(s).iloc[:, 2]), list(run_model(s).iloc[:, 2]), list(run_model(s).iloc[:, 2]),
                  list(run_model(s).iloc[:, 2]), list(run_model(s).iloc[:, 2]), list(run_model(s).iloc[:, 2]),
                  list(run_model(s).iloc[:, 2])])
area_mean = a.mean(axis=0)
area_mean.to_csv(os.path.join(path, r"area_mean.csv"))

# Isolate the mean distance from the centroid data from many runs of the model
c = pd.DataFrame([list(run_model(s).iloc[:, 3]), list(run_model(s).iloc[:, 3]), list(run_model(s).iloc[:, 3]),
                  list(run_model(s).iloc[:, 3]), list(run_model(s).iloc[:, 3]), list(run_model(s).iloc[:, 3]),
                  list(run_model(s).iloc[:, 3]), list(run_model(s).iloc[:, 3]), list(run_model(s).iloc[:, 3]),
                  list(run_model(s).iloc[:, 3])])
cent_mean = c.mean(axis=0)
cent_mean.to_csv(os.path.join(path, r"cent_mean.csv"))
