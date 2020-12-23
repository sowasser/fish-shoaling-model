# Script for conducting timeseries analyses that I am less familiar with how to
# do in R. Data are created in the single_run.py file, then exported as .csv.

import pandas as pd
import os
import numpy as np

# path = "/Users/user/Desktop/Local/Mackerel/Mackerel Data"  # for desktop
path = "/Users/Sophie/Desktop/DO NOT ERASE/1NUIG/Mackerel/Mackerel Data"  # for laptop

# Read in data generated from timeseries.R
g_nnd = pd.read_csv(filepath_or_buffer=os.path.join(path, r"ts_general_NND.csv"))
g_cent = pd.read_csv(filepath_or_buffer=os.path.join(path, r"ts_general_cent.csv"))
g_polar = pd.read_csv(filepath_or_buffer=os.path.join(path, r"ts_general_polar.csv"))
g_area = pd.read_csv(filepath_or_buffer=os.path.join(path, r"ts_general_area.csv"))

nnd_only = pd.read_csv(filepath_or_buffer=os.path.join(path, r"ts_nnd_NND.csv"))

tracked = pd.read_csv(filepath_or_buffer=os.path.join(path, r"timeseries_tracked.csv"),
                      sep=",")


# Find percentage overlap
def find_overlap(min_ls, max_ls, check_ls):
    """
    Determine the percentage overlap between to datasets (list1 and list2). For
    every value of df1 that is within the range of df2, add to an initial value
    and then find what percentage that value is of the original (list1)
    """
    value = []
    for i in check_ls:
        if min(min_ls) <= i <= max(max_ls):
            value.append(i)
    percentage = (len(value) / len(check_ls)) * 100
    return percentage


nnd_percent = find_overlap(g_nnd["min"], g_nnd["max"], tracked["nnd"])  # 0
cent_percent = find_overlap(g_cent["min"], g_cent["max"], tracked["cent"])  # 60.606%
polar_percent = find_overlap(g_polar["min"], g_polar["max"], tracked["polar"])  # 39.394
area_percent = find_overlap(g_area["min"], g_area["max"], tracked["area"])  # 0

nnd_only_percent = find_overlap(nnd_only["min"], nnd_only["max"], tracked["nnd"])  # 94.945%
