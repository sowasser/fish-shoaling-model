# This script is to visualize the distributions for the

from scipy.stats import gamma
import matplotlib.pyplot as plt
import numpy as np


# speed_dist = np.random.lognormal(mean=2, sigma=1, size=10000)
# vision_dist = np.random.lognormal(mean=10, sigma=1, size=10000)
# sep_dist = np.random.lognormal(mean=2, sigma=1, size=10000)

speed_dist = gamma.rvs(size=10000, a=2, loc=0, scale=5)
vision_dist = gamma.rvs(size=10000, a=5, loc=0, scale=5)
sep_dist = gamma.rvs(size=10000, a=2, loc=0, scale=5)


# Graph distributions
plt.style.use("dark_background")
fig = plt.figure(figsize=(6, 9))

ax1 = fig.add_subplot(3, 1, 1)
plt.title("speed")
#
ax2 = fig.add_subplot(3, 1, 2)
plt.title("vision")

ax3 = fig.add_subplot(3, 1, 3)
plt.title("separation")

ax1.hist(speed_dist, bins=50)
ax2.hist(vision_dist, bins=50)
ax3.hist(sep_dist, bins=50)

plt.show()


