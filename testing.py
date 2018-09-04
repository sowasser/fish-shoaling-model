"""
Script for testing parts of the model that are difficult to debug within the
whole complex.

Right now working on plotting the points needed for obstruction agents forming
a border around the model space.
"""

import numpy as np
import matplotlib.pyplot as plt

borders = [(10, n) + (n, 20) + (20, n) + (n, 10) for n in range(10, 20)]
x = [x[0] for x in borders]
y = [y[1] for y in borders]
pos = np.array((x, y))

# Plotting
plt.style.use("dark_background")
plt.scatter(x, y)
plt.show()
