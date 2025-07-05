import sys
import json
import pandas as pd
from scipy import stats
from datetime import datetime

# Check command line arguments
if len(sys.argv) != 2:
    print("Usage: python test_python.py <reference_mean>")
    sys.exit(1)

# Parse reference mean
try:
    ref_mean = float(sys.argv[1])
except ValueError:
    print("Error: reference_mean must be numeric.")
    sys.exit(1)

# Load the data
df = pd.read_csv("one_sample_ttest_raw_data.csv")

# Analysis date
analysis_date = datetime.today().strftime("%Y-%m-%d")

# Compute statistics
mean_val = df["SBP"].mean()
sd_val = df["SBP"].std(ddof=1)
t_stat, p_val = stats.ttest_1samp(df["SBP"], popmean=ref_mean)

# Build rows
rows = [
    ["CAMIS-PT-001","MEAN","Mean SBP",round(mean_val,2),f"{round(mean_val,2)}",analysis_date,1,"Y"],
    ["CAMIS-PT-001","SD","SD SBP",round(sd_val,2),f"{round(sd_val,2)}",analysis_date,2,"Y"],
    ["CAMIS-PT-001","TSTAT","t-Statistic",round(t_stat,2),f"{round(t_stat,2)}",analysis_date,3,"Y"],
    ["CAMIS-PT-001","PVALUE","p-Value",round(p_val,4),f"{round(p_val,4)}",analysis_date,4,"Y"]
]

# Build Dataset-JSON structure
dataset_json = {
    "datasetJSONCreationDateTime": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    "datasetJSONVersion": "1.1.0",
    "itemGroupOID": "IG.BDS.SUMMARY",
    "name": "BDS_SUMMARY",
    "label": "Summary Statistics BDS",
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
