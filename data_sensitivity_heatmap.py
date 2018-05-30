"""
Code for creating a heatmap of density factors from runs of the shoaling model.
Data is imported from the original data_sensitivity.py file, then animated
heatmaps are created in matplotlib.
"""

# Todo: try to create animated heatmaps for density:
# https://matplotlib.org/examples/images_contours_and_fields/interpolation_methods.html
# https://stackoverflow.com/questions/33742845/seaborn-animate-heatmap-correlation-matrix?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa


from data_sensitivity import data50, data100, data200
import matplotlib.pyplot as plt
from matplotlib import animation
