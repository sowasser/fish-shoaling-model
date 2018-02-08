"""
Functions for working with the data captured from video of fish using LoggerPro.
The position of each fish is captured for selected frames of the video.

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

# Todo: Code polarization function

import numpy as np
from scipy.spatial import KDTree, ConvexHull


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


def area(df):
    """
    Computes convex hull (smallest convex set that contains all points) as a
    measure of shoal area. Uses the area variable from the scipy.spatial
    ConvexHull function, which requires a numpy array of tuples as input.
    """
    position = np.column_stack((np.asarray(df[:, 0]), np.asarray(df[:, 1])))
    return ConvexHull(position).area


def polar(df):
    """
    Computes median absolute deviation (MAD) from the mean heading of the group
    as a measure of polarization.
    """
