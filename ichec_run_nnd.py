"""
Basic script for running the model on the Irish High End Computing Cluster
(ICHEC). On the cluster, the print data is saved in a .txt file for each job
(a set of runs) completed. Many of these are created.

In this file, all factors (speed, vision, separation, cohere, separate, match)
are varied and the only data collected is nearest neighbour distance (nnd).
"""
# Todo: figure out how to divide model runs for the different tasks
# Todo: figure out how to combine data afterwards

from shoal_model_nnd import *
import pandas as pd
import sys


def run_model(speed_prior, vision_prior, separation_prior,
              cohere_prior, separate_prior, match_prior):
    """
    Runs the shoal model for a certain number of steps with all of the
    parameters are fixed. Returns a dataframe with the average per run of all
    data collectors (average of all steps) and columns with the parameter
    values for that run, including the varying & fixed parameters so all
    dataframes can be stacked together.
    """
    model = ShoalModel_nnd(n_fish=20,
                           width=100,
                           height=100,
                           speed=speed_prior,
                           vision=vision_prior,
                           separation=separation_prior,
                           cohere=cohere_prior,
                           separate=separate_prior,
                           match=match_prior)
    for step in range(300):  # number of steps to run the model for
        model.step()
    data = model.datacollector.get_model_vars_dataframe()  # retrieve data from model
    data_trim = data.iloc[200:, ]  # remove some # of early runs
    # Condense data collectors into summary stats
    min = data_trim.min(axis=0)
    max = data_trim.max(axis=0)
    mean = data_trim.mean(axis=0)
    std = data_trim.std(axis=0)
    all_data = pd.concat([min, max, mean, std], axis=0)
    all_data["speed"] = speed_prior  # add speed value column
    all_data["vision"] = vision_prior  # add vision columnm
    all_data["separation"] = separation_prior  # add separation column
    all_data["cohere"] = cohere_prior  # add speed value column
    all_data["separate"] = separate_prior  # add vision columnm
    all_data["match"] = match_prior  # add separation column
    return pd.DataFrame(all_data).T


# Run model with prior called in create_tasks.py, as a float
model_data = run_model(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]),
                       float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]))

# Re-name columns so all data will print & index with unique values for R.
model_data.columns = ["nnd_min", "nnd_max", "nnd_mean", "nnd_std",
                      "speed", "vision", "separation",
                      "cohere", "separate", "match"]

pd.set_option("display.max_columns", None)  # display all columns
pd.set_option("display.width", 1000)  # stop print from splitting columns on to new lines

print(model_data)  # printing makes the data accessible from the cluster.