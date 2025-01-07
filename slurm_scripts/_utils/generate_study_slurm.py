from argparse import ArgumentParser
from pathlib import Path
from shutil import copyfile
from textwrap import dedent
from typing import TextIO


# == HELPERS == #
def resolve_root_path(path_str: str):
    # Run glob on the search pattern to get our list of files
    lead = path_str[0]
    if lead == '/':
        return Path('/')
    else:
        return Path(lead).resolve()


def parse_glob_pattern(pattern: str):
    # Run glob on the search pattern to get our list of files
    root_path = resolve_root_path(pattern)
    pattern = pattern[1:]
    return root_path.glob(pattern)


def init_slurm_out(slurm_header: Path, output: Path, overwrite: bool):
    # Confirm that the slurm header exists
    if not slurm_header.exists():
        raise ValueError("No SLURM-like header file exists at the designated path!")
    # Confirm that the slurm header is a file
    if not slurm_header.is_file():
        raise ValueError("The SLURM-like header designated is not a file!")

    # If an output file already exists and the overwrite flag was not given, error out to be safe
    if output.exists() and not overwrite:
        raise ValueError("Destination for new SLURM file already exists, and was about to be overwritten! "
                         "Use the '--overwrite' flag if this was intended.")

    # Generate the output directory if it doesn't already exist
    output.parent.mkdir(exist_ok=True, parents=True)

    # Copy the slurm header file to initialize our output file
    copyfile(slurm_header, output)

# == FILE IO == #
def slurm_init(fp: TextIO, n_jobs: int, conda_env_name: str):
    # Extend the script with the number of array jobs needed + environment setup
    # NOTE: 0 indexing means the (n)th job is the (n-1)th index, hence the -1 offset
    fp.write(dedent(
        f"""
        #SBATCH --array=0-{n_jobs-1}
    
        # Purge any loaded modules
        module purge
        """)
    )

    # If a conda environment was specified, have the script activate it as well
    if conda_env_name is not None:
        fp.write(dedent(f"""
            # Reset to the base environment; otherwise stupidity ensues
            source activate base
            
            # Load the Conda environment
            conda activate {conda_env_name}
        """))


def slurm_main(
        fp: TextIO,
        data_glob: str, n_data: int,
        model_glob: str, n_models: int,
        study_glob: str,
        run_ml_analysis_path: Path
):
    # This makes some very stupid looking glob searches sometimes,
    # but doing this ensures the script works even when moved!
    resolved_data_glob = resolve_root_path(data_glob) / data_glob
    resolved_model_glob = resolve_root_path(model_glob) / model_glob
    resolved_study_glob = resolve_root_path(study_glob) / study_glob

    # Write the modulo-based indexing code
    fp.write(dedent(f"""
    # Pre-calculated using 'generate_study_slurm.py'
    N_MODELS={n_models}
    STUDY_DIVISOR={n_data * n_models}
    
    # Get the study config to use via floor divide
    STUDY_IDX=$(($SLURM_ARRAY_TASK_ID / $STUDY_DIVISOR + 1))
    STUDY_FILE=`ls {resolved_study_glob} | head -n $STUDY_IDX | tail -n 1`
    
    # Get the 'inner' index via modulo of the outer
    INNER_IDX=$(($SLURM_ARRAY_TASK_ID % $STUDY_DIVISOR))
    
    # With the inner index, get the model config via modulo
    MODEL_IDX=$(($INNER_IDX % $N_MODELS + 1))
    MODEL_FILE=`ls {resolved_model_glob} | head -n $MODEL_IDX | tail -n 1`
    
    # With the inner index, get the data config via floor divide
    DATA_IDX=$(($INNER_IDX / $N_MODELS + 1))
    DATA_FILE=`ls {resolved_data_glob} | head -n $DATA_IDX | tail -n 1`
    
    # Run the resulting script
    python "{run_ml_analysis_path}" -d "$DATA_FILE" -m "$MODEL_FILE" -s "$STUDY_FILE" --overwrite
    """))

def debug_replicate_arrayjob(data_paths, model_paths, study_paths):
    n_data = len(data_paths)
    n_model = len(model_paths)
    n_study = len(study_paths)
    study_divisor = n_data * n_model

    for slurm_arr_task_id in range(n_data * n_model * n_study):
        study_idx = slurm_arr_task_id // study_divisor # +1
        inner_idx = slurm_arr_task_id % study_divisor

        data_idx = inner_idx // n_model  # +1

        model_idx = inner_idx % n_model # +1

        print(f'python ~/dcm-classic-ml/modular_optuna_ml/run_ml_analysis.py '
              f'-d "{data_paths[data_idx]}" '
              f'-m "{model_paths[model_idx]}" '
              f'-s "{study_paths[study_idx]}" --overwrite')


# == MAIN == #
def main(data_glob_pattern: str, model_glob_pattern: str, study_glob_pattern: str, slurm_header: Path, output: Path,
         run_ml_analysis: Path, overwrite: bool, conda_env_name: str, debug: bool):
    # Ensure that each of the glob patterns is valid and produces a useful result
    data_paths = list(parse_glob_pattern(data_glob_pattern))
    n_data_paths = len(data_paths)
    if n_data_paths < 1:
        raise ValueError("No data config paths found using the glob pattern provided!")
    model_paths = list(parse_glob_pattern(model_glob_pattern))
    n_model_paths = len(model_paths)
    if n_model_paths < 1:
        raise ValueError("No model config paths found using the glob pattern provided!")
    study_paths = list(parse_glob_pattern(study_glob_pattern))
    n_study_paths = len(study_paths)
    if n_study_paths < 1:
        raise ValueError("No study config paths found using the glob pattern provided!")

    # Confirm that the run_ml_analysis file exists and is a valid file
    if not run_ml_analysis.exists():
        raise ValueError("The specified 'run_ml_analysis' path does not exist!")
    if not run_ml_analysis.is_file():
        raise ValueError("The specified 'run_ml_analysis' path is not a file!")

    # Initialize the file using the provided SLURM header
    init_slurm_out(slurm_header, output, overwrite)
    # Extend it with the rest of our script
    with open(output, mode='a') as fp:
        # Add the initial header and environment resetting code
        slurm_init(fp, n_data_paths * n_model_paths * n_study_paths, conda_env_name)

        # Extend it with the actual processing code
        slurm_main(
            fp,
            data_glob_pattern, n_data_paths,
            model_glob_pattern, n_model_paths,
            study_glob_pattern, run_ml_analysis
        )

        # If debugging is on, do a "dry run" by listing out all commands as they would have been submitted to SLURM
        if debug:
            debug_replicate_arrayjob(data_paths, model_paths, study_paths)


if __name__ == '__main__':
    # Only parse command line arguments if we're running the script from the command line
    parser = ArgumentParser(
        description="Automatically generates a array-job SLURM script which will submit all possible combinations of a "
                    "set of data, model, and study configs present within a directory to the UCalgary ARC compute "
                    "cluster."
    )

    parser.add_argument(
        '-d', '--data_glob_pattern', type=str, required=True,
        help="Glob-like search pattern to use when searching for dataset configs the resulting "
             "array-job SLURM script should iterate through."
    )
    parser.add_argument(
        '-m', '--model_glob_pattern', type=str, required=True,
        help="Glob-like search pattern to use when searching for model configs the resulting "
             "array-job SLURM script should iterate through."
    )
    parser.add_argument(
        '-s', '--study_glob_pattern', type=str, required=True,
        help="Glob-like search pattern to use when searching for study configs the resulting "
             "array-job SLURM script should iterate through."
    )
    parser.add_argument(
        '-sl', '--slurm_header', type=Path, required=True,
        help="The SLURM header to use, without the '--array' component (which will be added by this script). "
             "Please refer to the the SLURM documentation on the 'sbatch' command for what this can include."
    )
    parser.add_argument(
        '-o', '--output', type=Path, default='run_ml_study.sl',
        help="The path and file name to output the resulting slurm script to. If the path specified doesn't exist, "
             "it will be created before the file is written"
    )
    parser.add_argument(
        '--run_ml_analysis', type=Path, required=True,
        help="Path to the 'run_ml_analysis.py' which should run for each array job with the corresponding config files."
    )
    parser.add_argument(
        '--overwrite', action='store_true', default=False,
        help="If this flag is present, this script WILL overwrite any existing SLURM script at the destination without "
             "warning! Be careful if you're using this flag!"
    )
    parser.add_argument(
        '--conda_env_name', type=str, default=None,
        help="The conda/mamba environment to load before running the analysis. If none is provided, assumes you will "
             "load the environment yourself at some point manually."
    )
    parser.add_argument(
        '--debug', action='store_true', default=False,
        help="Whether to run a 'debugging' run, listing out the full array of script calls which would be submitted via "
             "SLURM."
    )

    # Run the main script using the parsed arguments
    kwargs = parser.parse_args().__dict__
    main(**kwargs)
