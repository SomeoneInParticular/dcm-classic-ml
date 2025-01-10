#!/bin/bash
#SBATCH --mem=16G
#SBATCH --nodes=1
#SBATCH --cpus-per-task 24
#SBATCH --time 24:00:00
#SBATCH --partition=cpu2023,cpu2022,cpu2021,cpu2019
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=kalum.ost

# Clear the workspace of anything loaded by default
#module purge

# Load a basic Python working environment (SCT will load the rest)
#module load python/3.12.5

# Run each script in DeepSeg iteratively on all data in our datasource
for f in ../deepseg/*/*/*.sh; do
	# Get the script file's name, so it can be used as the log
	log_label=${f#*/*}
	log_label=${log_label%*.*}
	log_label=${log_label//\//_}

	# Run the script on out entire cMRI dataset
	python iterative_sct.py \
		-i "/work/cadotte_lab/bids_cmri/sourcedata" \
		-o "/work/cadotte_lab/bids_cmri/derivatives/sct_6.5" \
		-t 23 \
		-s "$f" \
		-sct "/work/cadotte_lab/tools/spinalcordtoolbox-6.5/bin" \
		-l "$log_label.log"
done
