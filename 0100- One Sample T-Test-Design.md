# [0100] One Sample T-Test - Design
This following details the design plan for assessing the consistency and accuracy of One Sample T-test implementations across R, SAS, and Python. Each section specifies input parameters, statistical agreement criteria, expected results, and known tool-specific limitations.

---
# Table of Contents 
- [0100 One Sample T-Test - Design](#0100-One-Sample-TTest---Design)
- [Input Dataset](#input-dataset)
- [Agreement Criteria](#agreement-criteria)
- [Expectations for Supported Statistics](#expectations-for-supported-statistics)
- [Function Usage and Critical Arguments](#function-usage-and-critical-arguments)
- [Known Incompatibilities](#known-incompatibilities)
- [Comparison Protocol and Metrics](#comparison-protocol-and-metrics)
- [Design Notes and Dataset](#design-notes-and-dataset)
- [References](#references)

---

# 1. Input Dataset 

**Disclaimer:** The dataset used in this study is fictional. The subject IDs and blood pressure measurements are not associated with any real study. Any similarity within this dataset to any actual people is purely coincidental.

**Dataset Hypothetical Scenario:** Clinical trial collecting systolic blood pressure (SBP) measurements for 50 patients. Goal is to verify whether the average SBP differs significantly from a population value (e.g., 120 mmHg).

**Sample Code to Generate Raw Dataset:**

```Python
import numpy as np
import pandas as pd

# set a seed for reproducibility
np.random.seed(42)

# parameters for synthetic data
num_patients = 50            # number of patients
true_mean_sbp = 121          # simulated average SBP (mmHg)
std_dev_sbp = 5              # standard deviation of SBP

# generate synthetic SBP values
sbp_values = np.random.normal(loc=true_mean_sbp, scale=std_dev_sbp, size=num_patients).round(1)

# create patient IDs (CAMIS-PT-001 to CAMIS-PT-050)
patient_ids = [f"CAMIS-PT-{i:03}" for i in range(1, num_patients + 1)]

# construct the raw dataset
raw_df = pd.DataFrame({
    "USUBJID": patient_ids,
    "SBP": sbp_values
})

# preview the data
print(raw_df.head())

# save to CSV
raw_df.to_csv("one_sample_ttest_raw_data.csv", index=False)

```

How To Run One Sample T-Tests In: 
- Python: `scipy.stats.ttest_1samp(df["SBP"], popmean=120)`
- R: `t.test(df$AVAL, mu = 120)`
- SAS: `PROC TTEST DATA=read H0=120; VAR AVAL; RUN;`

# 2. Agreement Criteria 
T statistic and p-value should have an absolute difference of <0.000001 across R, SAS, and Python for numeric agreement. 

**Justification:** An absolute difference threshold of 1e-6 was selected to allow for minor computational differences in floating-point arithmetic and algorithm implementations across platforms while still ensuring statistical equivalence.

# 3. Expectations for Supported Statistics
R, SAS, and Python should output consistent values for: 
- Confidence Interval (abs diff < 0.000001)
- Degrees of Freedom (should be the exact same across all outputs)
- Mean (abs diff < 0.000001)
- Standard Error (abs diff < 0.000001)
- Agreement w/null hypothesis (should be the exact same across all outputs)

**Reasoning:**
- There is no official SAS-stated threshold, but user-space discussions acknowledge and utilize numerical tolerance.
- In regulated pharma validation, tolerances of ~1e-6 are common benchmarks used in SOPs to assess parity between software outputs.

# 4. Function Usage and Critical Arguments 
- **R**: use `t.test` with args `x`, `mu`, `alternative`, `paired = False`, and `conf.level` specified 
    - note that `paired = False` should be set as we are only focusing on one sample t-tests not paired t-tests
- **SAS**: use `PROC TTEST` with args `DATA=`, `VAR=`, `H0=`, `SIDES=`, `ALPHA=`, and `DIST= normal` specified
    - note that `DIST= normal` should be specified as one sample t-tests assume approximately normally distributed data
- **Python**: use `scipy.stats.ttest_1samp` with args `a`, `popmean`, `alternative`, and `confidence_level` specified 

In R, SAS, and Python the dataset, null hypothesis, whether it is a two-sided test or not, and the confidence level should be specified to ensure numeric agreement across all functions. 

# 5. Known Incompatibilities 
- R & Python don't support useage of lognormal data, however t-tests generally assume normal distribution of data so there is no need to test on lognormal data distributions 
- For NaNs (Non numbers): 
    - SAS automatically excludes missing data
    - R defaults to `getOption("na.action")` where `na.action` is a globally defined variable that dictates how to handle missing values (which might be defined differently than omitting missing data)
    - Python defaults `nan_policy` to `propagate` where corresponding entry of output will be a `NaN`
- Inputs: 
    - R takes vectors as an input 
    - SAS expects datasets or variables specified in PROC 
    - Python works on numpy arrays/lists 
- Outputs:
    - R returns the statistic, p-value, and CI 
    - SAS produces detailed tables 
    - Python outputs the statistic, p-value, and CI (with aux functions)
- Handling zero variance: 
    - R: produces warning or `NaN` 
    - SAS: produces error 
    - Python: produces `NaN` or raises warning 

**Summary:** Formatting might not align perfectly, inputs may need to be manipulated slightly for each language and outputs won't be identical but should produce the same numeric values as long as how to handle `NaNs` and zero variances are specified (additionally null hypothesis, one-sided tests, and confidence level should be specified the same across all languages if they are not default values).  

# 6. Comparison Protocol and Metrics 
Compare input and output formatting across R, Python, and SAS and note differences. Compare the numeric output values of the statistic, p-value, CI, degrees of freedom, mean, and standard error across R, Python, and SAS and note if they are greater than the absolute difference thershold specified in parts 2 & 3 of the design outline. 

# 7. Design Notes and Dataset 
[one_sample_ttest_raw_data.csv](./one_sample_ttest_raw_data.csv) 

# 8. References 
- Requirements Analysis for One Sample T-Test: https://github.com/isabelkhan/eda_summer25/blob/main/0100%20One%20Sample%20T-test-%20Requirements%20Analysis.md#inputs 
- Public Discussion about Tolerance Checks: https://communities.sas.com/t5/SAS-Programming/How-to-check-variables-for-equality-within-tolerance-niether/td-p/234678?utm_source=chatgpt.com 
