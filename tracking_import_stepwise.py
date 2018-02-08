"""
Data captured from video of fish (sticklebacks or zebrafish) using LoggerPro.
The position of each fish is captured for selected frames of the video.

In this script, the data are imported and cleaned, then position is extracted
for statistical analyses. The data structure for this analysis method is
completely different than that in the tracking_import.py script. The results
can then be exported to R for graphing if you're a ggplot fan, or eventually
you (and by you I mean I) can figure out how to make graphs in Python. :þ

The functions for the statistical analyses are in the tracking_functions.py
script and are as follows:
    * Mean distance from the centroid
    * Mean nearest neighbour distance
    * Shoal area (area of the convex hull)
    * Polarization - can be included for tracking data with 2 points per fish
"""

# Todo: Code data import to make it work automatically for different datasets

import pandas as pd
import os
from tracking_functions import *


path = "/Users/user/Desktop/Local/Mackerel/shoal-model-in-R"
track = pd.read_csv(filepath_or_buffer=os.path.join(path, r"sticklebacks2_500x20.csv"),
                    sep=",")
track = track.drop(track.columns[0], axis=1)  # first column (time) is useless

# Column names: x1, y1, x2, y2, etc.
nums = range(1, 15)  # End is #+1. CHANGE THIS FOR DIFFERENT DATA SOURCES
list_x = ["x" + str(n) for n in nums]
list_y = ["y" + str(n) for n in nums]

# iterate between lists and assign as column names
track.columns = [item for sublist in zip(list_x, list_y) for item in sublist]

# Separate arrays of object position per frame & remove empty rows.
s1 = np.asarray(track[track.columns[0:2]].dropna(axis=0))
s2 = np.asarray(track[track.columns[2:4]].dropna(axis=0))
s3 = np.asarray(track[track.columns[4:6]].dropna(axis=0))
s4 = np.asarray(track[track.columns[6:8]].dropna(axis=0))
s5 = np.asarray(track[track.columns[8:10]].dropna(axis=0))
s6 = np.asarray(track[track.columns[10:12]].dropna(axis=0))
s7 = np.asarray(track[track.columns[12:14]].dropna(axis=0))
s8 = np.asarray(track[track.columns[14:16]].dropna(axis=0))
s9 = np.asarray(track[track.columns[16:18]].dropna(axis=0))
s10 = np.asarray(track[track.columns[18:20]].dropna(axis=0))
s11 = np.asarray(track[track.columns[20:22]].dropna(axis=0))
s12 = np.asarray(track[track.columns[22:24]].dropna(axis=0))
s13 = np.asarray(track[track.columns[24:26]].dropna(axis=0))
s14 = np.asarray(track[track.columns[26:28]].dropna(axis=0))
# s15 = np.asarray(track[track.columns[28:30]].dropna(axis=0))
# s16 = np.asarray(track[track.columns[30:32]].dropna(axis=0))
# s17 = np.asarray(track[track.columns[32:34]].dropna(axis=0))
# s18 = np.asarray(track[track.columns[34:36]].dropna(axis=0))
# s19 = np.asarray(track[track.columns[36:38]].dropna(axis=0))
# s20 = np.asarray(track[track.columns[38:40]].dropna(axis=0))
# s21 = np.asarray(track[track.columns[40:42]].dropna(axis=0))

# Combine for iterating into final dataframes
steps = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14]
# s15, s16, s17, s18, s19, s20, s21


# Mean Distance from Centroid
centroid_distance = [centroid_dist(s) for s in steps]


# Nearest Neighbour Distance
nn_distance = [nnd(s) for s in steps]


# Shoal Area
shoal_area = [area(s) for s in steps]


# Polarization
# polarization = [polar(s) for s in steps]
