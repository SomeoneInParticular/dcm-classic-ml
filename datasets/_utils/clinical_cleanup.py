from pathlib import Path

import numpy as np
import pandas as pd

# Load the data
init_df = pd.read_csv('../raw/participants.tsv', sep='\t')
init_df = init_df.set_index('GRP')


# Reformat the mJOA columns to avoid duplications and redundancies
mjoa_cols = [
    "('mJOA', 'initial')",
    "('mJOA', '12 months')",
    "('mJOA; Total [CSA]', 'initial')",
    "('mJOA; Total [CSA]', '12 months')"
]
mjoa_df = init_df.loc[:, mjoa_cols]

# Try and fill in the mJOA initial with the values in replicated column if they are null
## Initial mJOA (pre-surgery)
missing_idx = mjoa_df.loc[:, "('mJOA', 'initial')"].isna()
mjoa_df.loc[missing_idx, "('mJOA', 'initial')"] = mjoa_df.loc[missing_idx, "('mJOA; Total [CSA]', 'initial')"]

## 1 year mJOA (post-surgery)
missing_idx = mjoa_df.loc[:, "('mJOA', '12 months')"].isna()
mjoa_df.loc[missing_idx, "('mJOA', '12 months')"] = mjoa_df.loc[missing_idx, "('mJOA; Total [CSA]', '12 months')"]

# Isolate the mJOA columns from the rest of the dataset for safekeepting
mjoa_df = mjoa_df.drop(["('mJOA; Total [CSA]', 'initial')", "('mJOA; Total [CSA]', '12 months')"], axis=1)
init_df = init_df.drop(mjoa_cols, axis=1)


# Split the dataframe into columns which were collected at multiple timepoints, and those which weren't
timeless_df = init_df.iloc[:, -20:]
timed_df = init_df.drop(timeless_df.columns, axis=1)

# As we have handled mJOA already, keep only the values which would be available pre-surgery
keep_cols = []
for c in timed_df.columns:
    if c.split(',')[1] == " 'initial')":
        keep_cols.append(c)

# Join them back into the dataset
cleaned_df = init_df.loc[:, keep_cols]
cleaned_df.loc[:, timeless_df.columns] = timeless_df

# Drop some remaining duplicated columns
cleaned_df = cleaned_df.drop(columns=["('Surgical', 'initial')", "('BMI', 'initial')"])

# Filter out any patients which were non-surgical
cleaned_df= cleaned_df.loc[cleaned_df['Surgical'] == 1, :]

# Update the column headers to no longer state the time point (as they are all the same now)
cols = [c.replace("'initial'", "") for c in cleaned_df.columns]
cleaned_df.columns = cols

# Set all EQ5D values of '4' to null (clinicians use this to represent "did not answer" for some reason)
for c in cleaned_df.columns:
    if 'EQ5D' in c:
        cleaned_df.loc[cleaned_df[c] == 4, c] = np.nan

# Fix a malformed BMI value; set it to null so imputation can handle it later
cleaned_df.loc[cleaned_df['BMI'] == 0, 'BMI'] = np.nan


# Add back in the mJOA values in preparation for HRR calculation
final_df = cleaned_df.copy()
final_df.loc[:, mjoa_df.columns] = mjoa_df

# Reformat the column labels to prevent issues during analysis
cols = [c.replace("'", "").replace(",", "").replace(" )", ")") for c in final_df.columns]
cols = [c[1:-1] if c[0] == "(" and c[-1] == ")" else c for c in cols]
final_df.columns = cols

# Calculate the Hirabayashi Recovery Ratio (HRR) for each patient
def hrr(mjoa_init, mjoa_1year):
    numerator = mjoa_1year - mjoa_init
    denominator = 18 - mjoa_init
    return numerator / denominator
hrr_vals = hrr(final_df['mJOA initial'], final_df['mJOA 12 months'])
final_df['HRR'] = hrr_vals

# Calculate the recovery class of each patient
final_df['Recovery Class'] = ['good' if v >= 0.5 else "fair" for v in hrr_vals]
final_df.loc[pd.isna(hrr_vals), 'Recovery Class'] = np.nan
final_df = final_df.dropna(subset=['Recovery Class'])

# Save the results
out_dir = Path('../cleaned/')
if not out_dir.exists():
    out_dir.mkdir()
out_path = out_dir / "../cleaned/clinical_only.tsv"
final_df.to_csv(out_path, sep='\t')
