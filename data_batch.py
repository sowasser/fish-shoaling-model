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


def run_polar(steps):
    """
    Runs the shoal model for a certain number of steps and pulls out polarization.
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
    polar_run = data.iloc[:, 0]
    return list(polar_run)


multi = pd.DataFrame([run_polar(10), run_polar(10), run_polar(10)])
means = multi.mean(axis=0)
