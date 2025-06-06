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

# Input Dataset 
Select or synthesize input dataset 

# Agreement Criteria 
T statistic and p-value should have an absolute difference of <0.000001 across R, SAS, and Python for numeric agreement. 

# Expectations for Supported Statistics
R, SAS, and Python should output consistent values for: 
- Confidence Interval (abs diff < 0.0001)
- Degrees of Freedom (should be the exact same across all outputs)
- Mean (abs diff < 0.0001)
- Standard Error (abs diff < 0.0001)
- Agreement w/null hypothesis (should be the exact same across all outputs)

# Function Usage and Critical Arguments 
- **R**: use `t.test` with args `x`, `mu`, `alternative`, `paired = False`, and `conf.level` specified 
    - note that `paired = False` should be set as we are only focusing on one sample t-tests not paired t-tests
- **SAS**: use `PROC TTEST` with args `DATA=`, `VAR=`, `H0=`, `SIDES=`, `ALPHA=`, and `DIST= normal` specified
    - note that `DIST= normal` should be specified as one sample t-tests assume approximately normally distributed data
- **Python**: use `scipy.stats.ttest_1samp` with args `a`, `popmean`, `alternative`, and `confidence_level` specified 

In R, SAS, and Python the dataset, null hypothesis, whether it is a two-sided test or not, and the confidence level should be specified to ensure numeric agreement across all functions. 

# Known Incompatibilities 
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

# Comparison Protocol and Metrics 
Outline comparison protocol and metrics

# Design Notes and Dataset 
Upload design notes and dataset

# References 
- Requirements Analysis for One Sample T-Test: https://github.com/isabelkhan/eda_summer25/blob/main/0100%20One%20Sample%20T-test-%20Requirements%20Analysis.md#inputs 
