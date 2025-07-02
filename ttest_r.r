# Load libraries
library(dplyr)
library(readr)

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

# Build ADaM BDS dataset
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

