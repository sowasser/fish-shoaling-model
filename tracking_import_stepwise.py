"""
Data captured from video of fish (sticklebacks or zebrafish) using LoggerPro.
The position of each fish is captured for selected time steps of the video.

In this script, the data are imported and cleaned, then position is extracted
for statistical analyses, similar to the data collectors in the fish shoaling
model. The data structure for this analysis method is completely different than
that in the tracking_import.py script.
"""

import pandas as pd
import os
import math
import numpy as np

# Import second stickleback file. Was accelerated by 500% and data captured
# every 20 steps
path = "/Users/user/Desktop/Local/Mackerel/shoal-model-in-R"
track = pd.read_csv(filepath_or_buffer=os.path.join(path, r"sticklebacks2_500x20.csv"),
                    sep=",")
track = track.drop(track.columns[0], axis=1)  # first column (time) is useless

track.columns = ["x1", "y1", "x2", "y2", "x3", "y3", "x4", "y4", "x5", "y5",
                 "x6", "y6", "x7", "y7", "x8", "y8", "x9", "y9", "x10", "y10",
                 "x11", "y11", "x12", "y12", "x13", "y13", "x14", "y14"]

# Separate list of tuples for each step, remove empty row to prep for analysis
s1 = np.asarray(track[track.columns[0:2]].dropna(axis=0))
s2 = list(track[track.columns[2:4]].dropna(axis=0).itertuples(index=False, name=None))
s3 = list(track[track.columns[4:6]].dropna(axis=0).itertuples(index=False, name=None))
s4 = list(track[track.columns[6:8]].dropna(axis=0).itertuples(index=False, name=None))
s5 = list(track[track.columns[8:10]].dropna(axis=0).itertuples(index=False, name=None))
s6 = list(track[track.columns[10:12]].dropna(axis=0).itertuples(index=False, name=None))
s7 = list(track[track.columns[12:14]].dropna(axis=0).itertuples(index=False, name=None))
s8 = list(track[track.columns[14:16]].dropna(axis=0).itertuples(index=False, name=None))
s9 = list(track[track.columns[16:18]].dropna(axis=0).itertuples(index=False, name=None))
s10 = list(track[track.columns[18:20]].dropna(axis=0).itertuples(index=False, name=None))
s11 = list(track[track.columns[20:22]].dropna(axis=0).itertuples(index=False, name=None))
s12 = list(track[track.columns[22:24]].dropna(axis=0).itertuples(index=False, name=None))
s13 = list(track[track.columns[24:26]].dropna(axis=0).itertuples(index=False, name=None))
s14 = list(track[track.columns[26:28]].dropna(axis=0).itertuples(index=False, name=None))


# Distance from centroid for each frame

def distance(df1, df2):
    """Calculates Euclidean distance between two points."""
    dist = math.sqrt((df2[:, 0] - df1[:, 0])**2 + (df2[:, 1] - df1[:, 1])**2)
    return dist


def centroid(df):
    """Finds the centroid of each frame."""
    pos_x = df[:, 0]
    pos_y = df[:, 1]
    mean_x, mean_y = np.mean(pos_x), np.mean(pos_y)
    cent = (mean_x, mean_y)
    return np.asarray(cent)


def centroid_dist(df):
    """Calculates mean distance of all fish from the centroid for each frame."""
    cent_dist = []
    for i in df:
        pos = df[i, :]  # issue here
        dist = distance(pos, centroid(df))
        cent_dist = np.append(cent_dist, dist)
    return np.mean(cent_dist)


s1_cd = centroid_dist(s1)
