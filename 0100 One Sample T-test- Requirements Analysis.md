
# [0100] One Sample T-Test - Requirements Analysis

---

- [0100 - OneSampleTTest - Requirements Analysis](#0100---OneSampleTTest---Requirements-Analysis)
- [Background](#background)
  - [Hypotheses](#hypotheses)
  - [Assumptions](#assumptions)
  - [Results](#results)
    - [Test Statistic & P-value](#test-statistic--p-value)
- [Package Implementations](#package-implementations)
  - [SAS (TTEST)](#sas-ttest)
    - [Function/Procedure (SAS)](#functionprocedure-SAS)
    - [Inputs (SAS)](#inputs-SAS)
    - [Outputs (SAS)](#outputs-SAS)
    - [Sample Code (SAS)](#sample-code-SAS)
    - [Limitations/Notes (SAS)](#limitationsnotes-SAS)
  - [R (stats)](#r-stats)
    - [Function/Procedure (R)](#functionprocedure-R)
    - [Inputs (R)](#inputs-R)
    - [Outputs (R)](#outputs-R)
    - [Sample Code (R)](#sample-code-R)
    - [Limitations/Notes (R)](#limitationsnotes-R)
  - [Python (scipy.stats)](#python-scipystats)
    - [Function/Procedure (Python)](#functionprocedure-Python)
    - [Inputs (Python)](#inputs-Python)
    - [Outputs (Python)](#outputs-python)
    - [Sample Code (Python)](#sample-code-python)
    - [Limitations/Notes (Python)](#limitationsnotes-python)
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
- Data is independent and identically distributed (**i.i.d**)
- Underlying population is approximately **normally distributed** 
- Variable is measured on a **continous** scale 

## Results 

### Test Statistic & P-value
**T statistic**: 

t = (μ - μ<sub>0</sub>)/(s/√n)
where 
-  μ: sample mean 
- μ<sub>0</sub>: hypothesized population mean 
- s: sample standard deviation 
- n: sample size 

All t-statistics follow a t-distribution with n-1 degrees of freedom
(you can lookup the p-value using the t-statistic and degrees of freedom in a **t-distribution table**)

# Package Implementations

## SAS (TTEST)

### Function/Procedure (SAS) 
Use `PROC TTEST` function from `STAT` module. 

### Inputs (SAS)
- **Required**: 
    - `DATA=` (name of dataset)
    - `VAR=` (variable name for t-test)
    - `H0=` (null hypothesis)
    - `SIDES=` (`2`, `U`, or `L` indicates two-sided vs. one-sided test) 
    - `ALPHA=` (significance level)
    - `DIST= normal` (specifies normal v. lognormal data)
- **Optional**: 
    - `ORDER=`(determines sort order of CLASS or CROSSOVER variable) 
    - `TEST=`(specifies test criterion)
    - `TOST=`(requests equivalence test and specifies bounds)
    - `CI=`(requests CI for st dev or coeff of variation)
    - `COCHRAN=`(requests Cochran t-test)
    - `PLOT=`(produces ODS statistical graphics)
    - `BYVAR=`(groups results by variables specified in PAIRED or VAR)
    - `NOBYVAR=` (groups results by tables)

### Outputs (SAS)
- T-statistic 
- P-value 
- Confidence Interval 
- Degrees of Freedom
- Mean 
- Min & max
- Std. Deviation
- SE (std error) 
- For lognormal data: coefficient of variation


### Sample Code (SAS)

```sas
*data;
data read;
    input score count @@;
    datalines;
40 2   47 2   52 2   26 1   19 2
25 2   35 4   39 1   26 1   48 1
14 2   22 1   42 1   34 2   33 2
18 1   15 1   29 1   41 2   44 1
51 1   43 1   27 2   46 2   28 1
49 1   31 1   28 1   54 1   45 1
;

*perform t-test;
proc ttest data=read h0=30;
     var score;
run;
```

### Limitations/Notes (SAS)
- Null hypothesis defaults to `0` 
- Alternative hypothesis is two-sided by default (`SIDES = 2`)
- Automatically excludes missing data 
- Alpha is `0.05` by default for 95% CI
- `DIST=` should be set to `normal`

---
## R (stats)

### Function/Procedure (R)
Use `t.test` from base R `stats` package. 

### Inputs (R)
- **Required**: 
    - `x` (numeric vector of data)
    - `mu` (hypothesized mean)
    - `alternative` (`two-sided`, `less`, or `greater` specifies one-sided v two-sided test)
    - `paired = False` (logical indicating if you want a paired t-test)
    - `conf.level` (confidence level)
- **Optional**: 
    - `y` (optional non-empty numerical vector of data values)
    - `var.equal` (logical indicating whether to treat two variances as equal)
    - `formula` ( a formula of the form lhs ~ rhs where lhs is a numeric variable giving the data values and rhs a factor with two levels giving the corresponding groups)
    - `data` (an optional matrix or data frame containing the variables in the formula)
    - `subset` (an optional vector specifying a subset of observations to be used)
    - `na.action` (a function which indicates what should happen when the data contain NAs)
    - `na.rm` (`True`/`False` True instructs functions to remove missing values)

### Outputs (R)
- T-statistic
- Degrees of freedom 
- P-value 
- Confidence Interval 
- Estimated mean
- Null.value (specified hypothesized value of the mean)
- Std error (standard error of the mean (difference), used as denominator in the t-statistic formula)
- Alternative (a character string describing the alternative hypothesis) 
- method(a character string indicating what type of t-test was performed)
- data.name (character string giving the name(s) of the data)


### Sample Code (R)
```r
# Create sample data
read <- tibble::tribble(
  ~score, ~count,
  40, 2,   47, 2,   52, 2,   26, 1,   19, 2,
  25, 2,   35, 4,   39, 1,   26, 1,   48, 1,
  14, 2,   22, 1,   42, 1,   34, 2 ,  33, 2,
  18, 1,   15, 1,   29, 1,   41, 2,   44, 1,
  51, 1,   43, 1,   27, 2,   46, 2,   28, 1,
  49, 1,   31, 1,   28, 1,   54, 1,   45, 1
)

#perform t-test
t.test(read$score, mu = 30)
```

### Limitations/Notes (R)
- Null hypothesis/hypothesized mean (mu) defaults to `0` 
- Alternative hypothesis is `two.sided` by default 
- Confidence level is `0.95` by default 
- `paired` should be set to `False`

---
## Python (scipy.stats)

### Function/Procedure (Python)
Use `scipy.stats.ttest_1samp` from `scipy` package 

### Inputs (Python)
- **Required**: 
    - `a` (sample data array)
    - `popmean` (population mean to test against)
    - `alternative` (`two-sided`, `less`, or `greater` for two-sided v. one-sided tests)
- **Optional**: 
    - `axis` (axis to compute along(row v. column of data))
    - `nan_policy` (how to handle NaN (‘propagate’, ‘omit’ or ‘raise’))
    - `keepdims` (if `True`, axes which are reduced are left in the result as dimensions with size one, the result will broadcast correctly against input array)

### Outputs (Python)
- T-statistic 
- P-value 
- Degrees of freedom 
- Confidence interval 


### Sample Code (Python)
```python
import pandas as pd
from scipy import stats

# Create sample data
data = {
    'score': [40, 47, 52, 26, 19, 25, 35, 39, 26, 48, 14, 22, 42, 34, 33, 18, 15, 29, 41, 44, 51, 43, 27, 46, 28, 49, 31, 28, 54, 45],
    'count': [2, 2, 2, 1, 2, 2, 4, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1]
}

df = pd.DataFrame(data)

# Perform one-sample t-test
sample_mean = df['score'].mean()
null_mean = 30  # Hypothetical null hypothesis mean for comparison
alpha = 0.05  # Significance level

#getting t statistic & p-value 
result = stats.ttest_1samp(df['score'], null_mean)
t_statistic, p_value = result 
confidence_interval= result.confidence_interval(confidence_level = 0.95)

#formatting printed output 
print(f"t: {t_statistic}")
print(f"p-value: {p_value}")
print(f"mean of x: {sample_mean}")

if p_value < alpha:
    print("Reject null hypothesis: There is a significant difference.")
else:
    print("Fail to reject null hypothesis: There is no significant difference.")
```

### Limitations/Notes (Python)
- Population mean **must be specified** (if array_like, then its length along axis must equal 1, and it must otherwise be broadcastable with a)
- Alternative hypothesis is `two-sided` by default 
- Confidence level is `0.95` by default (alpha = 0.05)
- Axis defaults to `0`
- Keepdims defaults to `False`

---

# Summary
- Data must be approximately normally distributed 
- Null and alterntive hypotheses must be specified the same acoss R, SAS, and Python to produce the same output 
- Confidence levels must also be specified the same way across R, SAS, and Python to produce the same output 
- Data should be measured on a continous scale and be independent and identically distributed

# References
- CAMIS Project: https://psiaims.github.io/CAMIS/
- R `t.test` Documentation: https://www.rdocumentation.org/packages/stats/versions/3.6.2/topics/t.test 
- SAS `PROC TTEST` Documentation: https://documentation.sas.com/doc/en/statug/15.2/statug_ttest_syntax01.htm 
- Python `scipy.stats.ttest_1samp` Documentation: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_1samp.html 
