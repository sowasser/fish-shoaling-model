# This script is to visualize the distributions for the

from scipy.stats import gamma
import matplotlib.pyplot as plt
import numpy as np


speed_dist = gamma.rvs(size=1000, a=2)
vision_dist = gamma.rvs(size=1000, a=10)
sep_dist = gamma.rvs(size=1000, a=2)

# speed_dist = np.random.lognormal(mean=0.2, sigma=1, size=100)
# vision_dist = np.random.lognormal(mean=0.10, sigma=1, size=100)
# sep_dist = np.random.lognormal(mean=0.2, sigma=1, size=100)

# Graph distributions
plt.style.use("dark_background")
fig = plt.figure(figsize=(6, 9))

ax1 = fig.add_subplot(3, 1, 1)
plt.title("Speed Distribution")

ax2 = fig.add_subplot(3, 1, 2)
plt.title("Vision Distribution")

ax3 = fig.add_subplot(3, 1, 3)
plt.title("Separation Distribution")


ax1.hist(speed_dist, bins=50)
ax2.hist(vision_dist, bins=50)
ax3.hist(sep_dist, bins=50)

plt.show()


