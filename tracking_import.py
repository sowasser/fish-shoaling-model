"""
Data captured from video of fish (sticklebacks or zebrafish) using LoggerPro.
The position and velocity of each fish is captured for each time step of the
video.

In this script, the data are imported and cleaned, then position is extracted
for statistical analyses, similar to the data collectors in the fish shoaling
model.
"""

import pandas as pd
import os
import math

# Import first stickleback file. Was accelerated by 300%
path = "/Users/user/Desktop/Local/Mackerel/shoal-model-in-R"
track = pd.read_csv(filepath_or_buffer=os.path.join(path, r"sticklebacks1_300x.csv"),
                    sep=",")
# Rename columns. There has to be a better way to do this.
track.columns = ["time", "x1", "y1", "x1_v", "y1_v",
                 "x2", "y2", "x2_v", "y2_v",
                 "x3", "y3", "x3_v", "y3_v",
                 "x4", "y4", "x4_v", "y4_v",
                 "x5", "y5", "x5_v", "y5_v",
                 "x6", "y6", "x6_v", "y6_v",
                 "x7", "y7", "x7_v", "y7_v",
                 "x8", "y8", "x8_v", "y8_v",
                 "x9", "y9", "x9_v", "y9_v",
                 "x10", "y10", "x10_v", "y10_v",
                 "x11", "y11", "x11_v", "y11_v",
                 "x12", "y12", "x12_v", "y12_v",
                 "x13", "y13", "x13_v", "y13_v",
                 "x14", "y14", "x14_v", "y14_v",
                 "x15", "y15", "x15_v", "y15_v",
                 "x16", "y16", "x16_v", "y16_v",
                 "x17", "y17", "x17_v", "y17_v",
                 "x18", "y18", "x18_v", "y18_v",
                 "x19", "y19", "x19_v", "y19_v"]

time = track[track.columns[0]]

# Separate dataframes for position of each fish. There must be a better way
f1p = track[track.columns[1:3]]
f2p = track[track.columns[5:7]]
f3p = track[track.columns[9:11]]
f4p = track[track.columns[13:15]]
f5p = track[track.columns[17:19]]
f6p = track[track.columns[21:23]]
f7p = track[track.columns[25:27]]
f8p = track[track.columns[29:31]]
f9p = track[track.columns[33:35]]
f10p = track[track.columns[37:39]]
f11p = track[track.columns[41:43]]
f12p = track[track.columns[45:47]]
f13p = track[track.columns[49:51]]
f14p = track[track.columns[53:55]]
f15p = track[track.columns[57:59]]
f16p = track[track.columns[61:63]]
f17p = track[track.columns[65:67]]
f18p = track[track.columns[69:71]]
f19p = track[track.columns[73:75]]


def distance(x1, x2, y1, y2):
    """Calculates Euclidean distance between two points"""
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return dist

# having trouble: go to this stack overflow post for next steps:
# https://stackoverflow.com/questions/36609457/run-function-exactly-once-for-each-row-in-a-pandas-dataframe

# pos_y = track[track.columns[2::4]]
# pos_x = track[track.columns[1::4]]
# mean_y = pos_y.mean(axis=1)
# mean_x = pos_x.mean(axis=1)


# This renames the columns successfully, but in the wrong order. This outputs:
# time, x1, x2, x3..., y1, y2, y3..., x1_v, x2_v, x3_v..., y1_v, y2_v, y3_v...

# rng = range(1, int((len(list(track)) - 1) / 4) + 1)
# new_cols = ["time"] + \
#            ["x" + str(i) for i in rng] + \
#            ["y" + str(i) for i in rng] + \
#            ["x" + str(i) + "_v" for i in rng] + \
#            ["y" + str(i) + "_v" for i in rng]
# track.columns = new_cols
