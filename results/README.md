# Results Interpretation

## Running `result_analysis.ipynb`

1. Install Pandas, Seaborn, and Matplotlib, if you have not already done so
2. Run the full analysis as described in `dcm-classic-ml/README.md` on a valid BIDS dataset. 
   * The notebook assumes the resulting database is named `results.db`, and is placed in the same directory as `result_analysis.ipynb`. If your output is not here, either move it here or edit the `result_analysis.ipynb` to load from the new location prior to proceeding.
3. Install and run Jupyter Notebook or Jupyter Lab within this directory (see [here](https://docs.jupyter.org/en/latest/install.html) for how to do this)
4. Run all cells in `result_analysis.ipynb`; this can take a few minutes, as (depending on the analyses you ran) there is a large amount of data to analyzed and a large number of plots to generate (the latter of which are saved in the `figures/` directory).

## Implicit Result Filtering

As the study design is a 10-replicate, 10-fold, 100-trial one, any studies which did not complete the full 10,000 trials are dropped. This will likely only occur if the run in terminated prematurely (either manually, or due to "timeout" on an HPC).

