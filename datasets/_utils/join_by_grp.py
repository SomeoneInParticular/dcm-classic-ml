from argparse import ArgumentParser
from pathlib import Path

import pandas as pd


def main(input_1, input_2, output):
    # Load the files
    df1 = pd.read_csv(input_1, sep='\t')
    df1 = df1.set_index('GRP')
    df2 = pd.read_csv(input_2, sep='\t')
    df2 = df2.set_index('GRP')

    # If 'Recovery Class' is in both dataframe's already (it was run through 'update_imaging_with_clinical.py')
    # remove one copy to avoid an error
    if 'Recovery Class' in df1.columns and 'Recovery Class' in df2.columns:
        df2 = df2.drop(columns=['Recovery Class'])

    # Join them on the patient's ID
    df_out = df1.join(df2, how='inner')

    # Save the result
    df_out.to_csv(output, sep='\t')


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument(
        '-i1', '--input_1', required=True, type=Path,
        help="The first (cleaned) data file to used. Assumes TSV format."
    )
    parser.add_argument(
        '-i2', '--input_2', required=True, type=Path,
        help="The second (cleaned) data file to used. Assumes TSV format."
    )
    parser.add_argument(
        '-o', '--output', required=True, type=Path,
        help="Where to place the result. Output in TSV format."
    )

    kwargs = parser.parse_args().__dict__
    main(**kwargs)
