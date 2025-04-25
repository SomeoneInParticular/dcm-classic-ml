from argparse import ArgumentParser
from pathlib import Path

import pandas as pd


def main(clinical_data: Path, image_data: Path):
    # Try to import both files into memory
    clinical_df = pd.read_csv(clinical_data, sep='\t', index_col='GRP')
    image_df = pd.read_csv(image_data, sep='\t', index_col='GRP')

    # Filter the imaging dataframe to include only the sequences present in the clinical one
    to_drop = set(image_df.index) - set(clinical_df.index)
    image_df = image_df.drop(index=list(to_drop))

    # Add the Recovery Class to the imaging dataset
    image_df['Recovery Class'] = clinical_df['Recovery Class']

    # Update the imaging dataframe with the new data
    image_df.to_csv(image_data, sep='\t')


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument(
        '-c', '--clinical_data', required=True, type=Path,
        help="The clinical dataset to check against; only the patients present in this dataset will be kept!. "
             "Should be in '.tsv' format"
    )
    parser.add_argument(
        '-i', '--image_data', required=True, type=Path,
        help="The imaging dataset to filter; this will OVERRIDE the file, so be careful!. "
             "Should be in '.tsv' format"
    )

    kwargs = parser.parse_args().__dict__

    main(**kwargs)