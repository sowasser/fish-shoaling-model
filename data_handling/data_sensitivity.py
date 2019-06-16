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
import os

# Paths for exporting the data
# path = "/Users/user/Desktop/Local/Mackerel/Mackerel Data"
path = "/Users/Sophie/Desktop/DO NOT ERASE/1NUIG/Mackerel/Mackerel Data"

s = 100  # number of steps to run the model for each time
r = 30  # number of runs of the model


def run_model1(steps):
    """
    Runs the shoal model for a certain number of steps, returning a dataframe
    with all of the data collectors.
    """
    model = ShoalModel(n_fish=50,
                       width=50,
                       height=50,
                       speed=1,
                       vision=10,
                       separation=2)
    for j in range(steps):
        model.step()
    data1 = model.datacollector.get_model_vars_dataframe()
    return data1


# Isolate the polarization data from many runs of the model
p1 = pd.DataFrame()
for run in range(r):
    p1 = p1.append(run_model1(s).iloc[:, 0])  # add each run to data frame

# Isolate the nearest neighbour distance data from many runs of the model
n1 = pd.DataFrame()
for run in range(r):
    n1 = n1.append(run_model1(s).iloc[:, 1])

# Isolate the shoal area data from many runs of the model
a1 = pd.DataFrame()
for run in range(r):
    a1 = a1.append(run_model1(s).iloc[:, 2])

# Isolate the mean distance from the centroid data from many runs of the model
c1 = pd.DataFrame()
for run in range(r):
    c1 = c1.append(run_model1(s).iloc[:, 3])


def run_model2(steps):
    """
    Runs the shoal model for a certain number of steps, returning a dataframe
    with all of the data collectors.
    """
    model = ShoalModel(n_fish=50,
                       width=50,
                       height=50,
                       speed=10,
                       vision=10,
                       separation=2)
    for j in range(steps):
        model.step()
    data2 = model.datacollector.get_model_vars_dataframe()
    return data2


# Isolate the polarization data from many runs of the model
p2 = pd.DataFrame()
for run in range(r):
    p2 = p2.append(run_model2(s).iloc[:, 0])  # add each run to data frame

# Isolate the nearest neighbour distance data from many runs of the model
n2 = pd.DataFrame()
for run in range(r):
    n2 = n2.append(run_model2(s).iloc[:, 1])

# Isolate the shoal area data from many runs of the model
a2 = pd.DataFrame()
for run in range(r):
    a2 = a2.append(run_model2(s).iloc[:, 2])

# Isolate the mean distance from the centroid data from many runs of the model
c2 = pd.DataFrame()
for run in range(r):
    c2 = c2.append(run_model2(s).iloc[:, 3])


def run_model3(steps):
    """
    Runs the shoal model for a certain number of steps, returning a dataframe
    with all of the data collectors.
    """
    model = ShoalModel(n_fish=50,
                       width=50,
                       height=50,
                       speed=50,
                       vision=10,
                       separation=2)
    for j in range(steps):
        model.step()
    data3 = model.datacollector.get_model_vars_dataframe()
    return data3


# Isolate the polarization data from many runs of the model
p3 = pd.DataFrame()
for run in range(r):
    p3 = p3.append(run_model3(s).iloc[:, 0])  # add each run to data frame

# Isolate the nearest neighbour distance data from many runs of the model
n3 = pd.DataFrame()
for run in range(r):
    n3 = n3.append(run_model3(s).iloc[:, 1])

# Isolate the shoal area data from many runs of the model
a3 = pd.DataFrame()
for run in range(r):
    a3 = a3.append(run_model3(s).iloc[:, 2])

# Isolate the mean distance from the centroid data from many runs of the model
c3 = pd.DataFrame()
for run in range(r):
    c3 = c3.append(run_model3(s).iloc[:, 3])


# CALCULATE MEANS & CREATE DATA EXPORT ----------------------------------------

# Combine data from each model call into one dataframe, find means, combine again
means = pd.concat([pd.concat([p1, p2, p3]).mean(axis=1).reset_index(drop=True),
                   pd.concat([n1, n2, n3]).mean(axis=1).reset_index(drop=True),
                   pd.concat([a1, a2, a3]).mean(axis=1).reset_index(drop=True),
                   pd.concat([c1, c2, c3]).mean(axis=1).reset_index(drop=True)], axis=1)

# Add the variable values in question for each run & export
var = pd.Series([1] * r + [10] * r + [50] * r)
means = pd.concat([means, var], axis=1)
means.columns = ["polar", "nnd", "area", "centroid", "var"]
means.to_csv(os.path.join(path, r"means_var-speed.csv"))
