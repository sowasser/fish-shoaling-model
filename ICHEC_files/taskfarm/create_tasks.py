"""
Script for generating the task list to run the taskfarm on the ICHEC cluster.
The tasks are run based on a .txt file where each run is a task that passes in
a unique value for the the prior that is varying in that script (speed, vision
or separation) and has its own data output.

The distribution I'm using is a Gamma distribution because it needs to be non-
negative. I'm playing around with the parameters, but "a" is what the
distribution is centered around, "loc" is the bottom end of the distribution
(this is set to the default - 0), and "scale" is how far the distribution is
spread.
"""

from scipy.stats import gamma
import numpy as np
import os

runs = 10000  # TODO: Change for number of runs of the model

# Prior distributions - Gamma
speed_dist = gamma.rvs(size=runs, a=2, loc=0, scale=5)
vision_dist = gamma.rvs(size=runs, a=5, loc=0, scale=5)
sep_dist = gamma.rvs(size=runs, a=2, loc=0, scale=5)

# # Prior distributions - Lognormal
# speed_dist = np.random.lognormal(mean=0.2, sigma=1, size=1000)
# vision_dist = np.random.lognormal(mean=1, sigma=1, size=1000)
# sep_dist = np.random.lognormal(mean=2, sigma=1, size=1000)

# Same length as priors; for unique names for the output files
names = range(runs)

# path = "/Users/user/Desktop/Local/Mackerel/fish-shoaling-model/ICHEC_files/taskfarm"  # desktop
path = "/Users/Sophie/Desktop/DO NOT ERASE/1NUIG/Mackerel/fish-shoaling-model/ICHEC_files/taskfarm"  # laptop


# Write files with values from distributions above & unique output names
# TODO: make sure dates are correct
file = open(os.path.join(path, r"modelruns.txt"), "w")

# For when only one parameter varies at a time --------------------------------
# [file.write("python3 ../../ichec_run_speed.py " + str(i)
#             + " > ../output/16Apr2020/speed_output" + str(j)
#             + ".txt \n") for i, j in zip(speed_dist, names)]
#
# [file.write("python3 ../../ichec_run_vision.py " + str(i)
#             + " > ../output/16Apr2020/vision_output" + str(j)
#             + ".txt \n") for i, j in zip(vision_dist, names)]
#
# [file.write("python3 ../../ichec_run_sep.py " + str(i)
#             + " > ../output/16Apr2020/sep_output" + str(j)
#             + ".txt \n") for i, j in zip(sep_dist, names)]

# For varying all parameters --------------------------------------------------
[file.write("python3 ../../ichec_run.py " + str(speed) + " " + str(vis) + " " + str(sep)
            + " > ../output/13May2020/output" + str(i)
            + ".txt \n") for speed, vis, sep, i in zip(speed_dist, vision_dist, sep_dist, names)]

file.close()
