# For each image-derived dataset...
for f in ../cleaned/*/vertebral/vert_only*.tsv; do
  # Determine the root path and label for the file
  root_path=${f%*/*}
  label=${f#*vert_only*}

  # Identify the output path for the result
  full_out="$root_path/full$label"

  # Refine the imaging dataset to contain only surgical patients (using the clinical dataset as a reference) and our target metric
  img_dataset="../cleaned/clinical_only.tsv"
  python update_imaging_with_clinical.py -c "$img_dataset" -i "$f"

  # Run the joining script to join this file with clinical metrics from "clinical_only.tsv"
  python join_by_grp.py -i1 "$img_dataset" -i2 "$f" -o "$full_out"
done