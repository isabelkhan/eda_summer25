# Load libraries
library(dplyr)
library(readr)
library(jsonlite)

# Get command line arguments
args <- commandArgs(trailingOnly = TRUE)

# Check arguments
if (length(args) != 6) {
  stop(
    paste(
      "Usage:\n",
      "Rscript test_r.R <reference_mean> <alpha> <sidedness> <dataset_title> <input_filename> <column_name>\n\n",
      "Arguments:\n",
      "  reference_mean: numeric target mean\n",
      "  alpha: significance level (e.g., 0.05)\n",
      "  sidedness: 'two', 'upper', or 'lower'\n",
      "  dataset_title: quoted string label\n",
      "  input_filename: CSV file with data\n",
      "  column_name: column to analyze\n"
    )
  )
}

# Parse arguments
ref_mean <- as.numeric(args[1])
if (is.na(ref_mean)) {
  stop("Error: reference_mean must be numeric.")
}

alpha <- as.numeric(args[2])
if (is.na(alpha) || alpha <= 0 || alpha >= 1) {
  stop("Error: alpha must be a number between 0 and 1.")
}

sidedness <- tolower(args[3])
if (!(sidedness %in% c("two", "upper", "lower"))) {
  stop("Error: sidedness must be 'two', 'upper', or 'lower'.")
}

dataset_title <- args[4]
input_filename <- args[5]
column_name <- args[6]

# Read the data
df <- read_csv(input_filename)

# Validate column exists
if (!(column_name %in% names(df))) {
  stop(paste("Error: column '", column_name, "' not found in the dataset.\nAvailable columns: ", paste(names(df), collapse=", ")))
}

# Extract the column
values <- df[[column_name]]
values <- values[!is.na(values)]

# Analysis date
analysis_date <- Sys.Date()

# Compute statistics
mean_val <- mean(values)
sd_val <- sd(values)
n <- length(values)
dfree <- n - 1
stderr <- sd_val / sqrt(n)

# Compute t-statistic and p-value
ttest_res <- t.test(values, mu = ref_mean)

# Adjust p-value
if (sidedness == "two") {
  p_val <- ttest_res$p.value
} else {
  p_val <- ttest_res$p.value / 2
}

# Compute t critical and confidence intervals
if (sidedness == "two") {
  t_crit <- qt(1 - alpha / 2, dfree)
  ci_low <- mean_val - t_crit * stderr
  ci_high <- mean_val + t_crit * stderr
} else if (sidedness == "upper") {
  t_crit <- qt(1 - alpha, dfree)
  ci_low <- mean_val - t_crit * stderr
  ci_high <- NA
} else {  # 'lower'
  t_crit <- qt(1 - alpha, dfree)
  ci_low <- NA
  ci_high <- mean_val + t_crit * stderr
}

# Build rows (list of vectors)
rows <- list(
  list("CAMIS-PT-COMP","MEAN",paste0("Mean ", column_name),round(mean_val,2),as.character(round(mean_val,2)),as.character(analysis_date),1,"Y"),
  list("CAMIS-PT-COMP","SD",paste0("SD ", column_name),round(sd_val,2),as.character(round(sd_val,2)),as.character(analysis_date),2,"Y"),
  list("CAMIS-PT-COMP","SE","Standard Error",round(stderr,4),as.character(round(stderr,4)),as.character(analysis_date),3,"Y"),
  list("CAMIS-PT-COMP","DF","Degrees of Freedom",dfree,as.character(dfree),as.character(analysis_date),4,"Y"),
  list("CAMIS-PT-COMP","TSTAT","t-Statistic",round(ttest_res$statistic,4),as.character(round(ttest_res$statistic,4)),as.character(analysis_date),5,"Y"),
  list("CAMIS-PT-COMP","PVALUE","p-Value",round(p_val,4),as.character(round(p_val,4)),as.character(analysis_date),6,"Y")
)

# Add confidence intervals
if (sidedness == "two") {
  rows <- append(rows, list(
    list("CAMIS-PT-COMP","CILOW","Lower CI Bound",round(ci_low,4),as.character(round(ci_low,4)),as.character(analysis_date),7,"Y"),
    list("CAMIS-PT-COMP","CIHIGH","Upper CI Bound",round(ci_high,4),as.character(round(ci_high,4)),as.character(analysis_date),8,"Y")
  ))
} else if (sidedness == "upper") {
  rows <- append(rows, list(
    list("CAMIS-PT-COMP","CILOW","Lower CI Bound",round(ci_low,4),as.character(round(ci_low,4)),as.character(analysis_date),7,"Y")
  ))
} else {  # 'lower'
  rows <- append(rows, list(
    list("CAMIS-PT-COMP","CIHIGH","Upper CI Bound",round(ci_high,4),as.character(round(ci_high,4)),as.character(analysis_date),7,"Y")
  ))
}

# Build Dataset-JSON structure
dataset_json <- list(
  datasetJSONCreationDateTime = format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz="UTC"),
  datasetJSONVersion = "1.1.0",
  itemGroupOID = "IG.BDS.SUMMARY",
  name = "BDS_SUMMARY",
  label = dataset_title,
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
paramcd_list <- c("MEAN", "SD", "SE", "DF", "TSTAT", "PVALUE")
param_list <- c(paste0("Mean ", column_name), paste0("SD ", column_name), "Standard Error", "Degrees of Freedom", "t-Statistic", "p-Value")
aval_list <- c(
  round(mean_val,2),
  round(sd_val,2),
  round(stderr,4),
  dfree,
  round(ttest_res$statistic,4),
  round(p_val,4)
)

if (sidedness == "two") {
  paramcd_list <- c(paramcd_list, "CILOW", "CIHIGH")
  param_list <- c(param_list, "Lower CI Bound", "Upper CI Bound")
  aval_list <- c(aval_list, round(ci_low,4), round(ci_high,4))
} else if (sidedness == "upper") {
  paramcd_list <- c(paramcd_list, "CILOW")
  param_list <- c(param_list, "Lower CI Bound")
  aval_list <- c(aval_list, round(ci_low,4))
} else {
  paramcd_list <- c(paramcd_list, "CIHIGH")
  param_list <- c(param_list, "Upper CI Bound")
  aval_list <- c(aval_list, round(ci_high,4))
}

adam_df <- tibble(
  USUBJID = rep("CAMIS-PT-COMP", length(aval_list)),
  PARAMCD = paramcd_list,
  PARAM = param_list,
  AVAL = aval_list,
  AVALC = as.character(AVAL),
  ADT = rep(as.character(analysis_date), length(aval_list)),
  ASEQ = seq_along(aval_list),
  ANL01FL = "Y"
)

# Save CSV
write_csv(adam_df, "adam_bds_r.csv")
print(adam_df)

cat("Dataset-JSON v1.1 file created: adam_bds_r.json\n")
