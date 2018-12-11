"""
This file is for running multiple iterations of the shoal model under set
conditions, rather than individual runs for looking at sensitivity, as housed
in the data_sensitivity.py file.

The Batch Runner allows you to determine which parameters you'd like to keep
static across the multiple model runs and which you'd like to vary.

Data are collected in the data_collectors.py script and are:
    1. Polarization: a function returning the median absolute deviation of
       agent heading from the mean heading of the group
    2. Nearest neighbour distance: the mean distance of the 5 nearest agents,
       determined using a k-distance tree.
    3. Shoal Area: convex hull
    4. Mean Distance From Centroid
"""

from shoal_model import *
from mesa.batchrunner import BatchRunner
import pandas as pd
import os

path = "/Users/user/Desktop/Local/Mackerel/Mackerel Data"

# Todo: fix batch runner so it works!!!
# fixed_params = {"initial_fish": 38,
#                 "initial_obstruct": 4000,
#                 "width": 100,
#                 "height": 100}
#
# variable_params = {"speed": range(1, 1, 1),
#                    "vision": range(10, 10, 10),
#                    "separation": range(2, 2, 2)}
#
# batch_run = BatchRunner(ShoalModel,
#                         fixed_parameters=fixed_params,
#                         variable_parameters=variable_params,
#                         iterations=10,  # instantiations of the model
#                         max_steps=10,  # Run each for 100 steps
#                         model_reporters={"Polarization": polar,
#                                          "NND": nnd,
#                                          "Shoal Area": area,
#                                          "Mean Distance from Centroid": centroid_dist})
# batch_run.run_all()
#
#
# # Data collection methods
# # Extract data as a DataFrame
# batch_data = batch_run.get_model_vars_dataframe()
#
# batch_data.to_csv(os.path.join(path, r"batch_data.csv"), index=",")


model = ShoalModel(initial_fish=38,
                   initial_obstruct=4000,
                   width=100,
                   height=100,
                   speed=1,
                   vision=10,
                   separation=2)

for a in range(10):  # how many steps
    model.step()
data1 = model.datacollector.get_model_vars_dataframe()

for b in range(10):
    model.step()
data2 = model.datacollector.get_model_vars_dataframe()

for c in range(10):
    model.step()
data3 = model.datacollector.get_model_vars_dataframe()
