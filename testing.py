"""
Script for testing parts of the model that are difficult to debug within the
whole complex.
"""

from shoal_model_pos import *
import pandas as pd
import matplotlib.pyplot as plt

# Collect the data from a single run with x number of steps into a dataframe
model = ShoalModel()
for i in range(5):
    model.step()
data = model.datacollector.get_model_vars_dataframe()


# ###########################################
# # POSITION DATA MAPPING #
# ###########################################
#
# # This code is from the data_sensitivity_heatmap.py script, so more information
# # and code about how the other data collectors can be pulled out can be found
# # there. Mostly, I'm now trying to figure out how to do animations and hot to
# # get matplotlib's pcolormesh to work for me to create a heatmap of density,
# # rather than a scatter plot.
#
# # Separate data from data collectors into numpy arrays so they can be accessed more easily
# np_data = np.asarray(data)
#
# position = np_data[:, 4].flatten()  # select position data, remove one set of brackets & make a dataframe
# pos_df = pd.DataFrame(position.flatten())  # remove one set of brackets & make a dataframe
# pos_df = pos_df[0].apply(pd.Series)  # remove another set of brackets
# pos_df[0].apply(pd.Series)  # remove last set of brackets
# np_pos = np.asarray(pos_df)  # back to numpy array
#
# # isolate x and y positions
# x = np_pos[:, 0::2]
# y = np_pos[:, 1::2]
#
#
# # # Plotting
# plt.style.use("dark_background")
#
#
# fig = plt.figure(figsize=(6, 6))
# ax = fig.add_subplot(111)
# plt.title("Position of Fish")  # Todo: figure out sequential step numbering
#
# scatter = ax.scatter(x[0, :], y[0, :])  # select which step by selecting a row
# plt.show()
