# This script is to visualize the distributions for the

from scipy.stats import gamma
import matplotlib.pyplot as plt
import numpy as np


# speed_dist = np.random.lognormal(mean=2, sigma=1, size=10000)
# vision_dist = np.random.lognormal(mean=10, sigma=1, size=10000)
# sep_dist = np.random.lognormal(mean=2, sigma=1, size=10000)

# cohere_dist = [i for i in np.random.normal(loc=0.2, scale=0.2, size=1000) if i > 0]
# separate_dist = [i for i in np.random.normal(loc=0.1, scale=0.2, size=1000) if i > 0]
# match_dist = [i for i in np.random.normal(loc=0.4, scale=0.2, size=1000) if i > 0]

# cohere_dist = gamma.rvs(size=100, a=0.2, scale=.1)
# separate_dist = gamma.rvs(size=100, a=0.02, scale=.1)
# match_dist = gamma.rvs(size=100, a=0.4, scale=.1)

cohere_dist = np.random.uniform(0, 1, 100)
separate_dist = np.random.uniform(0, 1, 100)
match_dist = np.random.uniform(0, 1, 100)

# Graph distributions
plt.style.use("dark_background")
fig = plt.figure(figsize=(6, 9))

ax1 = fig.add_subplot(3, 1, 1)
plt.title("cohere")
#
ax2 = fig.add_subplot(3, 1, 2)
plt.title("separate")

ax3 = fig.add_subplot(3, 1, 3)
plt.title("match")

ax1.hist(cohere_dist, bins=100)
ax2.hist(separate_dist, bins=100)
ax3.hist(match_dist, bins=100)

plt.show()


