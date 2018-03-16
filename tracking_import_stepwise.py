"""
Data captured from video of fish (sticklebacks or zebrafish) using LoggerPro.
The position of each fish is captured for selected frames of the video.

In this script, the data are imported and cleaned, then position is extracted
for statistical analyses. The data structure for this analysis method is
completely different than that in the tracking_import.py script. The results
are then graphed using matplotlib.

These functions are for statistical analysis of the data, similar to the data
collectors in the fish shoaling model. They are:
    * Mean distance from the centroid
    * Mean nearest neighbour distance
    * Shoal area (area of the convex hull)
    * Polarization - can be included for tracking data with 2 points per fish

Shoal area will likely not be very useful, as the fish tend to stay at the
boarders of the tub they're in. Polarization can be included for tracking data
with 2 points per fish per frame.
"""

# Todo: Code data import to make it work automatically for different datasets

import pandas as pd
import numpy as np
import os
from scipy.spatial import KDTree, ConvexHull
import math
from statsmodels.robust.scale import mad
import matplotlib.pyplot as plt


path = "/Users/user/Desktop/Local/Mackerel/shoal-model-in-R"
track = pd.read_csv(filepath_or_buffer=os.path.join(path, r"sticklebacks1_300xstepwise.csv"),
                    sep=",")
track = track.drop(track.columns[0], axis=1)  # first column (time) is useless

# Column names: x1, y1, x2, y2, etc.
# Todo: CHANGE NUMS RANGE FOR DIFFERENT DATA SOURCES
nums = range(1, 22)  # End is #+1
list_x = ["x" + str(n) for n in nums]
list_y = ["y" + str(n) for n in nums]

# iterate between lists and assign as column names
track.columns = [item for sublist in zip(list_x, list_y) for item in sublist]

# List of arrays for each step of the video. Remove empty rows.
# Todo: CHANGE RANGE FOR DIFFERENT DATA SOURCES

# steps = []
# for start, stop in list(range(0, 41, 2)), list(range(2, 43, 2)):
#     steps += track[track.columns[start:stop]].dropna(axis=0)

# steps = [track[track.columns[start:stop]].dropna(axis=0) for start, stop in list(range(0, 41, 2))]

steps = [np.asarray(track[track.columns[0:2]].dropna(axis=0)),
         np.asarray(track[track.columns[2:4]].dropna(axis=0)),
         np.asarray(track[track.columns[4:6]].dropna(axis=0)),
         np.asarray(track[track.columns[6:8]].dropna(axis=0)),
         np.asarray(track[track.columns[8:10]].dropna(axis=0)),
         np.asarray(track[track.columns[10:12]].dropna(axis=0)),
         np.asarray(track[track.columns[12:14]].dropna(axis=0)),
         np.asarray(track[track.columns[14:16]].dropna(axis=0)),
         np.asarray(track[track.columns[16:18]].dropna(axis=0)),
         np.asarray(track[track.columns[18:20]].dropna(axis=0)),
         np.asarray(track[track.columns[20:22]].dropna(axis=0)),
         np.asarray(track[track.columns[22:24]].dropna(axis=0)),
         np.asarray(track[track.columns[24:26]].dropna(axis=0)),
         np.asarray(track[track.columns[26:28]].dropna(axis=0)),
         np.asarray(track[track.columns[28:30]].dropna(axis=0)),
         np.asarray(track[track.columns[30:32]].dropna(axis=0)),
         np.asarray(track[track.columns[32:34]].dropna(axis=0)),
         np.asarray(track[track.columns[34:36]].dropna(axis=0)),
         np.asarray(track[track.columns[36:38]].dropna(axis=0)),
         np.asarray(track[track.columns[38:40]].dropna(axis=0)),
         np.asarray(track[track.columns[40:42]].dropna(axis=0))]


# Mean Distance from Centroid
def centroid_dist(df):
    """
    Finds the centroid of each frame and then calculates mean distance of
    objects from the centroid.
    """
    pos_x = df[:, 0]
    pos_y = df[:, 1]
    cent = np.asarray(np.mean(pos_x), np.mean(pos_y))

    def distance(array):
        """Euclidean distance between object and centroid."""
        dist = np.linalg.norm(array - cent)
        return dist

    cent_dist = np.mean(np.apply_along_axis(distance, axis=1, arr=df))
    return np.mean(cent_dist)


centroid_distance = pd.DataFrame([centroid_dist(s) for s in steps])
centroid_distance.to_csv(os.path.join(path, r"track_cent_dist.csv"))


# Nearest Neighbour Distance
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


nn_distance = pd.DataFrame([nnd(s) for s in steps])
nn_distance.to_csv(os.path.join(path, r"track_nnd.csv"))


# Shoal Area
def area(df):
    """
    Computes convex hull (smallest convex set that contains all points) as a
    measure of shoal area. Uses the area variable from the scipy.spatial
    ConvexHull function, which requires a numpy array of tuples as input.
    """
    position = np.column_stack((np.asarray(df[:, 0]), np.asarray(df[:, 1])))
    return ConvexHull(position).area


shoal_area = pd.DataFrame([area(s) for s in steps])
shoal_area.to_csv(os.path.join(path, r"track_shoal_area.csv"))


# Polarization
def polar(df):
    """
    Computes median absolute deviation (MAD) from the mean heading of the group
    as a measure of polarization by calculating the angle (in radians) of the
    line between points at the front & back of each fish, then the MAD.
    """
    # Separate out points for front & back of the fish
    x_front = np.ndarray.tolist(df[::2, 0])
    y_front = np.ndarray.tolist(df[::2, 1])
    x_back = np.ndarray.tolist(df[1::2, 0])
    y_back = np.ndarray.tolist(df[1::2, 1])

    # Calculate difference, angle of line, return MAD
    x_diff = [xb - xf for xb, xf in zip(x_back, x_front)]
    y_diff = [yb - yf for yb, yf in zip(y_back, y_front)]
    angles = [math.atan2(y, x) for y, x in zip(y_diff, x_diff)]
    return mad(np.asarray(angles), center=np.median)


polarization = pd.DataFrame([polar(s) for s in steps])
polarization.to_csv(os.path.join(path, r"track_polar.csv"))


###############################################################################

# Plot Styles
plt.style.use("dark_background")
# plt.style.use("ggplot")
# plt.style.use("seaborn-dark")
# plt.style.use("Solarize_Light2")

# Create multiplot
fig = plt.figure(figsize=(8, 6), dpi=300)

ax1 = plt.subplot(221)
plt.title("Mean Distance from Centroid")
plt.ylabel("distance (mm)")

ax2 = plt.subplot(222)
plt.title("Mean Nearest Neighbour Distance")
plt.ylabel("distance (mm)")

ax3 = plt.subplot(223)
plt.title("Shoal Area")
plt.ylabel("area (mm2)")

ax4 = plt.subplot(224)
plt.title("Polarization")
plt.ylabel("Mean Absolute Deviation")

ax1.plot(centroid_distance)
ax2.plot(nn_distance)
ax3.plot(shoal_area)
ax4.plot(polarization)

plt.tight_layout()

plt.show()

plot_path = "/Users/user/Desktop/Local/Mackerel/Figures"
fig.savefig(os.path.join(plot_path, r"sticklebacks1_300xstepwise.png"))
