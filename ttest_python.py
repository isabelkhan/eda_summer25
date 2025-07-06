import sys
import json
import pandas as pd
from scipy import stats
from datetime import datetime
import numpy as np

# Usage message
usage_msg = (
    "Usage:\n"
    "  python test_python.py <reference_mean> <alpha> <sidedness> <dataset_title> <input_filename> <column_name>\n\n"
    "Arguments:\n"
    "  reference_mean: numeric target mean\n"
    "  alpha: significance level (e.g., 0.05)\n"
    "  sidedness: 'two', 'upper', or 'lower'\n"
    "  dataset_title: quoted string label\n"
    "  input_filename: CSV file with data\n"
    "  column_name: column in the CSV to analyze\n"
)

# Check argument count
if len(sys.argv) != 7:
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
if sidedness not in ["two", "upper", "lower"]:
    print("Error: sidedness must be 'two', 'upper', or 'lower'.")
    sys.exit(1)

dataset_title = sys.argv[4]
input_filename = sys.argv[5]
column_name = sys.argv[6]

# Load the data
df = pd.read_csv(input_filename)

# Validate column
if column_name not in df.columns:
    print(f"Error: column '{column_name}' not found in {input_filename}. Available columns: {list(df.columns)}")
    sys.exit(1)

# Analysis date
analysis_date = datetime.today().strftime("%Y-%m-%d")

# Basic stats
values = df[column_name].dropna()
mean_val = values.mean()
sd_val = values.std(ddof=1)
n = len(values)
dfree = n - 1
stderr = sd_val / np.sqrt(n)

# t-statistic and p-value
t_stat, p_val_raw = stats.ttest_1samp(values, popmean=ref_mean)

# Adjust p-value
if sidedness == "two":
    p_val = p_val_raw
else:
    p_val = p_val_raw / 2

# Compute t critical and confidence intervals
if sidedness == "two":
    t_crit = stats.t.ppf(1 - alpha / 2, dfree)
    ci_low = mean_val - t_crit * stderr
    ci_high = mean_val + t_crit * stderr
elif sidedness == "upper":
    t_crit = stats.t.ppf(1 - alpha, dfree)
    ci_low = mean_val - t_crit * stderr
    ci_high = np.nan
else:  # 'lower'
    t_crit = stats.t.ppf(1 - alpha, dfree)
    ci_low = np.nan
    ci_high = mean_val + t_crit * stderr

# Build rows for JSON
rows = [
    ["CAMIS-PT-COMP","MEAN",f"Mean {column_name}",round(mean_val,2),f"{round(mean_val,2)}",analysis_date,1,"Y"],
    ["CAMIS-PT-COMP","SD",f"SD {column_name}",round(sd_val,2),f"{round(sd_val,2)}",analysis_date,2,"Y"],
    ["CAMIS-PT-COMP","SE","Standard Error",round(stderr,4),f"{round(stderr,4)}",analysis_date,3,"Y"],
    ["CAMIS-PT-COMP","DF","Degrees of Freedom",dfree,str(dfree),analysis_date,4,"Y"],
    ["CAMIS-PT-COMP","TSTAT","t-Statistic",round(t_stat,4),f"{round(t_stat,4)}",analysis_date,5,"Y"],
    ["CAMIS-PT-COMP","PVALUE","p-Value",round(p_val,4),f"{round(p_val,4)}",analysis_date,6,"Y"],
]

# Also build parameter lists for CSV
paramcd_list = ["MEAN","SD","SE","DF","TSTAT","PVALUE"]
param_list = [f"Mean {column_name}", f"SD {column_name}", "Standard Error", "Degrees of Freedom", "t-Statistic", "p-Value"]
aval_list = [
    round(mean_val,2),
    round(sd_val,2),
    round(stderr,4),
    dfree,
    round(t_stat,4),
    round(p_val,4)
]

# Add confidence intervals
if sidedness == "two":
    rows.append(["CAMIS-PT-COMP","CILOW","Lower CI Bound",round(ci_low,4),f"{round(ci_low,4)}",analysis_date,7,"Y"])
    rows.append(["CAMIS-PT-COMP","CIHIGH","Upper CI Bound",round(ci_high,4),f"{round(ci_high,4)}",analysis_date,8,"Y"])
    paramcd_list += ["CILOW","CIHIGH"]
    param_list += ["Lower CI Bound","Upper CI Bound"]
    aval_list += [round(ci_low,4), round(ci_high,4)]
elif sidedness == "upper":
    rows.append(["CAMIS-PT-COMP","CILOW","Lower CI Bound",round(ci_low,4),f"{round(ci_low,4)}",analysis_date,7,"Y"])
    paramcd_list.append("CILOW")
    param_list.append("Lower CI Bound")
    aval_list.append(round(ci_low,4))
else:  # 'lower'
    rows.append(["CAMIS-PT-COMP","CIHIGH","Upper CI Bound",round(ci_high,4),f"{round(ci_high,4)}",analysis_date,7,"Y"])
    paramcd_list.append("CIHIGH")
    param_list.append("Upper CI Bound")
    aval_list.append(round(ci_high,4))

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

# Also build and write CSV 
adam_df = pd.DataFrame({
    "USUBJID": ["CAMIS-PT-COMP"] * len(paramcd_list),
    "PARAMCD": paramcd_list,
    "PARAM": param_list,
    "AVAL": aval_list,
    "AVALC": [str(a) for a in aval_list],
    "ADT": [analysis_date] * len(paramcd_list),
    "ASEQ": list(range(1, len(paramcd_list) + 1)),
    "ANL01FL": ["Y"] * len(paramcd_list)
})

adam_df.to_csv("adam_bds_python.csv", index=False)
print("CSV file created: adam_bds_python.csv")
print(adam_df)
