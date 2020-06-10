"""
Basic script for running the model on the Irish High End Computing Cluster
(ICHEC). On the cluster, the print data is saved in a .txt file for each job
(a set of runs) completed. Many of these are created.
"""
# Todo: figure out how to divide model runs for the different tasks
# Todo: figure out how to combine data afterwards

from shoal_model import *
import pandas as pd


def run_model(speed_prior, vision_prior, separation_prior,
              cohere_prior, separate_prior, match_prior):
    """
    Runs the shoal model for a certain number of steps with all of the
    parameters are fixed. Returns a dataframe with the average per run of all
    data collectors (average of all steps) and columns with the parameter
    values for that run, including the varying & fixed parameters so all
    dataframes can be stacked together.
    """
    model = ShoalModel(n_fish=20,
                       width=50,
                       height=50,
                       speed=speed_prior,
                       vision=vision_prior,
                       separation=separation_prior,
                       cohere=cohere_prior,
                       separate=separate_prior,
                       match=match_prior)
    for step in range(30):  # number of steps to run the model for
        model.step()
    data = model.datacollector.get_model_vars_dataframe()  # retrieve data from model
    # Add columns with the prior values for each parameter.
    data.insert(loc=4, column="speed", value=speed_prior)
    data.insert(loc=5, column="vision", value=vision_prior)
    data.insert(loc=6, column="separation", value=separation_prior)
    data.insert(loc=7, column="cohere", value=cohere_prior)
    data.insert(loc=8, column="separate", value=separate_prior)
    data.insert(loc=9, column="match", value=match_prior)
    return pd.DataFrame(data)


# Run model with prior called in create_tasks.py, as a float
model_data = run_model(2, 10, 2, 0.3, 0.03, 0.7)

# Re-name columns so all data will print & index with unique values for R.
model_data.columns = ["polar", "nnd", "area", "cent",
                      "speed", "vision", "separation",
                      "cohere", "separate", "match"]

pd.set_option("display.max_columns", None)  # display all columns
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 1000)  # stop print from splitting columns on to new lines

print(model_data)  # printing makes the data accessible from the cluster.