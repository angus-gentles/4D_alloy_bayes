#!/usr/bin/env bash
#SBATCH -J 4Dab
#SBATCH --output=do_alby.txt
#SBATCH -N 2
#SBATCH --ntasks-per-node=128
#SBATCH --partition=zen3_2048
#SBATCH --qos=zen3_2048
#SBATCH --time 3-00:00:00   # max runtime hh:mm:ss
source setup_conda.sh
conda activate alloy_bayes
./full_process.py