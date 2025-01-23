# Generate for the clinical-only dataset
python generate_data_configs.py -s "../cleaned/clinical_only.tsv" -o "../configs/clinical" -l "" --has_clinical

# Generate for the DeepSeg (Binary) Datasets
## Vertebral-Metrics
python generate_data_configs.py -s "../cleaned/deepseg_binary_c2c6/vertebral/vert*.tsv" -o "../configs/deepseg_binary_c2c6/vertebral" -l "binary_vertebral" --has_imaging
python generate_data_configs.py -s "../cleaned/deepseg_binary_c2c7/vertebral/vert*.tsv" -o "../configs/deepseg_binary_c2c7/vertebral" -l "binary_vertebral" --has_imaging
python generate_data_configs.py -s "../cleaned/deepseg_binary_c2c6/vertebral/full*.tsv" -o "../configs/deepseg_binary_c2c6/vertebral" -l "binary_vertebral" --has_imaging --has_clinical
python generate_data_configs.py -s "../cleaned/deepseg_binary_c2c7/vertebral/full*.tsv" -o "../configs/deepseg_binary_c2c7/vertebral" -l "binary_vertebral" --has_imaging --has_clinical
## Per-slice Statistics
python generate_data_configs.py -s "../cleaned/deepseg_binary_c2c6/perslice/slice*.tsv" -o "../configs/deepseg_binary_c2c6/perslice" -l "binary_perslice" --has_imaging
python generate_data_configs.py -s "../cleaned/deepseg_binary_c2c7/perslice/slice*.tsv" -o "../configs/deepseg_binary_c2c7/perslice" -l "binary_perslice" --has_imaging
python generate_data_configs.py -s "../cleaned/deepseg_binary_c2c6/perslice/full*.tsv" -o "../configs/deepseg_binary_c2c6/perslice" -l "binary_perslice" --has_imaging --has_clinical
python generate_data_configs.py -s "../cleaned/deepseg_binary_c2c7/perslice/full*.tsv" -o "../configs/deepseg_binary_c2c7/perslice" -l "binary_perslice" --has_imaging --has_clinical


# Generate for the DeepSeg (Soft) Datasets
## Vertebral-Metrics
python generate_data_configs.py -s "../cleaned/deepseg_soft_c2c6/vertebral/vert*.tsv" -o "../configs/deepseg_soft_c2c6/vertebral" -l "soft_vertebral" --has_imaging
python generate_data_configs.py -s "../cleaned/deepseg_soft_c2c7/vertebral/vert*.tsv" -o "../configs/deepseg_soft_c2c7/vertebral" -l "soft_vertebral" --has_imaging
python generate_data_configs.py -s "../cleaned/deepseg_soft_c2c6/vertebral/full*.tsv" -o "../configs/deepseg_soft_c2c6/vertebral" -l "soft_vertebral" --has_imaging --has_clinical
python generate_data_configs.py -s "../cleaned/deepseg_soft_c2c7/vertebral/full*.tsv" -o "../configs/deepseg_soft_c2c7/vertebral" -l "soft_vertebral" --has_imaging --has_clinical
## Per-slice Statistics
python generate_data_configs.py -s "../cleaned/deepseg_soft_c2c6/perslice/slice*.tsv" -o "../configs/deepseg_soft_c2c6/perslice" -l "soft_perslice" --has_imaging
python generate_data_configs.py -s "../cleaned/deepseg_soft_c2c7/perslice/slice*.tsv" -o "../configs/deepseg_soft_c2c7/perslice" -l "soft_perslice" --has_imaging
python generate_data_configs.py -s "../cleaned/deepseg_soft_c2c6/perslice/full*.tsv" -o "../configs/deepseg_soft_c2c6/perslice" -l "soft_perslice" --has_imaging --has_clinical
python generate_data_configs.py -s "../cleaned/deepseg_soft_c2c7/perslice/full*.tsv" -o "../configs/deepseg_soft_c2c7/perslice" -l "soft_perslice" --has_imaging --has_clinical
