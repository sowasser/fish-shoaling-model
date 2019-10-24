from scipy.stats import gamma
import matplotlib.pyplot as plt


speed_dist = gamma.rvs(size=10, a=2)
vision_dist = gamma.rvs(size=10, a=10)
sep_dist = gamma.rvs(size=10, a=2)


# Graph distributions
plt.style.use("dark_background")
fig = plt.figure(figsize=(6, 6))

ax1 = fig.add_subplot(3, 1, 1)
plt.title("Speed Distribution")

ax2 = fig.add_subplot(3, 1, 2)
plt.title("Vision Distribution")

ax3 = fig.add_subplot(3, 1, 3)
plt.title("Separation Distribution")


ax1.plot.hist(speed_dist)
ax2.plot.hist(vision_dist)
ax3.plot.hist(sep_dist)

plt.show()


