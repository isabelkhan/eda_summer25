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
- R & Python don't support useage of lognormal data, however t-tests generally assume normal distribution of data 
- 

# Comparison Protocol and Metrics 
Outline comparison protocol and metrics

# Design Notes and Dataset 
Upload design notes and dataset

# References 
