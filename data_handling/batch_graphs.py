"""
Various graphs for the data collected in the data_batch.py script. The means
of the data collectors for the model are calculated two ways:
    1. For each step of the model, averaged over all of the runs
    2. For each run of the model, averaged over all steps.
These can be useful for sensitivity analysis and to accompany future analysis.
"""

from data_handling.data_batch import *
import matplotlib.pyplot as plt


# MEANS FOR EACH STEP OVER ALL RUNS -------------------------------------------
plt.style.use("dark_background")
fig = plt.figure(figsize=(8, 5), dpi=300)
ax1 = plt.subplot(2, 2, 1)
plt.xlabel("Distance from Centroid")
plt.title("Mean Runs")

ax2 = plt.subplot(2, 2, 2)
plt.xlabel("Nearest Neighbour Distance")
plt.title("Mean Runs")

ax3 = plt.subplot(2, 2, 3)
plt.xlabel("Polarization")
plt.title("Mean Runs")

ax4 = plt.subplot(2, 2, 4)
plt.xlabel("Shoal Area")
plt.title("Mean Runs")

ax1.plot(mean_runs["polar"])
ax2.plot(mean_runs["nnd"])
ax3.plot(mean_runs["area"])
ax4.plot(mean_runs["centroid"])

plt.tight_layout()
plt.show()


# MEANS FOR EACH RUN OVER ALL STEPS -------------------------------------------
p_runs = p.mean(axis=1)
n_runs = n.mean(axis=1)
a_runs = a.mean(axis=1)
c_runs = c.mean(axis=1)

plt.style.use("dark_background")
fig2 = plt.figure(figsize=(8, 5), dpi=300)
ax5 = plt.subplot(2, 2, 1)
plt.xlabel("Distance from Centroid")
plt.title("Mean Steps")

ax6 = plt.subplot(2, 2, 2)
plt.xlabel("Nearest Neighbour Distance")
plt.title("Mean Steps")

ax7 = plt.subplot(2, 2, 3)
plt.xlabel("Polarization")
plt.title("Mean Steps")

ax8 = plt.subplot(2, 2, 4)
plt.xlabel("Shoal Area")
plt.title("Mean Steps")

ax5.plot(p_runs)
ax6.plot(n_runs)
ax7.plot(a_runs)
ax8.plot(c_runs)

plt.tight_layout()
plt.show()
