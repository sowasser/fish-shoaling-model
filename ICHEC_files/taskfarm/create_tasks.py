"""
Script for generating the task list to run the taskfarm on the ICHEC cluster.
The tasks are run based on a .txt file where each run is a task that has its
own data output.

TODO: fiure out how to break up the different parameters.
"""

import os

path = "/Users/user/Desktop/Local/Mackerel/fish-shoaling-model/ICHEC_files/taskfarm"
file = open(os.path.join(path, r"modelruns.txt"), "w")
for i in range(10):
    file.write("python3 ../../ichec_run.py > ../output/25feb2020/task" + str(i) + "_output.txt \n")

file.close()
