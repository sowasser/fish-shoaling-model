"""
This file is for running multiple iterations of the shoal model under set
conditions, rather than individual runs for looking at sensitivity, as housed
in the sensitivity_data.py file. This method provides the overall distributions
of the model. The process is automated by Mesa.

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


parameters = {"population": 100,
              "width": 100,
              "height": 100,
              "speed": 1,
              "vision": 10,
              "separation": 2}

batch_run = BatchRunner(ShoalModel,
                        parameters,
                        iterations=1,
                        # 5 instantiations of the model
                        max_steps=100,  # Run each for 100 steps
                        model_reporters={"Polarization": polar,
                                         "NND": nnd,
                                         "Shoal Area": area,
                                         "Mean Distance from Centroid": centroid_dist})
batch_run.run_all()


# Data collection methods
# Extract data as a DataFrame 
batch_data = batch_run.get_model_vars_dataframe()
print(batch_data)