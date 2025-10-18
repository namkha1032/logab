#!/bin/bash

#SBATCH -p a100
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --time=00:05:00
#SBATCH --mem=32GB
#SBATCH --gpus-per-node=1

#SBATCH --output=./logs/slurm-%j.log
#SBATCH --error=./logs/slurm-%j.log

#SBATCH --mail-type=ALL
#SBATCH --mail-user=namkha.nguyen@adelaide.edu.au

source /hpcfs/users/a1956473/miniconda3/etc/profile.d/conda.sh
conda activate base

# export TRANSFORMERS_OFFLINE=1

cd /hpcfs/users/a1956473/projects/logab/
python /hpcfs/users/a1956473/projects/logab/main_exec.py