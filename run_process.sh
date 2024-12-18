#!/usr/bin/env bash
#SBATCH -J 4Dab
#SBATCH --output=do_alby2.txt
#SBATCH -N 2
#SBATCH --ntasks-per-node=128
#SBATCH --partition=zen3_0512_a100x2
#SBATCH --qos=zen3_0512_a100x2
# SBATCH --time 00:10:00
#SBATCH --time 3-00:00:00   # max runtime hh:mm:ss
source setup_conda.sh
conda activate alloy_bayes
./full_process_expanded.py
