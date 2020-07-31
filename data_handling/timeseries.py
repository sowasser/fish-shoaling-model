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

test1 = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
test2 = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3]


# Find percentage overlap
def find_overlap(list1, list2):
    """
    Determine the percentage overlap between to datasets (list1 and list2). For
    every value of df1 that is within the range of df2, add to an initial value
    and then find what percentage that value is of the original (list1)
    """
    value = []
    for i in list1:
        if i in np.arange(min(list2), max(list2), 0.1):
            value.append(i)
    percentage = len(value) / len(list1)
    return percentage


test = find_overlap(test1, test2)

# polar_percentage = find_overlap(modelled["polar"], tracked["polar"])
