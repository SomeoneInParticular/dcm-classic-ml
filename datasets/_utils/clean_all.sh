# Clean up the clinical data first
python clinical_cleanup.py

# Then clean up each of the vertebral results
python vertebral_cleanup.py \
  -i ../raw/deepseg_binary_c2c6/vertebral.csv \
  -o ../cleaned/deepseg_binary_c2c6/ \
  --label 'vert_only'
python vertebral_cleanup.py \
  -i ../raw/deepseg_binary_c2c7/vertebral.csv \
  -o ../cleaned/deepseg_binary_c2c7/ \
  --label 'vert_only'
python vertebral_cleanup.py \
  -i ../raw/deepseg_soft_c2c6/vertebral.csv \
  -o ../cleaned/deepseg_soft_c2c6/ \
  --label 'vert_only'
python vertebral_cleanup.py \
  -i ../raw/deepseg_soft_c2c7/vertebral.csv \
  -o ../cleaned/deepseg_soft_c2c7/ \
  --label 'vert_only'
