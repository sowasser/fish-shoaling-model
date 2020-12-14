"""
Script for running single_run.py many times and collecting all of the output
files in a folder so they can be read into R as examples of multiple versions
of the model run with the same parameters.
"""

from shoal_model import *
from shoal_model_nnd import *
import os
import matplotlib.pyplot as plt

# path = "/Users/user/Desktop/Local/Mackerel/Mackerel Data"
path = "/Users/Sophie/Desktop/DO NOT ERASE/1NUIG/Mackerel/Mackerel Data/general runs"  # for laptop
path_nnd = "/Users/Sophie/Desktop/DO NOT ERASE/1NUIG/Mackerel/Mackerel Data/NND runs"  # for laptop


def single_run(n):
    # Collect the data from a single run with x number of steps into a dataframe
    model = ShoalModel(n_fish=20,
                       width=100,
                       height=100,
                       speed=9.5,
                       vision=17.7,
                       separation=3.9,
                       cohere=0.59,
                       separate=0.42,
                       match=0.50)
    for i in range(300):
        model.step()
    data = model.datacollector.get_model_vars_dataframe()
    data.columns = ["cent", "nnd", "polar", "area"]
    data.to_csv(os.path.join(path, r"single_run_"+str(n)+".csv"))


# Run model n times with all of the same parameters
for n in range(2):
    single_run(n)


def single_run_nnd(n):
    # Collect the data from a single run with x number of steps into a dataframe
    model = ShoalModel_nnd(n_fish=20,
                           width=100,
                           height=100,
                           speed=9.5,
                           vision=17.7,
                           separation=3.9,
                           cohere=0.59,
                           separate=0.42,
                           match=0.50)
    for i in range(300):
        model.step()
    data = model.datacollector.get_model_vars_dataframe()
    data.columns = ["nnd"]
    data.to_csv(os.path.join(path_nnd, r"single_run_nnd_"+str(n)+".csv"))


# Run model n times with all of the same parameters
for n in range(2):
    single_run_nnd(n)

# save data with NND-only ABC determined parameters
# data.to_csv(os.path.join(path, r"single_run_nnd.csv"))
