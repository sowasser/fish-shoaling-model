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
# Todo: Code polarization function

import pandas as pd
import numpy as np
import os
from scipy.spatial import KDTree, ConvexHull
from statsmodels.robust.scale import mad
import matplotlib.pyplot as plt


path = "/Users/user/Desktop/Local/Mackerel/shoal-model-in-R"
track = pd.read_csv(filepath_or_buffer=os.path.join(path, r"sticklebacks1_300xstepwise.csv"),
                    sep=",")
track = track.drop(track.columns[0], axis=1)  # first column (time) is useless

# Column names: x1, y1, x2, y2, etc.
nums = range(1, 22)  # End is #+1. CHANGE THIS FOR DIFFERENT DATA SOURCES
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
s15 = np.asarray(track[track.columns[28:30]].dropna(axis=0))
s16 = np.asarray(track[track.columns[30:32]].dropna(axis=0))
s17 = np.asarray(track[track.columns[32:34]].dropna(axis=0))
s18 = np.asarray(track[track.columns[34:36]].dropna(axis=0))
s19 = np.asarray(track[track.columns[36:38]].dropna(axis=0))
s20 = np.asarray(track[track.columns[38:40]].dropna(axis=0))
s21 = np.asarray(track[track.columns[40:42]].dropna(axis=0))


# Combine for iterating into final dataframes
steps = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16,
         s17, s18, s19, s20, s21]


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
# Separate into arrays for front point and back point
# s1_2 = [s1[::2], s1[1::2]]
# s2_2 = [s2[::2], s2[1::2]]
# s3_2 = [s3[::2], s3[1::2]]
# s4_2 = [s4[::2], s4[1::2]]
# s5_2 = [s5[::2], s5[1::2]]
# s6_2 = [s6[::2], s6[1::2]]
# s7_2 = [s7[::2], s7[1::2]]
# s8_2 = [s8[::2], s8[1::2]]
# s9_2 = [s9[::2], s9[1::2]]
# s10_2 = [s10[::2], s10[1::2]]
# s11_2 = [s11[::2], s11[1::2]]
# s12_2 = [s12[::2], s12[1::2]]
# s13_2 = [s13[::2], s13[1::2]]
# s14_2 = [s14[::2], s14[1::2]]
# s15_2 = [s15[::2], s15[1::2]]
# s16_2 = [s16[::2], s16[1::2]]
# s17_2 = [s17[::2], s17[1::2]]
# s18_2 = [s18[::2], s18[1::2]]
# s19_2 = [s19[::2], s19[1::2]]
# s20_2 = [s20[::2], s20[1::2]]
# s21_2 = [s21[::2], s21[1::2]]


def polar(df):
    """
    Computes median absolute deviation (MAD) from the mean heading of the group
    as a measure of polarization by calculating the counterclockwise angle (in
    radians) between the two points and then calculating the MAD for the step.
    """

    def angle_between(array):
        array1, array2 = array[::2], array[::2]
        angle1 = np.arctan2(*array1[::-1])
        angle2 = np.arctan2(*array2[::-1])
        return np.rad2deg((angle1 - angle2) % (2 * np.pi))

    angles = np.apply_along_axis(angle_between(df), axis=1, arr=df)
    return mad(np.asarray(angles), center=np.median)


polarization = pd.DataFrame([polar(s) for s in steps])
# polarization.to_csv(os.path.join(path, r"track_polar.csv"))


###############################################################################

# Plot Styles
plt.style.use("dark_background")
# plt.style.use("ggplot")
# plt.style.use("seaborn-dark")
# plt.style.use("Solarize_Light2")

# Create multiplot
fig = plt.figure(figsize=(6, 9), dpi=300)

ax1 = plt.subplot(311)
plt.title("Mean Distance from Centroid")
plt.ylabel("distance (mm)")

ax2 = plt.subplot(312)
plt.title("Mean Nearest Neighbour Distance")
plt.ylabel("distance (mm)")

ax3 = plt.subplot(313)
plt.title("Shoal Area")
plt.ylabel("area (mm2)")

ax1.plot(centroid_distance)
ax2.plot(nn_distance)
ax3.plot(shoal_area)

ax1.get_shared_x_axes().join(ax1, ax2, ax3)
plt.xlabel("step")
plt.tight_layout()

plt.show()

plot_path = "/Users/user/Desktop/Local/Mackerel/Figures"
fig.savefig(os.path.join(plot_path, r"tracking.png"))
