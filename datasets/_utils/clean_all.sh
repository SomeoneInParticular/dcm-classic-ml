# Clean up the clinical data first
echo "## Clinical ##"
python clinical_cleanup.py

# Then clean up each of the vertebral results
echo "## DeepSeg Binary C2C6 - Vertebral ##"
python vertebral_cleanup.py \
  -i ../raw/deepseg_binary_c2c6/vertebral.csv \
  -o ../cleaned/deepseg_binary_c2c6/vertebral/ \
  --label 'vert_only'
echo "## DeepSeg Binary C2C7 - Vertebral ##"
python vertebral_cleanup.py \
  -i ../raw/deepseg_binary_c2c7/vertebral.csv \
  -o ../cleaned/deepseg_binary_c2c7/vertebral/ \
  --label 'vert_only'
echo "## DeepSeg Soft C2C6 - Vertebral ##"
python vertebral_cleanup.py \
  -i ../raw/deepseg_soft_c2c6/vertebral.csv \
  -o ../cleaned/deepseg_soft_c2c6/vertebral/ \
  --label 'vert_only'
echo "## DeepSeg Soft C2C7 - Vertebral ##"
python vertebral_cleanup.py \
  -i ../raw/deepseg_soft_c2c7/vertebral.csv \
  -o ../cleaned/deepseg_soft_c2c7/vertebral/ \
  --label 'vert_only'

# And then clean up each of the per-slice results
echo "## DeepSeg Binary C2C6 - Per-Slice ##"
python perslice_cleanup.py \
  -i ../raw/deepseg_binary_c2c6/perslice.csv \
  -o ../cleaned/deepseg_binary_c2c6/perslice/ \
  --label 'slice_only'
echo "## DeepSeg Binary C2C7 - Per-Slice ##"
python perslice_cleanup.py \
  -i ../raw/deepseg_binary_c2c7/perslice.csv \
  -o ../cleaned/deepseg_binary_c2c7/perslice/ \
  --label 'slice_only'
echo "## DeepSeg Soft C2C6 - Per-Slice ##"
python perslice_cleanup.py \
  -i ../raw/deepseg_soft_c2c6/perslice.csv \
  -o ../cleaned/deepseg_soft_c2c6/perslice/ \
  --label 'slice_only'
echo "## DeepSeg Soft C2C7 - Per-Slice ##"
python perslice_cleanup.py \
  -i ../raw/deepseg_soft_c2c7/perslice.csv \
  -o ../cleaned/deepseg_soft_c2c7/perslice/ \
  --label 'slice_only'
