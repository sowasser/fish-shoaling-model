"""
This file is for testing the effect of different model conditions on the output
from the data collectors. These tests are used for validating the model with
Approximate Bayesian Computation, in R. The data collectors are:
    1. Polarization: a function returning the median absolute deviation of
       agent heading from the mean heading of the group
    2. Nearest neighbour distance: the mean distance of the 5 nearest agents,
       determined using a k-distance tree.
    3. Shoal area: convex hull
    4. Mean distance from centroid

The model is run for x steps, x number of times and then the mean of each data
collector per run (average of all steps) is calculated and added to a dataframe
along with the parameter being tested (i.e. speed, vision, etc.)
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

speed_distrib = [0.5, 2, 5, 10, 20]
# speed1 = 2
# speed2 = 2
# speed3 = 2
# speed4 = 2
# speed5 = 2

vis_distrib = [10, 10, 10, 10, 10]
# vis1 = 10
# vis2 = 10
# vis3 = 10
# vis4 = 10
# vis5 = 10

sep_distrib = [2, 2, 2, 2, 2]
# sep1 = 0.5
# sep2 = 2
# sep3 = 5
# sep4 = 10
# sep5 = 20

# Todo: figure out how to run the model over random samples from a lognormal distribution
# these are returning very high values - I guess the sum of the whole distribution?
# speed_dist = np.random.lognormal(mean=2, sigma=1, size=None)
# vis_dist = np.random.lognormal(mean=10, sigma=1, size=None)
# sep_dist = np.random.lognormal(mean=2, sigma=1, size=None)


# RUN MODELS & COLLECT DATA ---------------------------------------------------


def run_speed_model(steps, speed):
    """
    Runs the shoal model for a certain number of steps with speed varying while
    all other parameters are fixed. Returns a dataframe with all of the data
    collectors and a column with the speed parameter values.
    """
    speed_parameter = []
    model = ShoalModel(n_fish=50,
                       width=50,
                       height=50,
                       speed=speed,
                       vision=10,
                       separation=2)
    for step in range(steps):
        model.step()  # run the model for certain number of steps
        speed_parameter.append(speed)  # create list of parameter values tested
    data = model.datacollector.get_model_vars_dataframe()  # retrieve data from model
    data["speed"] = speed_parameter  # add parameter value column
    return data

p = pd.DataFrame()
n = pd.DataFrame()
a = pd.DataFrame()
c = pd.DataFrame()

speed_data = pd.concat([run_speed_model(s, i) for i in speed_distrib])
print(speed_data)



    # Isolate the polarization data from many runs of the model
    # for run in range(r):
    #     p = run_model(s).iloc[:, 0]  # add each run to data frame
    #
    # # Isolate the nearest neighbour distance data from many runs of the model
    # for run in range(r):
    #     n = run_model(s).iloc[:, 1]
    #
    # # Isolate the shoal area data from many runs of the model
    # for run in range(r):
    #     a = run_model(s).iloc[:, 2]
    #
    # # Isolate the mean distance from the centroid data from many runs of the model
    # for run in range(r):
    #     c = run_model(s).iloc[:, 3]


# CALCULATE MEANS & CREATE DATA EXPORT ----------------------------------------

# Todo: remove early steps (burn-in) where the fish haven't started to cohere.

# # Combine data from each model call into one dataframe, find means, combine again
# means = pd.concat([pd.concat([p1, p2, p3, p4, p5]).mean(axis=1).reset_index(drop=True),
#                    pd.concat([n1, n2, n3, n4, n5]).mean(axis=1).reset_index(drop=True),
#                    pd.concat([a1, a2, a3, a4, a5]).mean(axis=1).reset_index(drop=True),
#                    pd.concat([c1, c2, c3, c4, c5]).mean(axis=1).reset_index(drop=True)], axis=1)
#
# # Add the parameter values for each run & export
# speed = pd.Series([speed1] * r +
#                   [speed2] * r +
#                   [speed3] * r +
#                   [speed4] * r +
#                   [speed5] * r)
# vision = pd.Series([vis1] * r +
#                    [vis2] * r +
#                    [vis3] * r +
#                    [vis4] * r +
#                    [vis5] * r)
# separation = pd.Series([sep1] * r +
#                        [sep2] * r +
#                        [sep3] * r +
#                        [sep4] * r +
#                        [sep5] * r)
#
# means = pd.concat([means, speed, vision, separation], axis=1)
# means.columns = ["polar", "nnd", "area", "centroid", "speed", "vision", "separation"]
#
# # Todo: change the name of the file to represent parameter varied
# means.to_csv(os.path.join(path, r"means_var-sep.csv"))
