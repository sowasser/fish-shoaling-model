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


# This renames the columns successfully, but in the wrong order. This outputs:
# time, x1, x2, x3..., y1, y2, y3..., x1_v, x2_v, x3_v..., y1_v, y2_v, y3_v...

# rng = range(1, int((len(list(track)) - 1) / 4) + 1)
# new_cols = ["time"] + \
#            ["x" + str(i) for i in rng] + \
#            ["y" + str(i) for i in rng] + \
#            ["x" + str(i) + "_v" for i in rng] + \
#            ["y" + str(i) + "_v" for i in rng]
# track.columns = new_cols
