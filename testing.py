"""
Script for testing parts of the model that are difficult to debug within the
whole complex.

Right now working on plotting the points needed for obstruction agents forming
a border around the model space.
"""

import numpy as np
import matplotlib.pyplot as plt

left = [(40, n) for n in range(40, 60)]
top = [(n, 60) for n in range(40, 60)]
right = [(60, n) for n in range(40, 60)]
bottom = [(n, 40) for n in range(40, 60)]

borders = left + top + right + bottom
x = [x[0] for x in borders]
y = [y[1] for y in borders]
pos = np.array((x, y))

# Plotting
plt.style.use("dark_background")
fig = plt.figure(figsize=(5, 5))
ax1 = fig.add_subplot(111)

ax1.scatter(pos[0], pos[1])

plt.xlim(0, 100)
plt.ylim(0, 100)

plt.show()

