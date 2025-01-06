#!/bin/bash
#SBATCH --mem=1G
#SBATCH --nodes=1
#SBATCH --cpus-per-task 16
#SBATCH --time 24:00:00
#SBATCH --partition=cpu2023,cpu2022,cpu2021,cpu2019
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=kalum.ost