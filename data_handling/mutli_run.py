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
# path_nnd = "/Users/Sophie/Desktop/DO NOT ERASE/1NUIG/Mackerel/Mackerel Data/NND runs"  # for laptop
path_priors = "/Users/Sophie/Desktop/DO NOT ERASE/1NUIG/Mackerel/Mackerel Data/prior runs"  # for laptop


def single_run(sd, vs, sp, co, sep, mt, n):
    """
    Run shoal model n times with fixed parameters values, collect data, and
    save output as a .csv file with a unique name.
    """
    model = ShoalModel(n_fish=20,
                       width=100,
                       height=100,
                       speed=sd,
                       vision=vs,
                       separation=sp,
                       cohere=co,
                       separate=sep,
                       match=mt)
    for i in range(300):  # number of steps
        model.step()
    data = model.datacollector.get_model_vars_dataframe()
    data.columns = ["cent", "nnd", "polar", "area"]
    data.to_csv(os.path.join(path, r"single_run_"+str(n)+".csv"))


# Run model n times with parameter values determined from the general ABC
for n in range(100):
    single_run(2.8, 9.7, 8.1, 0.53, 0.28, 0.54, n)


# def single_run_nnd(sd, vs, sp, co, sep, mt, n):
#     """
#     Run shoal model with just NND as the summary statistic n times with fixed
#     parameters values, collect data, and save output as a .csv file with a
#     unique name.
#     """
#     model = ShoalModel_nnd(n_fish=20,
#                            width=100,
#                            height=100,
#                            speed=sd,
#                            vision=vs,
#                            separation=sp,
#                            cohere=co,
#                            separate=sep,
#                            match=mt)
#     for i in range(300):
#         model.step()
#     data = model.datacollector.get_model_vars_dataframe()
#     data.columns = ["nnd"]
#     data.to_csv(os.path.join(path_nnd, r"single_run_nnd_"+str(n)+".csv"))
#
#
# # Run model n times with parameter values determined from the NND-only ABC
# for n in range(100):
#     single_run_nnd(9.5, 17.7, 3.9, 0.59, 0.42, 0.50, n)


def single_run_priors(sd, vs, sp, co, sep, mt, n):
    """
    Run shoal model n times with fixed parameters values, collect data, and
    save output as a .csv file with a unique name.
    """
    model = ShoalModel(n_fish=20,
                       width=100,
                       height=100,
                       speed=sd,
                       vision=vs,
                       separation=sp,
                       cohere=co,
                       separate=sep,
                       match=mt)
    for i in range(300):  # number of steps
        model.step()
    data = model.datacollector.get_model_vars_dataframe()
    data.columns = ["cent", "nnd", "polar", "area"]
    data.to_csv(os.path.join(path_priors, r"single_run_prior_"+str(n)+".csv"))


# Run model n times with mean prior distribution values before ABC
for n in range(100):
    single_run_priors(10, 10, 10, 0.5, 0.5, 0.5, n)
