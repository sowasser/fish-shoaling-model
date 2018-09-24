"""
Script for testing parts of the model that are difficult to debug within the
whole complex.

Right now working on fixing the data collectors so they an differentiate
between the different agent types.
"""

from shoal_model import *
import matplotlib.pyplot as plt

import numpy as np
import math
from statsmodels.robust.scale import mad


def polar(model):
    """
    Computes median absolute deviation (MAD) from the mean velocity of the
    group. As the value approaches 0, polarization increases.
    To find the MAD, the x,y coordinates are converted to radians by finding
    the arc tangent of y/x. The function used pays attention to the sign of
    the input to make sure that the correct quadrant for the angle is determined.
    """
    velocity_x = [agent.velocity[0] for agent in model.schedule.agents]
    velocity_y = [agent.velocity[1] for agent in model.schedule.agents]
    angle = []
    for (y, x) in zip(velocity_y, velocity_x):
        a = math.atan2(y, x)
        angle.append(a)
    return mad(np.asarray(angle), center=np.median)


model50 = ShoalModel()
for j in range(1000):
    model50.step()
data50 = model50.datacollector.get_model_vars_dataframe()


# Plotting
plt.style.use("dark_background")
fig = plt.figure(figsize=(5, 5))
ax1 = fig.add_subplot(111)

ax1.plot(data50["Polarization"])

plt.xlim(0, 100)
plt.ylim(0, 100)

plt.show()

