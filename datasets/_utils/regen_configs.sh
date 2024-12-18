# Generate for the clinical-only dataset
python generate_data_configs.py -s "../clinical/participants_cleaned.tsv" -o "../clinical/configs" -l "" --has_clinical

# Generate for the DeepSeg (Binary) Datasets
python generate_data_configs.py -s "../deepseg_binary/c2c6/full_*.tsv" -o "../deepseg_binary/c2c6/configs" -l "deepseg_binary_c2c6_binary" --has_clinical --has_imaging
python generate_data_configs.py -s "../deepseg_binary/c2c7/full_*.tsv" -o "../deepseg_binary/c2c7/configs" -l "deepseg_binary_c2c7_binary" --has_clinical --has_imaging
python generate_data_configs.py -s "../deepseg_binary/c2c6/img_*.tsv" -o "../deepseg_binary/c2c6/configs" -l "deepseg_binary_c2c6_binary" --has_imaging
python generate_data_configs.py -s "../deepseg_binary/c2c7/img_*.tsv" -o "../deepseg_binary/c2c7/configs" -l "deepseg_binary_c2c7_binary" --has_imaging

# Generate for the DeepSeg (Soft) Datasets
python generate_data_configs.py -s "../deepseg_soft/c2c6/full_*.tsv" -o "../deepseg_soft/c2c6/configs" -l "deepseg_soft_c2c6_binary" --has_clinical --has_imaging
python generate_data_configs.py -s "../deepseg_soft/c2c7/full_*.tsv" -o "../deepseg_soft/c2c7/configs" -l "deepseg_soft_c2c7_binary" --has_clinical --has_imaging
python generate_data_configs.py -s "../deepseg_soft/c2c6/img_*.tsv" -o "../deepseg_soft/c2c6/configs" -l "deepseg_soft_c2c6_binary" --has_imaging
python generate_data_configs.py -s "../deepseg_soft/c2c7/img_*.tsv" -o "../deepseg_soft/c2c7/configs" -l "deepseg_soft_c2c7_binary" --has_imaging
