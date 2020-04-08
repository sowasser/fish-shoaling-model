"""
Script for importing and consolidating files from the ICHEC cluster. The data
generated on the cluster are output as individual text files, which need to be
collated into one file to be run through an approximate bayesian computation
package in R (found in shoal-model-in-R).
"""

# TODO: Actually get this to work. Broken beyond generating the list of file names.

import pandas as pd
from glob import glob
import os

# Generate a list of the separation files in this folder
sep_files = glob("/Users/Sophie/Desktop/DO NOT ERASE/1NUIG/Mackerel/Mackerel Data/ICHEC/30Mar2020/sep_output*.txt")

# Read all of the files into one list
sep_data = []
for f in sep_files:
    sep_data.append(pd.read_table(f))
    
# Turn this list into a pandas dataframe
big_sep_data = pd.concat(sep_data, ignore_index=True)

# Write the dataframe to a .csv file that can be easily imported into R
path = "/Users/Sophie/Desktop/"  # for laptop
big_sep_data.to_csv(os.path.join(path, r"var-sep.csv"), index=False)
