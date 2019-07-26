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
path = "/Users/user/Desktop/Local/Mackerel/Mackerel Data"  # for desktop
# path = "/Users/Sophie/Desktop/DO NOT ERASE/1NUIG/Mackerel/Mackerel Data"  # for laptop

s = 3  # number of steps to run the model for each time
r = 10  # number of runs of the model

# SET PARAMETER VALUES --------------------------------------------------------
# Todo: update these values for whatever parameter you want to test.
speed1 = 1
speed2 = 5
speed3 = 10
speed4 = 15
speed5 = 20

vis1 = 10
vis2 = 10
vis3 = 10
vis4 = 10
vis5 = 10

sep1 = 2
sep2 = 2
sep3 = 2
sep4 = 2
sep5 = 2


# RUN MODELS & COLLECT DATA ---------------------------------------------------

def run_model1(steps):
    """
    Runs the shoal model for a certain number of steps, returning a dataframe
    with all of the data collectors.
    """
    model = ShoalModel(n_fish=50,
                       width=50,
                       height=50,
                       speed=speed1,
                       vision=vis1,
                       separation=sep1)
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
                       speed=speed2,
                       vision=vis2,
                       separation=sep2)
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
                       speed=speed3,
                       vision=vis3,
                       separation=sep3)
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


def run_model4(steps):
    """
    Runs the shoal model for a certain number of steps, returning a dataframe
    with all of the data collectors.
    """
    model = ShoalModel(n_fish=50,
                       width=50,
                       height=50,
                       speed=speed4,
                       vision=vis4,
                       separation=sep4)
    for j in range(steps):
        model.step()
    data4 = model.datacollector.get_model_vars_dataframe()
    return data4


# Isolate the polarization data from many runs of the model
p4 = pd.DataFrame()
for run in range(r):
    p4 = p4.append(run_model4(s).iloc[:, 0])  # add each run to data frame

# Isolate the nearest neighbour distance data from many runs of the model
n4 = pd.DataFrame()
for run in range(r):
    n4 = n4.append(run_model4(s).iloc[:, 1])

# Isolate the shoal area data from many runs of the model
a4 = pd.DataFrame()
for run in range(r):
    a4 = a4.append(run_model4(s).iloc[:, 2])

# Isolate the mean distance from the centroid data from many runs of the model
c4 = pd.DataFrame()
for run in range(r):
    c4 = c4.append(run_model4(s).iloc[:, 3])


def run_model5(steps):
    """
    Runs the shoal model for a certain number of steps, returning a dataframe
    with all of the data collectors.
    """
    model = ShoalModel(n_fish=50,
                       width=50,
                       height=50,
                       speed=speed5,
                       vision=vis5,
                       separation=sep5)
    for j in range(steps):
        model.step()
    data5 = model.datacollector.get_model_vars_dataframe()
    return data5


# Isolate the polarization data from many runs of the model
p5 = pd.DataFrame()
for run in range(r):
    p5 = p5.append(run_model5(s).iloc[:, 0])  # add each run to data frame

# Isolate the nearest neighbour distance data from many runs of the model
n5 = pd.DataFrame()
for run in range(r):
    n5 = n5.append(run_model5(s).iloc[:, 1])

# Isolate the shoal area data from many runs of the model
a5 = pd.DataFrame()
for run in range(r):
    a5 = a5.append(run_model5(s).iloc[:, 2])

# Isolate the mean distance from the centroid data from many runs of the model
c5 = pd.DataFrame()
for run in range(r):
    c5 = c5.append(run_model5(s).iloc[:, 3])

# CALCULATE MEANS & CREATE DATA EXPORT ----------------------------------------

# Combine data from each model call into one dataframe, find means, combine again
means = pd.concat([pd.concat([p1, p2, p3, p4, p5]).mean(axis=1).reset_index(drop=True),
                   pd.concat([n1, n2, n3, n4, n5]).mean(axis=1).reset_index(drop=True),
                   pd.concat([a1, a2, a3, a4, a5]).mean(axis=1).reset_index(drop=True),
                   pd.concat([c1, c2, c3, c4, c5]).mean(axis=1).reset_index(drop=True)], axis=1)

# Add the parameter values for each run & export
speed = pd.Series([speed1] * r +
                  [speed2] * r +
                  [speed3] * r +
                  [speed4] * r +
                  [speed5] * r)
vision = pd.Series([vis1] * r +
                   [vis2] * r +
                   [vis3] * r +
                   [vis4] * r +
                   [vis5] * r)
sep = pd.Series([sep1] * r +
                [sep2] * r +
                [sep3] * r +
                [sep4] * r +
                [sep5] * r)

means = pd.concat([means, speed, sep, vision], axis=1)
means.columns = ["polar", "nnd", "area", "centroid", "speed", "vision", "separation"]

# Todo: change the name of the file to represent parameter varied
means.to_csv(os.path.join(path, r"means_var-speed.csv"))
