import sys
import json
import pandas as pd
from scipy import stats
from datetime import datetime
import numpy as np

# Usage message
usage_msg = (
    "Usage:\n"
    "  python test_python.py <reference_mean> <alpha> <sidedness> <dataset_title> <input_filename>\n\n"
    "Arguments:\n"
    "  reference_mean: numeric target mean\n"
    "  alpha: significance level (e.g., 0.05)\n"
    "  sidedness: 'one' or 'two'\n"
    "  dataset_title: quoted string label\n"
    "  input_filename: CSV file with data\n"
)

# Check arguments
if len(sys.argv) != 6:
    print(usage_msg)
    sys.exit(1)

# Parse arguments
try:
    ref_mean = float(sys.argv[1])
except ValueError:
    print("Error: reference_mean must be numeric.")
    sys.exit(1)

try:
    alpha = float(sys.argv[2])
    if not (0 < alpha < 1):
        raise ValueError
except ValueError:
    print("Error: alpha must be a number between 0 and 1.")
    sys.exit(1)

sidedness = sys.argv[3].lower()
if sidedness not in ["one", "two"]:
    print("Error: sidedness must be 'one' or 'two'.")
    sys.exit(1)

dataset_title = sys.argv[4]
input_filename = sys.argv[5]

# Load the data
df = pd.read_csv(input_filename)

# Analysis date
analysis_date = datetime.today().strftime("%Y-%m-%d")

# Basic stats
mean_val = df["SBP"].mean()
sd_val = df["SBP"].std(ddof=1)
n = len(df)
dfree = n - 1
stderr = sd_val / np.sqrt(n)

# t-statistic and p-value
t_stat, p_val_raw = stats.ttest_1samp(df["SBP"], popmean=ref_mean)

# Adjust p-value for one-sided test
if sidedness == "one":
    p_val = p_val_raw / 2
else:
    p_val = p_val_raw

# Compute t critical and confidence intervals
if sidedness == "one":
    t_crit = stats.t.ppf(1 - alpha, dfree)
    ci_low = mean_val - t_crit * stderr
    ci_high = np.nan  # one-sided test typically reports lower bound only
else:
    t_crit = stats.t.ppf(1 - alpha/2, dfree)
    ci_low = mean_val - t_crit * stderr
    ci_high = mean_val + t_crit * stderr

# Build rows
rows = [
    ["CAMIS-PT-COMP","MEAN","Mean SBP",round(mean_val,2),f"{round(mean_val,2)}",analysis_date,1,"Y"],
    ["CAMIS-PT-COMP","SD","SD SBP",round(sd_val,2),f"{round(sd_val,2)}",analysis_date,2,"Y"],
    ["CAMIS-PT-COMP","SE","Standard Error",round(stderr,4),f"{round(stderr,4)}",analysis_date,3,"Y"],
    ["CAMIS-PT-COMP","DF","Degrees of Freedom",dfree,str(dfree),analysis_date,4,"Y"],
    ["CAMIS-PT-COMP","TSTAT","t-Statistic",round(t_stat,4),f"{round(t_stat,4)}",analysis_date,5,"Y"],
    ["CAMIS-PT-COMP","PVALUE","p-Value",round(p_val,4),f"{round(p_val,4)}",analysis_date,6,"Y"],
]

# Add confidence intervals
if sidedness == "two":
    rows.append(["CAMIS-PT-COMP","CILOW","Lower CI Bound",round(ci_low,4),f"{round(ci_low,4)}",analysis_date,7,"Y"])
    rows.append(["CAMIS-PT-COMP","CIHIGH","Upper CI Bound",round(ci_high,4),f"{round(ci_high,4)}",analysis_date,8,"Y"])
else:
    rows.append(["CAMIS-PT-COMP","CILOW","Lower CI Bound",round(ci_low,4),f"{round(ci_low,4)}",analysis_date,7,"Y"])

# Build Dataset-JSON structure
dataset_json = {
    "datasetJSONCreationDateTime": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    "datasetJSONVersion": "1.1.0",
    "itemGroupOID": "IG.BDS.SUMMARY",
    "name": "BDS_SUMMARY",
    "label": dataset_title,
    "records": len(rows),
    "columns": [
        {"itemOID":"IT.BDS.USUBJID","name":"USUBJID","label":"Subject ID","dataType":"string","keySequence":1},
        {"itemOID":"IT.BDS.PARAMCD","name":"PARAMCD","label":"Parameter Code","dataType":"string"},
        {"itemOID":"IT.BDS.PARAM","name":"PARAM","label":"Parameter Description","dataType":"string"},
        {"itemOID":"IT.BDS.AVAL","name":"AVAL","label":"Analysis Value","dataType":"decimal"},
        {"itemOID":"IT.BDS.AVALC","name":"AVALC","label":"Analysis Value (char)","dataType":"string"},
        {"itemOID":"IT.BDS.ADT","name":"ADT","label":"Analysis Date","dataType":"date","keySequence":2},
        {"itemOID":"IT.BDS.ASEQ","name":"ASEQ","label":"Analysis Sequence","dataType":"integer","keySequence":3},
        {"itemOID":"IT.BDS.ANL01FL","name":"ANL01FL","label":"Flag analysis 01","dataType":"string"}
    ],
    "rows": rows
}

# Write JSON file
with open("adam_bds_python.json", "w") as f:
    json.dump(dataset_json, f, indent=2)

print("Dataset-JSON v1.1 file created: adam_bds_python.json")
