# Create some convenience variable to avoid a lot of copy-pasting
PROJECT_ROOT="/home/kalum.ost/projects/dcm-classic-ml"
DATA_ROOT="$PROJECT_ROOT/datasets/configs"

# Generate the clinical study array uniquely, as its not nested like the others
python generate_study_slurm.py \
  -d "$PROJECT_ROOT/datasets/configs/clinical/*.json" \
  -s "$PROJECT_ROOT/study/study_config.json" \
  -m "$PROJECT_ROOT/models/*.json" \
  -sl "kost_slurm_header.sl" \
  -o "study_sbatch/run_studies_clinical.sl" \
  --run_ml_analysis "$PROJECT_ROOT/modular_optuna_ml/run_ml_analysis.py" \
  --conda_env_name "dcm-classic-ml" \
  --overwrite

# Generate array jobs for DeepSeg (Binary C2C6)
python generate_study_slurm.py \
  -d "$PROJECT_ROOT/datasets/configs/deepseg_binary_c2c6/*/*.json" \
  -s "$PROJECT_ROOT/study/study_config.json" \
  -m "$PROJECT_ROOT/models/*.json" \
  -sl "kost_slurm_header.sl" \
  -o "study_sbatch/run_studies_deepseg_binary_c2c6.sl" \
  --run_ml_analysis "$PROJECT_ROOT/modular_optuna_ml/run_ml_analysis.py" \
  --conda_env_name "dcm-classic-ml" \
  --overwrite
# Generate array jobs for DeepSeg (Binary C2C7)
python generate_study_slurm.py \
  -d "$PROJECT_ROOT/datasets/configs/deepseg_binary_c2c7/*/*.json" \
  -s "$PROJECT_ROOT/study/study_config.json" \
  -m "$PROJECT_ROOT/models/*.json" \
  -sl "kost_slurm_header.sl" \
  -o "study_sbatch/run_studies_deepseg_binary_c2c7.sl" \
  --run_ml_analysis "$PROJECT_ROOT/modular_optuna_ml/run_ml_analysis.py" \
  --conda_env_name "dcm-classic-ml" \
  --overwrite
# Generate array jobs for DeepSeg (Soft C2C6)
python generate_study_slurm.py \
  -d "$PROJECT_ROOT/datasets/configs/deepseg_soft_c2c6/*/*.json" \
  -s "$PROJECT_ROOT/study/study_config.json" \
  -m "$PROJECT_ROOT/models/*.json" \
  -sl "kost_slurm_header.sl" \
  -o "study_sbatch/run_studies_deepseg_soft_c2c6.sl" \
  --run_ml_analysis "$PROJECT_ROOT/modular_optuna_ml/run_ml_analysis.py" \
  --conda_env_name "dcm-classic-ml" \
  --overwrite
# Generate array jobs for DeepSeg (Soft C2C7)
python generate_study_slurm.py \
  -d "$PROJECT_ROOT/datasets/configs/deepseg_soft_c2c7/*/*.json" \
  -s "$PROJECT_ROOT/study/study_config.json" \
  -m "$PROJECT_ROOT/models/*.json" \
  -sl "kost_slurm_header.sl" \
  -o "study_sbatch/run_studies_deepseg_soft_c2c7.sl" \
  --run_ml_analysis "$PROJECT_ROOT/modular_optuna_ml/run_ml_analysis.py" \
  --conda_env_name "dcm-classic-ml" \
  --overwrite