================================================================================
README.txt
EDA_SUMMER25 - One Sample T-Test Validation Scripts
================================================================================

PROJECT OVERVIEW
----------------
This project validates that R, Python, and SAS produce identical output for a 
one-sample t-test. It generates ADaM-compliant outputs in Dataset-JSON v1.1 
formats. The workflow is designed to compare observed data to a reference mean, 
with flexible configuration for:

- alpha (significance level)
- sidedness (two-sided, upper-tailed, lower-tailed)
- dataset title
- input file and column

================================================================================
FILES
================================================================================

Markdown Files:
---------------
- 0100 One Sample T-test- Requirements Analysis.md
  Describes the statistical requirements of a t-test.

- 0100- One Sample T-Test-Design.md
  Documents the analysis design and expectations for comparing t-tests across Python, R, and SAS.

Generated Sample Input Data:
-----------
- one_sample_ttest_raw_data.csv
  Contains just patient numbers and their systolic blood pressure (SBP).

- one_sample_ttest_clinical_data.csv
  Contains an ADaM formatted version of patients and their SBPs.

Analysis Scripts:
-----------------
- ttest_python.py
  Python script performing the t-test and outputting a Dataset-JSON v1.1.

- ttest_r.R
  R script performing the t-test and outputting a Dataset-JSON v1.1.

Output Files:
-------------
- adam_bds_python.json
  Python-generated Dataset-JSON v1.1 output.

- adam_bds_python.csv
  Python-generated CSV in ADaM BDS structure.

- adam_bds_r.json
  R-generated Dataset-JSON v1.1 output.

- adam_bds_r.csv
  R-generated CSV in ADaM BDS structure.


================================================================================
PYTHON REQUIREMENTS
================================================================================

Python Version:
---------------
- Python 3.8 or higher (Python 3.12.11 was used for testing)

Python Packages:
----------------
- pandas (2.3.0 was used for testing)
- scipy (1.16.0 was used for testing)
- numpy (1.26.4 was used for testing)

To install:
------------
pip install pandas scipy numpy
-OR-
pip3 install pandas scipy numpy

================================================================================
R REQUIREMENTS
================================================================================

R Version:
----------
- R 4.0 or higher (R version 4.4.2 was used for testing)

R Packages:
-----------
- dplyr (1.1.4 was used for testing)
- readr (2.1.5 was used for testing)
- jsonlite (1.8.9 was used for testing)

To install:
------------
install.packages(c("dplyr", "readr", "jsonlite"))

================================================================================
USAGE
================================================================================

---------------------------------
PYTHON SCRIPT
---------------------------------
Usage:
------
python ttest_python.py <reference_mean> <alpha> <sidedness> <dataset_title> <input_filename> <column_name>

Arguments:
----------
reference_mean   : Numeric value to test against (e.g., 120)
alpha            : Significance level (e.g., 0.05)
sidedness        : "two", "upper", or "lower" **only these 3 options will be accepted**
dataset_title    : Descriptive label for the output dataset json
input_filename   : CSV file with input data to be analyzed (must be in the same directory as your Python script)
column_name      : Column in CSV to analyze and run t-test on

Example:
--------
python ttest_python.py 120 0.05 two "SBP T-Test" one_sample_ttest_raw_data.csv SBP


---------------------------------
R SCRIPT
---------------------------------
Usage:
------
Rscript ttest_r.R <reference_mean> <alpha> <sidedness> <dataset_title> <input_filename> <column_name>

Arguments:
----------
reference_mean   : Numeric value to test against (e.g., 120)
alpha            : Significance level (e.g., 0.05)
sidedness        : "two", "upper", or "lower" **only these 3 options will be accepted**
dataset_title    : Descriptive label for the output dataset json
input_filename   : CSV file with data to be analyzed (must be in the same directory as your R script)
column_name      : Column in CSV to analyze and run t-test on

Example:
--------
Rscript ttest_r.R 120 0.05 upper "SBP Upper-tailed Test" one_sample_ttest_clinical_data.csv SBP

================================================================================
OUTPUT
================================================================================

Both scripts will create:

- JSON output: adam_bds_[language].json
  (Dataset-JSON v1.1 format)

- CSV output: adam_bds_[language].csv
  (ADaM BDS format)

These outputs include:
- Mean
- SD
- Standard Error
- Degrees of Freedom
- t-Statistic
- p-Value
- Confidence Interval (based on sidedness)

================================================================================
NOTES
================================================================================

- Always verify column names in your input CSV.
- For reproducibility, ensure you use the same alpha and sidedness in both scripts.
- For validation, you can compare the Python, R, and SAS outputs side by side.

================================================================================
