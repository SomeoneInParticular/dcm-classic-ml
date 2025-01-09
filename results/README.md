# Results Interpretation

## Running `result_analysis.ipynb`

1. Install Pandas, Seaborn, and Matplotlib, if you have not already done so
2. Run the full analysis as described in `dcm-classic-ml/README.md` on a valid BIDS dataset. 
   * The notebook assumes the resulting database is named `results.db`, and is placed in the directory above this one (where our study generated it). If your output not here, either move it here or edit the `result_analysis.ipynb` to load from the new location prior to step 4.
3. Install and run Jupyter Notebook or Jupyter Lab within this directory (see [here](https://docs.jupyter.org/en/latest/install.html) for how to do this)
4. Run all cells in `result_analysis.ipynb`; this can take a few minutes, as there are a large number of plots being generated (all of which are saved in the `figures/` directory).

## Result filtering

As the study design is a 10-replicate, 10-fold, 100-trial one, any studies which did not complete the full 10,000 trials were dropped. At present, due to the large number of analytical permutations, this means 625 total studies are available.

# Metric Distributions

All metrics were based on our study's dataset; if you are running this on a different dataset, the results are almost certain to change!

## mJOA

## Pre-Surgery

Distribution was roughly normal, with the largest proportion of patients (131/292) having moderate severity DCM prior to surgical treatment. Once the notebook has been run, a histogram plot of this can be found at `figures/mjoa_dist/pre_treatment_mjoa.svg`.

## Post-Surgery

As would be expected, the average mJOA score post-surgery was substantially better, with the majority of patients (163/292) now having mild DCM after surgical treatment. Once the notebook has been run, a histogram plot of this can be found at `figures/mjoa_dist/post_treatment_mjoa.svg`.

## Improvement Distributions

Likewise, the majority of patients (214/292) saw some improvement in their condition (defined as their post-surgical mJOA exceeding their pre-surgical mJOA by any amount), as shown below. Once the notebook has been run, a histogram plot of this can be found at `figures/mjoa_dist/treatment_mjoa_delta.svg`.

However, whether patients saw significant improvement in their condition (as defined by a Hirabayashi Recovery Ratio (HRR) of 0.5 of greater, see figure below), the majority is much closer, with only 53% of patients doing so. The Kernel Density Estimates of this metric, stratified by the DCM severity of the patient pre-surgery, can be found at `figures/mjoa_dist/hirabayashi_ratios.svg` after the notebook has been run.

## Demographics

### Age

As would be expected, the vast majority of patients in this study were older than 40. A histogram of the overall distribution can be found at `figures/demo_dist/age_dist.svg` after the notebook has been run.

### Sex

The majority of patients (60.62%) were male, with all others being female. A pie chart of the ratio can be found at `figures/demo_dist/sex_dist.svg` after the notebook has been run.

### Body Mass Index (BMI)

Most patients had a BMI equal to or greater than 25, which indicates they were overweight or obese. A histogram of the overall distribution can be found at `figures/demo_dist/bmi_dist.svg` after the notebook has been run.

### Symptom Duration

Most (63.71%) of the patients in our dataset had symptoms for more than 2 years before receiving surgical treatment. A pie chart of the ratio can be found at `figures/demo_dist/symptom_duration_dist.svg` after the notebook has been run.

### Work status

Most patients were either actively working (labelled as `W`) or were retired, self-employed, or working-from-home (together labelled as `HSR`). Only 21.58% of patients in our dataset were not actively employed or retired in some form. A pie chart of the ratio can be found at `figures/demo_dist/work_status_(category)_dist.svg` after the notebook has been run.

# Performance by Trial

## Balanced Accuracy

The graphs placed within `figures/bacc_performance` were designed to help tease out any trends in performance across Optuna trials for various analytical protocols in the study. These plots are stratified in two major ways

1. **_Protocol Variant:_**
   * `dataset`: Plot stratified by what set of features were used during model training 
     * `img`: Imaging only
     * `clinical`: Clinical metrics only
     * `full`: Both clinical and imaging metrics used
   * `ori`: The orientation of the imaging metrics used, if they were used.
     * `axial`: Axially-oriented MRI sequences.
     * `sag`: Sagittally-oriented MRI sequences.
     * `none`: No imaging metrics used (clinical-only)
     * **NOTE:** For our purposes, 3d images are marked as `axial` as, in our dataset, the handful of 3d images we had had a higher axial resolution than sagittal.
   * `weight`: The imaging weight (or contrast) used
     * `T1w`: T1-weighted (high contrast between fatty and hydrous tissue)
     * `T2w`: T2-weighted (high contrast liquids and solid mass)
     * `none`: No imaging metrics used (clinical-only)
   * `model`: The Machine-Learning model being tested
     * `AdaBoostClassifier`: AdaBoosted Classifiers, each composed of a tuned chain of Decision Trees with tuned parameters.
     * `RandomForestClassifier`: Random Forest Classifiers, each consisting of a tuned bundle of Decision Trees with tuned parameters.
     * `KNNC`: K-Nearest Neighbor Classifiers, tested with various numbers of neighbors and regularization.
     * `SupportVectorClassifier`: Support Vector Machines, tested with various kernels.
     * `LogisticRegression`: Logistic Regressions, testing with various forms and degrees of regularization. 
2. **_Metric Assessed:_**
   * **Balanced Accuracy (Average Test)**: The average performance on the testing dataset at each trial point.
   * **Balanced Accuracy (Test @ Peak Validate)**: The model's average performance on the testing set across replicates, sampled by selecting the analysis permutation with the highest performance on the validation set.
   * **Balanced Accuracy (Test weighted by Validate)**: The model's performance on the testing set weighted average using the performance on the validation set as the weighted.

# Statistical Analyses

## Paired Ranked Sum

This statistical test will identify whether one group of samples, defined as all samples for which a given analytical variant was used, outperforms another by a significant margin. This is accomplished via a one-tailed ranked-sum test, chosen over the classic T-test as the distribution of some groupings were not normally distributed. Whether a given grouping was significantly better than another was based on p-value of 0.05, with Bonferroni and Benjaminini-Yekutieli multiple comparisons measure correction applied to supress the possibility false positives.

## Kruskal-Wallace

This statistical tests aims to identify whether there is any significant difference in performance at all between a set of groups. This is done with a two-tailed Kruskal-Wallace test, chosen over ANOVA as we do not meet its normality assumption requirement in all sample groupings. Whether this difference was significant was based on p-value of 0.05, with Bonferroni multiple comparisons measure correction applied to supress the possibility false positives.

# Results Summary

## Testing at Peak Validation

When allowing for ties in performance:

* When selecting testing performance at peak validation (i.e. the model most likely to be selected based on human intuition), the following was observed:
  * RFE feature pre-processing applied without PCA out performances most of its alternatives, with no feature pre-processing being the next best choice.
  * Model's trained on axially oriented MRI sequences outperform those trained on sagittally oriented ones. Likewise, using T2-weighted MRI sequences provides a significant performance boost over using T1-weighted sequences.
  * Using both clinical and imaging metrics together results in better performance than using one or the other subset alone.
  * Using the DeepSeg algorithm (binary segmentation) to process the MRI sequences provides a significant performance boost over using the SoftSeg algorithm (non-binary segmentation).
  * Analyses using Logistic Regression outperformed those trained on every other model type tested, with Random Forest Classifiers being the runner-up
  * Kruskal-Wallace showed that all variable elements of the analysis had results which differed significantly from each other, even if they were not significantly better or worse as measured by the prior paired rank-sum test.
* When selecting testing performance at the optimal objective function value (i.e. the model most likely to be selected based on Optuna's internal selection criterion), the following was observed:
  * RFE used without PCA continues to outperform alternatives by a significant margin
  * Models trained on axially oriented MRI sequences continue to outperform those trained on sagittally oriented ones. 
  * Models trained on T2-weighted MRI sequences continue to outperform those trained on T1-weighted sequences.
  * Using the full dataset only provides a significant performance boost over using imaging alone, with the performance difference between clinical and full no longer being significant
  * Models using DeepSeg-derived metrics continue to outperform those trained using SoftSeg-derived metrics
  * Logistic Regression based analyses outperform only KNN and AdaBoost based models, and are no longer the clear choice above all others
  * No change in Kruskal-Wallace, though the segmentation algorithm is less significant than before

When filtering out entries which have a very large proportion of ties (likely indicating overfitting during training, with ties of 100% balanced accuracy at validation being common)

* When selecting testing performance at peak validation (i.e. the model most likely to be selected based on human intuition), the following differences from prior were observed:
  * Logistic Regression no longer outperforms every other model type by a significant margin
  * DeepSeg-derived imaging metrics do not provide as significant a boost to performance over SoftSeg as they did prior
  * Using the full dataset only provides a significant performance boost over using imaging alone, with the performance difference between clinical and full no longer being significant.
* No ties occurred when using "objective" as the other class, making the results identical to the analyses detailed in the previous section

## Testing at Peak Objective

In contrast to the prior analysis, the choice of ML model was by far the most significant effect, with the only non-ML related performance difference which was found to be significant being model's trained on the full dataset outperforming those trained on imaging data alone. This was confirmed by Kruskal-Wallace analysis, where only the choice of ML model and dataset were found to significantly change the performance of the analysis.

No ties were observed in this context, making the results between high tie-excluded and tie-inclusive filters identical 

## Feature Importance

### Permutation Based

The 10 most impactful features, on average, for models with both clinical and imaging-derived features were:

1. Age
2. mJOA (Initial Pre-Surgery)
3. Mean Cross-Sectional Area of Spinal Cord at Vertebra 2
4. Body Mass Index
5. Orientation of Spinal Cord at Vertebra 3
6. Mean Cross-Sectional Area of Spinal Cord at Vertebra 3
7. Standard Deviation of Eccentricity of Spinal Cord at Vertebra 5
8. Average Eccentricity of Spinal Cord at Vertebra 4
9. Mean AP Diameter of Spinal Cord at Vertebra 2
10. Standard Deviation of RL Angle of Spinal Cord at Vertebra 4

