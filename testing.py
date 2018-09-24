"""
Script for testing parts of the model that are difficult to debug within the
whole complex.
"""

from shoal_model import *
import matplotlib.pyplot as plt

###########################################
# GRAPHS OF DATA COLLECTORS FOR DEBUGGING #
###########################################

model = ShoalModel(initial_fish=50,
                   initial_obstruct=4000,
                   width=100,
                   height=100,
                   speed=1,
                   vision=10,
                   separation=2)
for i in range(10):
    model.step()
data = model.datacollector.get_model_vars_dataframe()


plt.style.use("dark_background")
fig = plt.figure(figsize=(6, 4), dpi=300)
ax1 = plt.subplot(2, 2, 1)
plt.title("Polarization")
ax2 = plt.subplot(2, 2, 2)
plt.title("Nearest Neighbour Distance")
ax3 = plt.subplot(2, 2, 3)
plt.title("Shoal Area")
ax4 = plt.subplot(2, 2, 4)
plt.title("Mean Distance from Centroid")

ax1.plot(data["Polarization"])
ax2.plot(data["Nearest Neighbour Distance"])
ax3.plot(data["Shoal Area"])
ax4.plot(data["Mean Distance from Centroid"])

plt.tight_layout()
plt.show()
