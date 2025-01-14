# Copy the participants file from our BIDS dataset locally for ease-of-access
cp "/work/cadotte_lab/bids_cmri/participants.tsv" "../raw/participants.tsv"

# Concatenate the results of our per-vertebrae analyses into large files, to be processed later with data cleaning
cat /work/cadotte_lab/bids_cmri/derivatives/sct_6.5/*/*/deepsegv2_vertebrae_metrics.csv > "../raw/deepseg_binary_c2c6/vertebrae.csv"
cat /work/cadotte_lab/bids_cmri/derivatives/sct_6.5/*/*/deepsegv2_vertebrae_metrics_c2c7.csv > "../raw/deepseg_binary_c2c7/vertebrae.csv"
cat /work/cadotte_lab/bids_cmri/derivatives/sct_6.5/*/*/softseg_vertebrae_metrics.csv > "../raw/deepseg_soft_c2c6/vertebrae.csv"
cat /work/cadotte_lab/bids_cmri/derivatives/sct_6.5/*/*/softseg_vertebrae_metrics_c2c7.csv > "../raw/deepseg_soft_c2c7/vertebrae.csv"

cat /work/cadotte_lab/bids_cmri/derivatives/sct_6.5/*/*/deepsegv2_slice_metrics.csv > "../raw/deepseg_binary_c2c6/perslice.csv"
cat /work/cadotte_lab/bids_cmri/derivatives/sct_6.5/*/*/deepsegv2_slice_metrics_c2c7.csv > "../raw/deepseg_binary_c2c7/perslice.csv"
cat /work/cadotte_lab/bids_cmri/derivatives/sct_6.5/*/*/softseg_slice_metrics.csv > "../raw/deepseg_soft_c2c6/perslice.csv"
cat /work/cadotte_lab/bids_cmri/derivatives/sct_6.5/*/*/softseg_slice_metrics_c2c7.csv > "../raw/deepseg_soft_c2c7/perslice.csv"
