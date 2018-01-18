"""
This script contains the functions used to collect data on the polarization
and spatial extent of the shoal. These are, currently:
    1. Polarization: a function returning the median absolute deviation of
       agent heading from the mean heading of the group
    2. Nearest neighbour distance: the mean distance of the 5 nearest agents,
       determined using a k-distance tree.
    3. Shoal Area: convex hull
    4. Mean Distance From Centroid

More functions will be added as more methods for conceptualizing the shoal are
found in the literature.

These are used in shoal_model.py and elsewhere.
"""

import numpy as np
import math
from scipy.spatial import KDTree, ConvexHull
from statsmodels.robust.scale import mad


def polar(model):
    """
    Computes median absolute deviation (MAD) from the mean velocity of the
    group. As the value approaches 0, polarization increases.
    To find the MAD, the x,y coordinates are converted to radians by finding
    the arc tangent of y/x. The function used pays attention to the sign of
    the input to make sure that the correct quadrant for the angle is determined.
    """
    velocity_x = [agent.velocity[0] for agent in model.schedule.agents]
    velocity_y = [agent.velocity[1] for agent in model.schedule.agents]
    angle = []
    for (y, x) in zip(velocity_y, velocity_x):
        a = math.atan2(y, x)
        angle.append(a)
    return mad(np.asarray(angle), center=np.median)


def nnd(model):
    """
    Computes the average nearest neighbor distance for each agent as another
    measure of cohesion. Method finds & averages the nearest neighbours
    using a KDTree, a machine learning concept for clustering or
    compartmentalizing data. Right now, the 5 nearest neighbors are considered.
    """
    fish = np.asarray([agent.pos for agent in model.schedule.agents])
    fish_tree = KDTree(fish)
    means = []
    for me in fish:
        neighbors = fish_tree.query(x=me, k=6)  # includes agent @ dist = 0
        dist = list(neighbors[0])  # select dist not neighbor # from .query output
        dist.pop(0)  # removes closest agent - itself @ dist = 0
        means.append(sum(dist) / len(dist))
    return sum(means) / len(means)


def area(model):
    """
    Computes convex hull (smallest convex set that contains all points) as
    measure of shoal area. Uses the area variable from the scipy.spatial
    ConvexHull function.
    """
    # Data needs to be a numpy array of floats - two columns (x,y)
    pos_x = np.asarray([agent.pos[0] for agent in model.schedule.agents])
    pos_y = np.asarray([agent.pos[1] for agent in model.schedule.agents])
    return ConvexHull(np.column_stack((pos_x, pos_y))).area


def centroid_dist(model):
    """
    Extracts xy coordinates for each agent, finds the centroid, and then
    calculates the mean distance of each agent from the centroid.
    """
    pos_x = np.asarray([agent.pos[0] for agent in model.schedule.agents])
    pos_y = np.asarray([agent.pos[1] for agent in model.schedule.agents])
    mean_x = np.mean(pos_x)
    mean_y = np.mean(pos_y)
    centroid = (mean_x, mean_y)
    pos = [agent.pos for agent in model.schedule.agents]
    cent_dist = []
    for p in pos:
        dist = model.space.get_distance(p, centroid)
        cent_dist = np.append(cent_dist, dist)
    return np.mean(cent_dist)