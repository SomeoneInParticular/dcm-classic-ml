from argparse import ArgumentParser
from copy import deepcopy
from pathlib import Path
from json import dump


# The basic template for a data config JSON, which will be filled out using the following functions later
TEMPLATE = {
  "label": None,
  "format": "tabular",
  "data_source": None,
  "separator": "\t",
  "index": "GRP",
  "pre_split_hooks": [],
  "post_split_hooks": []
}


# === PRE-SPLIT HOOKS === #
def update_presplit_clinical(config: dict):
    # Isolate the pre_split_hook list
    pre_split_hooks = config['pre_split_hooks']

    # A large number of clinical metrics are redundant/deleterious, and should be dropped explicitly
    pre_split_hooks.append({
        "type": "drop_features_explicit",
        "features": [
            "Site",
            "Surgical",
            "Number of Surgeries",
            "Treatment Plan",
            "Followup: 6-18 weeks",
            "Followup: 12 month",
            "Followup: 24 month",
            "Followup: 60 month",
            "Date of Assessment",
            "CSM Duration",
            "Work Status",
            "mJOA 12 months",
            "HRR"
        ]
    })


def update_presplit_imaging(config: dict):
    # Isolate the pre_split_hook list
    pre_split_hooks = config['pre_split_hooks']

    # The orientation and weight of the image is redundant, as the data has been isolated already
    pre_split_hooks.append({
        "type": "drop_features_explicit",
        "features": [
            "acq",
            "weight"
        ]
    })


def update_presplit_nullity(config: dict):
    # Isolate the pre_split_hook list
    pre_split_hooks = config['pre_split_hooks']

    # Add some nullity checks as well
    pre_split_hooks.extend([{
        "type": "feature_drop_null",
        "threshold": 0.5
    }, {
        "type": "sample_drop_null",
        "threshold": 0.5
    }])


# === POST-SPLIT HOOKS === #
def update_postsplit_clinical_ohe(config: dict):
    # Isolate the post_split_hook list
    post_split_hooks = config['post_split_hooks']

    # A large number of clinical features are categorical, and need to be one-hot encoded for ML analyses to work
    post_split_hooks.extend([{
        "type": "imputation_simple",
        "strategy": "most_frequent",
        "features": [
            "EQ5D: Anxiety/Depression",
            "EQ5D: Mobility",
            "EQ5D: Pain/Discomfort",
            "EQ5D: Self-Care",
            "EQ5D: Total",
            "EQ5D: Usual Activities",
            "Sex",
            "Symptom Duration",
            "Work Status (Category)",
            "Comorbidities: Nicotine (Smoking)",
            "Comorbidities: Nicotine (Smokeless)",
            "Comorbidities: Nicotine (Patches)",
            "Comorbidities: Nicotine (Recent Quit)"
        ]}, {
        "type": "one_hot_encode",
        "features": [
            "EQ5D: Anxiety/Depression",
            "EQ5D: Mobility",
            "EQ5D: Pain/Discomfort",
            "EQ5D: Self-Care",
            "EQ5D: Usual Activities",
            "Sex",
            "Symptom Duration",
            "Work Status (Category)",
            "Comorbidities: Nicotine (Smoking)",
            "Comorbidities: Nicotine (Smokeless)",
            "Comorbidities: Nicotine (Patches)",
            "Comorbidities: Nicotine (Recent Quit)"
        ],
        "max_unique_vals": 5,
        "handle_unknown": "ignore"
    }])


def update_postsplit_fill_and_standardize(config: dict):
    # Isolate the pre_split_hook list
    post_split_hooks = config['post_split_hooks']

    # Add an imputation-by-mean for any remaining nulls, following by a standard scaler to suppress magnitude
    post_split_hooks.extend([{
        "type": "imputation_simple",
        "strategy": "mean"
    }, {
        "type": "standard_scaling",
        "run_per_cross": True
    }])


# === TABULAR FEATURE PRE-PROCESSING === #
def add_rfe_prep(config: dict):
    config['label'] += '_rfe'
    config['post_split_hooks'].append({
        "type": "recursive_feature_elimination",
        "proportion": {
            "label": "rfe_feature_proportion",
            "type": "float",
            "low": 0.1,
            "high": 0.9
        }
    })

def add_pca_prep(config: dict):
    config['label'] += '_pca'
    config['post_split_hooks'].append({
        "type":  "principal_component_analysis",
        "proportion": {
            "label": "pca_component_proportion",
            "type": "float",
            "low": 0.1,
            "high": 0.9
        }
    })


# === MAIN === #
def main(search_pattern: str, output_dir: Path, label: str, has_clinical: bool, has_imaging: bool):
    # If the dataset has neither clinical nor imaging data, is corrupted and needs to be filtered
    if not (has_clinical or has_imaging):
        raise ValueError("Requested configuration files be generated for data which has neither imaging nor clinical "
                         "data. A dataset must contain at least one set of data metrics!")

    # Run glob on the search pattern to get our list of files
    if search_pattern[0] == '/':
        # TODO: This is stupid, make it less stupid
        root_path = Path('/')
        search_pattern = search_pattern[1:]
    else:
        root_path = Path('.')
    data_paths = root_path.glob(search_pattern)

    # Raise an error if the output directory is a file
    if output_dir.is_file():
        raise ValueError("Output directory already exists as a file! Cannot save config files to destination")
    # Otherwise, if the directory doesn't already exist, make it
    elif not output_dir.exists():
        output_dir.mkdir(parents=True)

    # Generate our desired configurations files for each data path
    for p in data_paths:
        # Initialize the JSON config
        base_config = deepcopy(TEMPLATE)
        base_config['label'] = label
        base_config['data_source'] = str(p.resolve())

        # Extend the label with the name of the file
        p_name = p.name.split('.')[0]
        if label == '':
            base_config['label'] += p_name
        else:
            base_config['label'] += '_' + p_name

        # If this is a clinical dataset, add the corresponding data hooks
        if has_clinical:
            update_presplit_clinical(base_config)
            update_postsplit_clinical_ohe(base_config)
        # If this is an imaging dataset, add the corresponding data hooks
        if has_imaging:
            update_presplit_imaging(base_config)
        # Add the remaining data hooks
        update_presplit_nullity(base_config)
        update_postsplit_fill_and_standardize(base_config)

        # 5 variations of the pre-processing exist, resulting in 5 different config files
        config_variants = {}

        # No pre-processing (no-prep)
        tmp_config = deepcopy(base_config)
        tmp_config['label'] += '_noprep'
        config_variants['noprep'] = tmp_config

        # RFE only
        tmp_config = deepcopy(base_config)
        add_rfe_prep(tmp_config)
        config_variants['rfe'] = deepcopy(tmp_config)

        # RFE -> PCA
        add_pca_prep(tmp_config)
        config_variants['rfe_pca'] = deepcopy(tmp_config)

        # PCA only
        tmp_config = deepcopy(base_config)
        add_pca_prep(tmp_config)
        config_variants['pca'] = deepcopy(tmp_config)

        # PCA -> RFE
        add_rfe_prep(tmp_config)
        config_variants['pca_rfe'] = deepcopy(tmp_config)

        # Save all the resulting config files
        for k, v in config_variants.items():
            file_out = str(output_dir / v['label']) + '.json'
            with open(file_out, mode='w') as fp:
                dump(v, fp, indent=2)


if __name__ == '__main__':
    # Only parse command line arguments if we're running this script from the command line
    parser = ArgumentParser()

    parser.add_argument(
        '-s', '--search_pattern', type=str, required=True,
        help="Glob-like search pattern to use when finding the datasets to generate configurations files."
    )
    parser.add_argument(
        '-o', '--output_dir', type=Path, required=True,
        help="Where you want the resulting configuration files to be placed. "
             "The directory will be generated if it doesn't already exist"
    )
    parser.add_argument(
        '-l', '--label', type=str, required=True,
        help="The label which should be given to this set of dataset configs (before permutation labelling)."
    )
    parser.add_argument(
        '--has_clinical', action='store_true', default=False,
        help="If this flag is set, all datasets will be presumed to contain clinically-derived metrics."
    )
    parser.add_argument(
        '--has_imaging', action='store_true', default=False,
        help="If this flag is set, all datasets will be presumed to contain imaging-derived metrics."
    )

    # Parse the arguments are run our main script
    kwargs = parser.parse_args().__dict__
    main(**kwargs)