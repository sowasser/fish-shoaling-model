"""
This script produces gamma distributions for each of the input parameters
(priors) that will be tested with ABC. These values are then used in the model
calls for ICHEC.
"""

from scipy.stats import gamma

speed_dist = gamma.rvs(size=90000, a=2)
vision_dist = gamma.rvs(size=90000, a=10)
sep_dist = gamma.rvs(size=90000, a=2)

# TODO: figure out best file type to write these distributions to.
