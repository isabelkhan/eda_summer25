# Load libraries
library(dplyr)
library(readr)
library(jsonlite)

# Get command line arguments
args <- commandArgs(trailingOnly = TRUE)

# Check arguments
if (length(args) != 1) {
  stop("Usage: Rscript test_r.R <reference_mean>")
}

# Parse reference mean
ref_mean <- as.numeric(args[1])
if (is.na(ref_mean)) {
  stop("Error: reference_mean must be numeric.")
}

# Read the data
df <- read_csv("one_sample_ttest_raw_data.csv")

# Analysis date
analysis_date <- Sys.Date()

# Compute statistics
mean_val <- mean(df$SBP)
sd_val <- sd(df$SBP)
ttest_res <- t.test(df$SBP, mu = ref_mean)

# Build rows (as list of vectors)
rows <- list(
  list("CAMIS-PT-001","MEAN","Mean SBP",round(mean_val,2),as.character(round(mean_val,2)),as.character(analysis_date),1,"Y"),
  list("CAMIS-PT-001","SD","SD SBP",round(sd_val,2),as.character(round(sd_val,2)),as.character(analysis_date),2,"Y"),
  list("CAMIS-PT-001","TSTAT","t-Statistic",round(ttest_res$statistic,2),as.character(round(ttest_res$statistic,2)),as.character(analysis_date),3,"Y"),
  list("CAMIS-PT-001","PVALUE","p-Value",round(ttest_res$p.value,4),as.character(round(ttest_res$p.value,4)),as.character(analysis_date),4,"Y")
)

# Build Dataset-JSON structure
dataset_json <- list(
  datasetJSONCreationDateTime = format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz="UTC"),
  datasetJSONVersion = "1.1.0",
  itemGroupOID = "IG.BDS.SUMMARY",
  name = "BDS_SUMMARY",
  label = "Summary Statistics BDS",
  records = length(rows),
  columns = list(
    list(itemOID="IT.BDS.USUBJID", name="USUBJID", label="Subject ID", dataType="string", keySequence=1),
    list(itemOID="IT.BDS.PARAMCD", name="PARAMCD", label="Parameter Code", dataType="string"),
    list(itemOID="IT.BDS.PARAM", name="PARAM", label="Parameter Description", dataType="string"),
    list(itemOID="IT.BDS.AVAL", name="AVAL", label="Analysis Value", dataType="decimal"),
    list(itemOID="IT.BDS.AVALC", name="AVALC", label="Analysis Value (char)", dataType="string"),
    list(itemOID="IT.BDS.ADT", name="ADT", label="Analysis Date", dataType="date", keySequence=2),
    list(itemOID="IT.BDS.ASEQ", name="ASEQ", label="Analysis Sequence", dataType="integer", keySequence=3),
    list(itemOID="IT.BDS.ANL01FL", name="ANL01FL", label="Flag analysis 01", dataType="string")
  ),
  rows = rows
)

# Save JSON
write_json(dataset_json, "adam_bds_r.json", pretty = TRUE, auto_unbox = TRUE)

# Also build ADaM BDS dataset for CSV
adam_df <- tibble(
  USUBJID = rep("CAMIS-PT-001", 4),
  PARAMCD = c("MEAN", "SD", "TSTAT", "PVALUE"),
  PARAM = c("Mean SBP", "SD SBP", "t-Statistic", "p-Value"),
  AVAL = round(c(mean_val, sd_val, ttest_res$statistic, ttest_res$p.value), 4),
  AVALC = as.character(round(c(mean_val, sd_val, ttest_res$statistic, ttest_res$p.value), 4)),
  ADT = rep(as.character(analysis_date), 4),
  ASEQ = 1:4,
  ANL01FL = "Y"
)

# Save CSV
write_csv(adam_df, "adam_bds_r.csv")
print(adam_df)

cat("Dataset-JSON v1.1 file created: adam_bds_r.json\n")
