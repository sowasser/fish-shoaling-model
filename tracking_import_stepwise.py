"""
Data captured from video of fish (sticklebacks or zebrafish) using LoggerPro.
The position of each fish is captured for selected frames of the video.

In this script, the data are imported and cleaned, then position is extracted
for statistical analyses. The data structure for this analysis method is
completely different than that in the tracking_import.py script.

The functions for the statistical analyses are in the tracking_functions.py
script and are as follows:
    * Mean distance from the centroid
    * Mean nearest neighbour distance
    * Shoal area (area of the convex hull)
    * Polarization - can be included for tracking data with 2 points per fish
"""

# Todo: Make data import and final dataframe creation for each statistic more universal

import pandas as pd
import os
from tracking_functions import *


path = "/Users/user/Desktop/Local/Mackerel/shoal-model-in-R"
track = pd.read_csv(filepath_or_buffer=os.path.join(path, r"sticklebacks2_500x20.csv"),
                    sep=",")
track = track.drop(track.columns[0], axis=1)  # first column (time) is useless

track.columns = ["x1", "y1", "x2", "y2", "x3", "y3", "x4", "y4", "x5", "y5",
                 "x6", "y6", "x7", "y7", "x8", "y8", "x9", "y9", "x10", "y10",
                 "x11", "y11", "x12", "y12", "x13", "y13", "x14", "y14"]
# "x15", "y15", "x16", "y16", "x17", "y17", "x18", "y18", "x19",
# "y19", "x20", "y20", "x22", "y22"]

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


###############################
# Mean Distance from Centroid #
###############################

centroid_distance = [centroid_dist(s1), centroid_dist(s2), centroid_dist(s3),
                     centroid_dist(s4), centroid_dist(s5), centroid_dist(s6),
                     centroid_dist(s7), centroid_dist(s8), centroid_dist(s9),
                     centroid_dist(s10), centroid_dist(s11), centroid_dist(s12),
                     centroid_dist(s13), centroid_dist(s14)]
# centroid_dist(s15), centroid_dist(s16), centroid_dist(s17),
# centroid_dist(s18), centroid_dist(s19), centroid_dist(s20),
# centroid_dist(s21)]


##############################
# Nearest Neighbour Distance #
##############################

nn_distance = [nnd(s1), nnd(s2), nnd(s3), nnd(s4), nnd(s5), nnd(s6), nnd(s7),
               nnd(s8), nnd(s9), nnd(s10), nnd(s11), nnd(s12), nnd(s13),
               nnd(s14)]
# nnd(s15), nnd(s16), nnd(s17), nnd(s18), nnd(s19), nnd(s20), nnd(s21)]


##############
# Shoal Area #
##############

shoal_area = [area(s1), area(s2), area(s3), area(s4), area(s5), area(s6),
              area(s7), area(s8), area(s9), area(s10), area(s11), area(s12),
              area(s13), area(s14)]
# area(s15), area(s16), area(s17), area(s18), area(s19), area(s20), area(s21)]


################
# Polarization #
################

# polarization = [polar(s1), polar(s2), polar(s3), polar(s4), polar(s5),
#                 polar(s6), polar(s7), polar(s8), polar(s9), polar(s10),
#                 polar(s11), polar(s12), polar(s13), polar(s14), polar(s15),
#                 polar(s16), polar(s17), polar(s18), polar(s19), polar(s20),
#                 polar(s21)]
