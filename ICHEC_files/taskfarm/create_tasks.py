"""
Script for generating the task list to run the taskfarm on the ICHEC cluster.
The tasks are run based on a .txt file where each run is a task that has its
own data output.
"""

import os

# path = "/Users/user/Desktop/Local/Mackerel/fish-shoaling-model/ICHEC_files/taskfarm"  # desktop
path = "/Users/Sophie/Desktop/DO NOT ERASE/1NUIG/Mackerel/fish-shoaling-model/ICHEC_files/taskfarm"  # laptop

file = open(os.path.join(path, r"modelruns.txt"), "w")

# Write a line running the scripts varying each parameter (speed, vision,
# separation) i times
for i in range(200):
    file.write("python3 ../../ichec_run_speed.py > ../output/25Mar2020/speed_output"
               + str(i) + ".txt \n")

for i in range(200):
    file.write("python3 ../../ichec_run_vision.py > ../output/25Mar2020/vision_output"
               + str(i) + ".txt \n")

for i in range(200):
    file.write("python3 ../../ichec_run_sep.py > ../output/25Mar2020/sep_output"
               + str(i) + ".txt \n")

file.close()
