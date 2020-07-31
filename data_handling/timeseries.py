# Script for conducting timeseries analyses that I am less familiar with how to
# do in R. Data are created in the single_run.py file, then exported as .csv.

import pandas as pd
import os
import numpy as np

# path = "/Users/user/Desktop/Local/Mackerel/Mackerel Data"  # for desktop
path = "/Users/Sophie/Desktop/DO NOT ERASE/1NUIG/Mackerel/Mackerel Data"  # for laptop

modelled = pd.read_csv(filepath_or_buffer=os.path.join(path, r"timeseries_modelled.csv"),
                       sep=",")
modelled = modelled.drop(modelled.columns[0], axis=1)  # drop first column

tracked = pd.read_csv(filepath_or_buffer=os.path.join(path, r"timeseries_tracked.csv"),
                      sep=",")
tracked = tracked.drop(tracked.columns[0], axis=1)  # drop first column


# Find percentage overlap
def find_overlap(list1, list2):
    """
    Determine the percentage overlap between to datasets (list1 and list2). For
    every value of df1 that is within the range of df2, add to an initial value
    and then find what percentage that value is of the original (list1)
    """
    value = []
    for i in list1:
        if min(list2) <= i <= max(list2):
            value.append(i)
    percentage = (len(value) / len(list1)) * 100
    return percentage


cent_percent = find_overlap(modelled["cent"], tracked["cent"])  # 85.9%
nnd_percent = find_overlap(modelled["nnd"], tracked["nnd"])  # 0
nnd_only_percent = find_overlap(modelled["nnd_only"], tracked["nnd"])  # 23.2%
polar_percent = find_overlap(modelled["polar"], tracked["polar"])  # 74.7%
area_percent = find_overlap(modelled["area"], tracked["area"])  # 0
