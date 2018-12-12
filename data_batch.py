"""
This file is for running multiple iterations of the shoal model under set
conditions, rather than individual runs for looking at sensitivity, as housed
in the data_sensitivity.py file.

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

# path = "/Users/user/Desktop/Local/Mackerel/Mackerel Data"


def mean_model(iterations):
    """
    Runs the model many times and takes the average of all data collectors for
    all runs for each step of the model.
    """
    steps = pd.DataFrame()
    for i in iterations:
        model = ShoalModel(initial_fish=38,
                           initial_obstruct=4000,
                           width=100,
                           height=100,
                           speed=1,
                           vision=10,
                           separation=2)
        for j in range(10):
            model.step()
        data = model.datacollector.get_model_vars_dataframe()
        polar_run = data.iloc[:, 0]
        polar_all = steps.append(polar_run, ignore_index=True)
        # nnd_run = data.iloc[:, 1]
        # nnd_all = steps.append(nnd_run, ignore_index=True)
        # area_run = data.iloc[:, 2]
        # area_all = steps.append(area_run, ignore_index=True)
        # cent_run = data.iloc[:, 3]
        # cent_all = steps.append(cent_run, ignore_index=True)
        # return polar_all, nnd_all, area_all, cent_all
    return polar_all


mean_model(range(2))
