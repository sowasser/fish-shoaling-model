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

runs = 1000  # TODO: Change for number of runs of the model

# Prior distributions - other factors
# speed_dist = gamma.rvs(size=runs, a=2, loc=0, scale=1)
# vision_dist = gamma.rvs(size=runs, a=5, loc=0, scale=1)
# sep_dist = gamma.rvs(size=runs, a=2, loc=0, scale=1)

speed_dist = [2] * runs
vision_dist = [5] * runs
sep_dist = [2] * runs

# speed_dist = np.random.uniform(low=0, high=10, size=runs)
# vision_dist = np.random.uniform(low=0, high=10, size=runs)
# sep_dist = np.random.uniform(low=0, high=10, size=runs)

# Prior distributions - boid factors
# cohere_dist = np.random.uniform(low=0, high=1, size=runs)
# separate_dist = np.random.uniform(low=0, high=1, size=runs)
# match_dist = np.random.uniform(low=0, high=1, size=runs)

cohere_dist = [0.2] * runs
separate_dist = [0.2] * runs
match_dist = [0.5] * runs


# Same length as priors; for unique names for the output files
names = range(runs)

# path = "/Users/user/Desktop/Local/Mackerel/fish-shoaling-model/ICHEC_files/taskfarm"  # desktop
path = "/Users/Sophie/Desktop/DO NOT ERASE/1NUIG/Mackerel/fish-shoaling-model/ICHEC_files/taskfarm"  # laptop


# Write files with values from distributions above & unique output names
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

# TODO: Choose which set of parameters to vary
# 1. For varying cohere, separate, dist ---------------------------------------
# [file.write("python3 ../../ichec_run_boidfactors.py " + str(c) + " " + str(s) + " " + str(m)
#             + " > ../output/29May2020/output" + str(n)  # TODO: make sure date is correct
#             + ".txt \n") for c, s, m, n in zip(cohere_dist, separate_dist, match_dist, names)]

# 2. For varying speed, vision, separation ------------------------------------
# [file.write("python3 ../../ichec_run_otherfactors.py " + str(speed) + " " + str(vis) + " " + str(sep)
#             + " > ../output/01Jun2020/output" + str(n)  # TODO: make sure date is correct
#             + ".txt \n") for speed, vis, sep, n in zip(speed_dist, vision_dist, sep_dist, names)]

# 3. For varying all parameters -----------------------------------------------
[file.write("python3 ../../ichec_run_allfactors.py " + str(speed) + " " + str(vis) + " " + str(sep)
            + " " + str(c) + " " + str(s) + " " + str(m)
            + " > ../output/02Jun2020/output" + str(n)  # TODO: make sure date is correct
            + ".txt \n") for speed, vis, sep, c, s, m, n in zip(speed_dist, vision_dist, sep_dist,
                                                                cohere_dist, separate_dist, match_dist, names)]

file.close()
