"""
Script for testing parts of the model that are difficult to debug within the
whole complex.

Right now working on plotting the points needed for obstruction agents forming
a border around the model space.
"""

import numpy as np
import matplotlib.pyplot as plt

# borders = [(10, n) + (n, 20) + (20, n) + (n, 10) for n in range(10, 20)]

left = [(0, n) for n in range(100)]
x_l = [x[0] for x in left]
y_l = [y[1] for y in left]
pos_l = np.array((x_l, y_l))

top = [(n, 100) for n in range(100)]
x_t = [x[0] for x in top]
y_t = [y[1] for y in top]
pos_t = np.array((x_t, y_t))

right = [(100, n) for n in range(100)]
x_r = [x[0] for x in right]
y_r = [y[1] for y in right]
pos_r = np.array((x_r, y_r))

bottom = [(n, 0) for n in range(100)]
x_b = [x[0] for x in bottom]
y_b = [y[1] for y in bottom]
pos_b = np.array((x_b, y_b))


# pos = np.array((x, y))

# Plotting
plt.style.use("dark_background")
fig = plt.figure(figsize=(5, 5))
ax1 = fig.add_subplot(111)

ax1.scatter(x_l, y_l, label="left")
ax1.scatter(x_t, y_t, label="top")
ax1.scatter(x_r, y_r, label="right")
ax1.scatter(x_b, y_b, label="bottom")

plt.legend(loc="upper right")
plt.show()
