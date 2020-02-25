"""
Basic script for running the model on the Irish High End Computing Cluster
(ICHEC). On the cluster, the print data is saved in a .txt file for each job
(a set of runs) completed. Many of these are created.
"""
# Todo: figure out how to divide model runs for the different tasks
# Todo: figure out how to combine data afterwards

from shoal_model import *

# Collect the data from a single run with x number of steps into a dataframe
model = ShoalModel(n_fish=20,
                   width=50,
                   height=50,
                   speed=2,
                   vision=10,
                   separation=2)
for i in range(10):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.columns = ["polar", "nnd", "area", "cent"]

print(data)
