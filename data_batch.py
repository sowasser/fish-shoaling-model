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
#
#
# model = ShoalModel(initial_fish=38,
#                    initial_obstruct=4000,
#                    width=100,
#                    height=100,
#                    speed=1,
#                    vision=10,
#                    separation=2)
#
# for _ in range(10):  # how many steps
#     model.step()
# data1 = model.datacollector.get_model_vars_dataframe()
# data1.to_csv(os.path.join(path, r"data1.csv"))
#
# for _ in range(10):
#     model.step()
# data2 = model.datacollector.get_model_vars_dataframe()
# data2.to_csv(os.path.join(path, r"data2.csv"))
#
# for _ in range(10):
#     model.step()
# data3 = model.datacollector.get_model_vars_dataframe()
# data3.to_csv(os.path.join(path, r"data3.csv"))


def mean_model(iterations):
    polar_all = np.asarray()
    nnd_all = np.asarray()
    area_all = np.asarray()
    cent_all = np.asarray()
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
        np_data = data.values
        polar_run = np_data[:, 1]
        polar_all = np.append(polar_run)
        nnd_run = np_data[:, 2]
        nnd_all = np.append(nnd_run)
        area_run = np_data[:, 3]
        area_all = np.append(area_run)
        cent_run = np_data[:, 4]
        cent_all = np.append(cent_run)
    return polar_all, nnd_all, area_all, cent_all


mean_model(range(2))
