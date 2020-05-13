"""
Basic script for running the model on the Irish High End Computing Cluster
(ICHEC). On the cluster, the print data is saved in a .txt file for each job
(a set of runs) completed. Many of these are created.
"""
# Todo: figure out how to divide model runs for the different tasks
# Todo: figure out how to combine data afterwards

from shoal_model import *
import pandas as pd


def run_model(speed_prior, vision_prior, sep_prior):
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
                       separation=sep_prior)
    for step in range(50):  # number of steps to run the model for
        model.step()
    data = model.datacollector.get_model_vars_dataframe()  # retrieve data from model
    data_trim = data.iloc[10:, ]  # remove some # of early runs
    # Condense data collectors into summary stats
    min = data_trim.min(axis=0)
    max = data_trim.max(axis=0)
    mean = data_trim.mean(axis=0)
    std = data_trim.std(axis=0)
    all_data = pd.concat([min, max, mean, std], axis=0)
    all_data["speed"] = speed_prior  # add speed value column
    all_data["vision"] = vision_prior  # add vision columnm
    all_data["separation"] = sep_prior  # add separation column
    return pd.DataFrame(all_data).T


# Run model with test values
model_data = run_model(40, 100, 40)

# Re-name columns so all data will print & index with unique values for R.
model_data.columns = ["cent_min", "nnd_min", "polar_min", "area_min",
                      "cent_max", "nnd_max", "polar_max", "area_max",
                      "cent_mean", "nnd_mean", "polar_mean", "area_mean",
                      "cent_std", "nnd_std", "polar_std", "area_std",
                      "speed", "vision", "sep"]

pd.set_option("display.max_columns", None)  # display all columns
pd.set_option("display.width", 1000)  # stop print from splitting columns on to new lines

print(model_data)  # printing makes the data accessible from the cluster.
