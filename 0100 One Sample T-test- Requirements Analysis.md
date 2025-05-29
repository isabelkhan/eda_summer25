
# [0100] One Sample T-Test - Requirements Analysis

---

- [0100 - OneSampleTTest - Requirements Analysis](#0100---OneSampleTTest---Requirements-Analysis)
- [Background](#background)
  - [Hypotheses](#hypotheses)
  - [Assumptions](#assumptions)
  - [Test Statistic & P-value](#test-statistic--p-value)
- [Package Implementations](#package-implementations)
  - [SAS (TTEST)](#sas-ttest)
    - [Function / Procedure](#function--procedure)
    - [Inputs](#inputs)
    - [Outputs](#outputs)
    - [Sample Code](#sample-code)
    - [Limitations / Notes](#limitations--notes)
  - [R (stats)](#r-stats)
    - [Function / Procedure](#function--procedure)
    - [Inputs](#inputs)
    - [Outputs](#outputs)
    - [Sample Code](#sample-code)
    - [Limitations / Notes](#limitations--notes)
  - [Python (scipy.stats)](#python-scipystats)
    - [Function / Procedure](#function--procedure)
    - [Inputs](#inputs)
    - [Outputs](#outputs)
    - [Sample Code](#sample-code)
    - [Limitations / Notes](#limitations--notes)
- [Summary](#summary)
- [References](#references)


---

# Background

A one-sample t-test is a statistical method used to determine whether the **mean of a single sample significantly differs from a known or hypothesized population mean**. 

This test is useful when the standard deviation of the population is unknown and when the sample size is small to moderate (<30).

A one-sample t-test can be used in clinical trial data to compare a sample mean (from trial participants) against a known or hypothesized population value, such as a standard, target, or baseline value. This is especially useful when:

- You’re evaluating whether a treatment shifts a biomarker or measurement away from a clinically meaningful value.
- You have only one group (e.g., no control group, or a single-arm study).
- You’re checking if the observed mean effect significantly differs from a known comparator (like a regulatory threshold or historical average).


## Hypotheses

Let μ<sub>0</sub> denote the **hypothesized population mean**. 
- Null Hypothesis (H<sub>0</sub>): the sample mean (μ) is equal to the hypothesized population mean (μ = μ<sub>0</sub>)
- Alternative Hypothesis (H<sub>A</sub>): the sample mean (μ) is **EITHER** not equal to the hypothesized population mean (μ ≠ μ<sub>0</sub>)[^1] **OR** greater/less than the hypothesized population mean (μ > μ<sub>0</sub>) OR (μ < μ<sub>0</sub>)[^2]

[^1]: this is called a one-sided t-test 
[^2]: this is called a two-sided t-test


## Assumptions
- data is independent and identically distributed (**i.i.d**)
- underlying population is approximately **normally distributed** 
- variable is measured on a **continous** scale 

## Test Statistic & P-value
**T statistic**: 

t = (μ - μ<sub>0</sub>)/(s/√n)
where 
-  μ: sample mean 
- μ<sub>0</sub>: hypothesized population mean 
- s: sample standard deviation 
- n: sample size 

all t-statistics follow a t-distribution with n-1 degrees of freedom
(you can lookup the p-value using the t-statistic and degrees of freedom in a **t-distribution table**)

# Package Implementations

## SAS (TTEST)

### Function/Procedure 
Use `PROC TTEST` function from `STAT` module. 

### Inputs 
- **Required**: `DATA=`, `VAR=`, `H0=`, `SIDES=`, `ALPHA=`, `DIST= normal`
- **Optional**: `ORDER=`, `TEST=`, `TOST=`, `CI=`, `COCHRAN=`, `PLOT=`, `BYVAR=`, `NOBYVAR=`

### Outputs
- T-statistic 
- P-value 
- Confidence Interval 
- Degrees of Freedom
- Mean 
- Min & max
- Std. Deviation
- SE (std error) 
- For lognormal data: coefficient of variation


### Sample Code

```sas
proc ttest data=read h0=30;
     var score;
  run;
```

### Limitations/Notes

---
## R (stats)

### Function/Procedure 
[Insert function or procedure used.]

### Inputs 

### Outputs

### Sample Code

### Limitations/Notes

---
## Python (scipy.stats)

### Function/Procedure 
[Insert function or procedure used.]

### Inputs 

### Outputs

### Sample Code

### Limitations/Notes

---

# Summary

# References