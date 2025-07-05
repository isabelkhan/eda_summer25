import sys
import pandas as pd
from scipy import stats
from datetime import datetime

# Check command line arguments
if len(sys.argv) != 2:
    print("Usage: python test_python.py <reference_mean>")
    sys.exit(1)

# Parse the reference mean from the command line
try:
    ref_mean = float(sys.argv[1])
except ValueError:
    print("Error: reference_mean must be a number.")
    sys.exit(1)

# Load the data
df = pd.read_csv("one_sample_ttest_raw_data.csv")

# Analysis date
analysis_date = datetime.today().strftime("%Y-%m-%d")

# Compute statistics
mean_val = df["SBP"].mean()
sd_val = df["SBP"].std(ddof=1)
t_stat, p_val = stats.ttest_1samp(df["SBP"], popmean=ref_mean)

# Build ADaM BDS dataset
records = [
    {"USUBJID": "CAMIS-PT-001", "PARAMCD": "MEAN",   "PARAM": "Mean SBP",   "AVAL": round(mean_val,2), "AVALC": f"{round(mean_val,2)}", "ADT": analysis_date, "ASEQ":1, "ANL01FL":"Y"},
    {"USUBJID": "CAMIS-PT-001", "PARAMCD": "SD",     "PARAM": "SD SBP",     "AVAL": round(sd_val,2),   "AVALC": f"{round(sd_val,2)}",   "ADT": analysis_date, "ASEQ":2, "ANL01FL":"Y"},
    {"USUBJID": "CAMIS-PT-001", "PARAMCD": "TSTAT",  "PARAM": "t-Statistic","AVAL": round(t_stat,2),   "AVALC": f"{round(t_stat,2)}",   "ADT": analysis_date, "ASEQ":3, "ANL01FL":"Y"},
    {"USUBJID": "CAMIS-PT-001", "PARAMCD": "PVALUE", "PARAM": "p-Value",    "AVAL": round(p_val,4),    "AVALC": f"{round(p_val,4)}",    "ADT": analysis_date, "ASEQ":4, "ANL01FL":"Y"}
]

adam_df = pd.DataFrame(records)

# Output CSV
adam_df.to_csv("adam_bds_python.csv", index=False)
print(adam_df)
