# For each image-derived dataset...
for f in ../cleaned/*/vert_only*.tsv; do
  # Determine the root path and label for the file
  root_path=${f%*/*}
  label=${f#*vert_only*}

  # Identify the output path for the result
  full_out="$root_path/full$label"

  # Run the joining script to join this file with clinical metrics from "clinical_only.tsv"
  python join_by_grp.py -i1 "../cleaned/clinical_only.tsv" -i2 $f -o $full_out
done