"""
Script for testing parts of the model that are difficult to debug within the
whole complex.
"""

from shoal_model import *
import pandas as pd
import matplotlib.pyplot as plt

###########################################
# POSITION DATA MAPPING #
###########################################

# Collect the data from a single run with x number of steps into a dataframe
model = ShoalModel(initial_fish=50,
                   initial_obstruct=4000,
                   width=100,
                   height=100,
                   speed=1,
                   vision=10,
                   separation=10)
for i in range(10):
    model.step()
data = model.datacollector.get_model_vars_dataframe()

# Separate data from data collectors into numpy arrays so they can be accessed more easily
np_data = np.asarray(data)

position = np_data[:, 4].flatten()  # remove one set of brackets & make a dataframe
pos_df = pd.DataFrame(position.flatten())  # remove one set of brackets & make a dataframe
pos_df = pos_df[0].apply(pd.Series)  # remove another set of brackets
pos_df[0].apply(pd.Series)  # remove last set of brackets
np_pos = np.asarray(pos_df)  # back to numpy array

# isolate first positions in the first step
x1 = np_pos[0, 0::2].tolist()
y1 = np_pos[0, 1::2].tolist()
step1 = [x1, y1]


# # Plotting
plt.style.use("dark_background")

x = range(100)
y = range(100)

fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111)
plt.title("Position of Fish")  # Todo: figure out sequential step numbering

scatter = ax.scatter(x1, y1)
plt.show()
