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

# Import second stickleback file. Was accelerated by 500% and data captured
# every 20 steps
path = "/Users/user/Desktop/Local/Mackerel/shoal-model-in-R"
track = pd.read_csv(filepath_or_buffer=os.path.join(path, r"sticklebacks2_500x20.csv"),
                    sep=",")
track = track.drop(track.columns[0], axis=1)  # first column (time) is useless

track.columns = ["x1", "y1", "x2", "y2", "x3", "y3", "x4", "y4", "x5", "y5",
                 "x6", "y6", "x7", "y7", "x8", "y8", "x9", "y9", "x10", "y10",
                 "x11", "y11", "x12", "y12", "x13", "y13", "x14", "y14"]

# Separate into dataframes for each step and remove empty row to prep for analysis
s1 = track[track.columns[0:2]].dropna(axis=0)
s2 = track[track.columns[2:4]].dropna(axis=0)
s3 = track[track.columns[4:6]].dropna(axis=0)
s4 = track[track.columns[6:8]].dropna(axis=0)
s5 = track[track.columns[8:10]].dropna(axis=0)
s6 = track[track.columns[10:12]].dropna(axis=0)
s7 = track[track.columns[12:14]].dropna(axis=0)
s8 = track[track.columns[14:16]].dropna(axis=0)
s9 = track[track.columns[16:18]].dropna(axis=0)
s10 = track[track.columns[18:20]].dropna(axis=0)
s11 = track[track.columns[20:22]].dropna(axis=0)
s12 = track[track.columns[22:24]].dropna(axis=0)
s13 = track[track.columns[24:26]].dropna(axis=0)
s14 = track[track.columns[26:28]].dropna(axis=0)
