# Copy the participants file from our BIDS dataset locally for ease-of-access
mkdir -p "../raw/"
cp "/work/cadotte_lab/bids_cmri/participants.tsv" "../raw/participants.tsv"

# Concatenate the results of our per-vertebrae analyses into large files, to be processed later with data cleaning
mkdir -p "../raw/deepseg_binary_c2c6"
mkdir -p "../raw/deepseg_binary_c2c7"
mkdir -p "../raw/deepseg_soft_c2c6"
mkdir -p "../raw/deepseg_soft_c2c7"

cat /work/cadotte_lab/bids_cmri/derivatives/sct_6.5/*/*/deepsegv2_vertebrae_metrics.csv > "../raw/deepseg_binary_c2c6/vertebral.csv"
cat /work/cadotte_lab/bids_cmri/derivatives/sct_6.5/*/*/deepsegv2_vertebrae_metrics_c2c7.csv > "../raw/deepseg_binary_c2c7/vertebral.csv"
cat /work/cadotte_lab/bids_cmri/derivatives/sct_6.5/*/*/softseg_vertebrae_metrics.csv > "../raw/deepseg_soft_c2c6/vertebral.csv"
cat /work/cadotte_lab/bids_cmri/derivatives/sct_6.5/*/*/softseg_vertebrae_metrics_c2c7.csv > "../raw/deepseg_soft_c2c7/vertebral.csv"

cat /work/cadotte_lab/bids_cmri/derivatives/sct_6.5/*/*/deepsegv2_slice_metrics.csv > "../raw/deepseg_binary_c2c6/perslice.csv"
cat /work/cadotte_lab/bids_cmri/derivatives/sct_6.5/*/*/deepsegv2_slice_metrics_c2c7.csv > "../raw/deepseg_binary_c2c7/perslice.csv"
cat /work/cadotte_lab/bids_cmri/derivatives/sct_6.5/*/*/softseg_slice_metrics.csv > "../raw/deepseg_soft_c2c6/perslice.csv"
cat /work/cadotte_lab/bids_cmri/derivatives/sct_6.5/*/*/softseg_slice_metrics_c2c7.csv > "../raw/deepseg_soft_c2c7/perslice.csv"
