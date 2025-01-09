# Generate for the clinical-only dataset
python generate_data_configs.py -s "../cleaned/clinical_only.tsv" -o "../cleaned/configs/clinical" -l "" --has_clinical

# Generate for the DeepSeg (Binary) Datasets
python generate_data_configs.py -s "../cleaned/deepseg_binary_c2c6/vert*.tsv" -o "../cleaned/configs/deepseg_binary_c2c6" -l "" --has_imaging
python generate_data_configs.py -s "../cleaned/deepseg_binary_c2c7/vert*.tsv" -o "../cleaned/configs/deepseg_binary_c2c7" -l "" --has_imaging
python generate_data_configs.py -s "../cleaned/deepseg_binary_c2c6/full*.tsv" -o "../cleaned/configs/deepseg_binary_c2c6" -l "" --has_imaging --has_clinical
python generate_data_configs.py -s "../cleaned/deepseg_binary_c2c7/full*.tsv" -o "../cleaned/configs/deepseg_binary_c2c7" -l "" --has_imaging --has_clinical

# Generate for the DeepSeg (Soft) Datasets
python generate_data_configs.py -s "../cleaned/deepseg_soft_c2c6/vert*.tsv" -o "../cleaned/configs/deepseg_soft_c2c6" -l "" --has_imaging
python generate_data_configs.py -s "../cleaned/deepseg_soft_c2c7/vert*.tsv" -o "../cleaned/configs/deepseg_soft_c2c7" -l "" --has_imaging
python generate_data_configs.py -s "../cleaned/deepseg_soft_c2c6/full*.tsv" -o "../cleaned/configs/deepseg_soft_c2c6" -l "" --has_imaging --has_clinical
python generate_data_configs.py -s "../cleaned/deepseg_soft_c2c7/full*.tsv" -o "../cleaned/configs/deepseg_soft_c2c7" -l "" --has_imaging --has_clinical
