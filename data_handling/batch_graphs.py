"""
Various graphs for the data collected in the data_batch.py script. The means
of the data collectors for the model are calculated two ways:
    1. For each step of the model, averaged over all of the runs
    2. For each run of the model, averaged over all steps.
These can be useful for sensitivity analysis and to accompany future analysis.
"""

from data_handling.data_batch import *
import matplotlib.pyplot as plt

# TODO: figure out why both sets of graphs are showing up the same

# MEANS FOR EACH STEP OVER ALL RUNS -------------------------------------------
plt.style.use("dark_background")
fig = plt.figure(figsize=(8, 11), dpi=300)
ax1 = plt.subplot(4, 2, 1)
plt.ylabel("Polarization")
plt.xlabel("step")

ax2 = plt.subplot(4, 2, 3)
plt.ylabel("Nearest Neighbour Distance")
plt.xlabel("step")

ax3 = plt.subplot(4, 2, 5)
plt.ylabel("Shoal Area")
plt.xlabel("step")

ax4 = plt.subplot(4, 2, 7)
plt.ylabel("Distance from Centroid")
plt.xlabel("step")

ax1.plot(mean_runs["polar"])
ax2.plot(mean_runs["nnd"])
ax3.plot(mean_runs["area"])
ax4.plot(mean_runs["centroid"])


# MEANS FOR EACH RUN OVER ALL STEPS -------------------------------------------
ax5 = plt.subplot(4, 2, 2)
plt.ylabel("Polarization")
plt.xlabel("run")

ax6 = plt.subplot(4, 2, 4)
plt.ylabel("Nearest Neighbour Distance")
plt.xlabel("run")

ax7 = plt.subplot(4, 2, 6)
plt.ylabel("Shoal Area")
plt.xlabel("run")

ax8 = plt.subplot(4, 2, 8)
plt.ylabel("Distance from Centroid")
plt.xlabel("run")

ax5.plot(mean_steps["polar"])
ax6.plot(mean_steps["nnd"])
ax7.plot(mean_steps["area"])
ax8.plot(mean_steps["centroid"])

plt.tight_layout()
plt.show()
