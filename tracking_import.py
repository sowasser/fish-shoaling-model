"""
Data captured from video of fish (sticklebacks or zebrafish) using LoggerPro.
The position and velocity of each fish is captured for each time step of the
video.

In this script, the data are imported and cleaned, then position is extracted
for statistical analyses, similar to the data collectors in the fish shoaling
model.
"""

import pandas as pd
import numpy as np
import os


# Import first stickleback file. Was accelerated by 300%
path = "/Users/user/Desktop/Local/Mackerel/shoal-model-in-R"
track = pd.read_csv(filepath_or_buffer=os.path.join(path, r"sticklebacks1_300x.csv"),
                    sep=",")

# Column names: x1, y1, x1_v, y1_v, x2, y2, x2_v, y2_v, etc.
# Separate out 1st (time) column
time = track[track.columns[0]]
track = track.drop(track.columns[0], axis=1)

nums = range(1, 20)  # End is #+1. CHANGE THIS FOR DIFFERENT DATA SOURCES
list_x = ["x" + str(n) for n in nums]
list_y = ["y" + str(n) for n in nums]
list_xv = ["x" + str(n) + "_v" for n in nums]
list_yv = ["y" + str(n) + "_v" for n in nums]

# iterate between lists and assign as column names
track.columns = [item for sublist in zip(list_x, list_y, list_xv, list_yv)
                 for item in sublist]

# Separate dataframes for position of each fish.
f1p = np.asarray(track[track.columns[0:2]])
f2p = np.asarray(track[track.columns[4:6]])
f3p = track[track.columns[8:10]]
f4p = track[track.columns[12:14]]
f5p = track[track.columns[16:18]]
f6p = track[track.columns[20:22]]
f7p = track[track.columns[24:26]]
f8p = track[track.columns[28:30]]
f9p = track[track.columns[32:34]]
f10p = track[track.columns[36:38]]
f11p = track[track.columns[40:42]]
f12p = track[track.columns[44:46]]
f13p = track[track.columns[48:50]]
f14p = track[track.columns[52:54]]
f15p = track[track.columns[56:58]]
f16p = track[track.columns[60:62]]
f17p = track[track.columns[64:66]]
f18p = track[track.columns[68:70]]
f19p = track[track.columns[72:74]]

pair1 = np.column_stack((f1p, f2p))


def mean_distance(pair):
    """Calculates mean distance between agents per time step"""

    def distance(df):
        """Calculates Euclidean distance between two points"""
        # Todo: fix this function!
        df1 = df[:, [0, 1]]
        df2 = df[:, [2, 3]]
        dist = np.linalg.norm(df1 - df2)
        return dist

    return np.mean(np.apply_along_axis(distance, axis=1, arr=pair))


md = mean_distance(pair1)
