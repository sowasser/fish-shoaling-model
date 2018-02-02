"""
Data captured from video of fish (sticklebacks or zebrafish) using LoggerPro.
The position of each fish is captured for selected frames of the video.

In this script, the data are imported and cleaned, then position is extracted
for statistical analyses, similar to the data collectors in the fish shoaling
model. The data structure for this analysis method is completely different than
that in the tracking_import.py script.

Statistics performed:
    * Mean distance from the centroid
"""

import pandas as pd
import os
import numpy as np
from scipy.spatial import KDTree

# Import second stickleback file. Was accelerated by 500% and data captured
# every 20 steps
path = "/Users/user/Desktop/Local/Mackerel/shoal-model-in-R"
track = pd.read_csv(filepath_or_buffer=os.path.join(path, r"sticklebacks2_500x20.csv"),
                    sep=",")
track = track.drop(track.columns[0], axis=1)  # first column (time) is useless

track.columns = ["x1", "y1", "x2", "y2", "x3", "y3", "x4", "y4", "x5", "y5",
                 "x6", "y6", "x7", "y7", "x8", "y8", "x9", "y9", "x10", "y10",
                 "x11", "y11", "x12", "y12", "x13", "y13", "x14", "y14"]

# Separate arrays of object position per frame. Removed empty rows.
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


###############################
# Mean distance from centroid #
###############################

def centroid_dist(df):
    """
    Finds the centroid of each frame and then calculates mean distance of
    objects from the centroid.
    """
    pos_x = df[:, 0]
    pos_y = df[:, 1]
    mean_x, mean_y = np.mean(pos_x), np.mean(pos_y)
    cent = np.asarray(mean_x, mean_y)

    def distance(array):
        """Euclidean distance between object and centroid."""
        dist = np.linalg.norm(array - cent)
        return dist

    cent_dist = np.apply_along_axis(distance, axis=1, arr=df)
    return np.mean(cent_dist)


centroid_distance = [centroid_dist(s1), centroid_dist(s2), centroid_dist(s3),
                     centroid_dist(s4), centroid_dist(s5), centroid_dist(s6),
                     centroid_dist(s7), centroid_dist(s8), centroid_dist(s9),
                     centroid_dist(s10), centroid_dist(s11), centroid_dist(s12),
                     centroid_dist(s13), centroid_dist(s14)]


##############################
# Nearest Neighbour Distance #
##############################

def nnd(df):
    """
    Computes the average nearest neighbour distance for each object. Finds &
    averages nearest neighbours using a KDTree, a machine learning concept for
    clustering or compartmentalizing data. Can control how many neighbours are
    considered 'near'.
    """
    fish_tree = KDTree(df)
    means = []
    for me in df:
        neighbors = fish_tree.query(x=me, k=6)  # includes agent @ dist = 0
        dist = list(neighbors[0])  # select dist from .query output
        dist.pop(0)  # removes closest agent - itself @ dist = 0
        means.append(sum(dist) / len(dist))
    return sum(means) / len(means)


nn_distance = [nnd(s1), nnd(s2), nnd(s3), nnd(s4), nnd(s5), nnd(s6), nnd(s7),
               nnd(s8), nnd(s9), nnd(s10), nnd(s11), nnd(s12), nnd(s13), nnd(s14)]
