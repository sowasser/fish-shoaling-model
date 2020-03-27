#!/bin/sh
#SBATCH -p ProdQ
#SBATCH -N 1
#SBATCH -t 0:05:00
# Charge job to myaccount
#SBATCH -A ngear014c
# Write stdout+stderr to file
#SBATCH -o ../output/output.txt
# Mail me on job start & end
#SBATCH --mail-user=ichec@sowasser.com
#SBATCH --mail-type=BEGIN,END

# This job's working directory
cd $SLURM_SUBMIT_DIR

module load taskfarm
export TASKFARM_GROUP=20
taskfarm modelruns.txt
