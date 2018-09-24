"""
Script for testing parts of the model that are difficult to debug within the
whole complex.

Right now working on fixing the data collectors so they an differentiate
between the different agent types.
"""

from shoal_model import *
import matplotlib.pyplot as plt


model50 = ShoalModel(initial_fish=50,
                     initial_obstruct=4000,
                     width=100,
                     height=100,
                     speed=1,
                     vision=10,
                     separation=2)
for j in range(10):
    model50.step()
data50 = model50.datacollector.get_model_vars_dataframe()


# Plotting
plt.style.use("dark_background")
fig = plt.figure(figsize=(5, 5))
ax1 = fig.add_subplot(111)

ax1.plot(data50["Shoal Area"])

plt.show()

