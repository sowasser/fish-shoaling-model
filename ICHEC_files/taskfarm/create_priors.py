"""
This script produces gamma distributions for each of the input parameters
(priors) that will be tested with ABC. These values are then used in the model
calls for ICHEC.
"""

from scipy.stats import gamma
import os

speed_dist = gamma.rvs(size=10000, a=2)
vision_dist = gamma.rvs(size=10000, a=10)
sep_dist = gamma.rvs(size=10000, a=2)


# path = "/Users/user/Desktop/Local/Mackerel/fish-shoaling-model/ICHEC_files/taskfarm"  # desktop
path = "/Users/Sophie/Desktop/DO NOT ERASE/1NUIG/Mackerel/fish-shoaling-model/ICHEC_files/taskfarm"  # laptop

# Write text files with each value of the distribution on its own line
file = open(os.path.join(path, r"speed_priors.txt"), "w")

for i in speed_dist:
    file.write(str(i) + "\n")

file.close()

file = open(os.path.join(path, r"vision_priors.txt"), "w")

for i in vision_dist:
    file.write(str(i) + "\n")

file.close()

file = open(os.path.join(path, r"sep_priors.txt"), "w")

for i in sep_dist:
    file.write(str(i) + "\n")

file.close()
