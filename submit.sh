#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=short
#SBATCH --time=0-08:00:00
#SBATCH --mem-per-cpu=5800
#SBATCH --output=log/slurm-%j.log
source activate.sh
python approximate_gradient.py $1 $2
