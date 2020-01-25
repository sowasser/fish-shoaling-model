"""
Script for a single run of the model, with a print statement to make sure it worked.
"""

from shoal_model import *

# Collect the data from a single run with x number of steps into a dataframe
model = ShoalModel()
for i in range(10):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
# data.columns = ["polar", "nnd", "area", "centroid", "mass"]

print(data)
