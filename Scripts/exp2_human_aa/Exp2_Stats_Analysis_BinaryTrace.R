# Load necessary libraries
library(lme4)
library(lmerTest)  # For F-tests with Kenward-Roger degrees of freedom
library(emmeans)  # For post-hoc pairwise comparisons
library(pbkrtest)  # Ensure Kenward-Roger works correctly

# Get the project root directory (2 levels up from this script)
# This works for both Rscript and RStudio
get_script_dir <- function() {
  args <- commandArgs(trailingOnly = FALSE)
  file_arg <- grep("^--file=", args, value = TRUE)
  if (length(file_arg) > 0) {
    # Running via Rscript
    return(dirname(sub("^--file=", "", file_arg)))
  } else if (!is.null(sys.frames()[[1]]$ofile)) {
    # Running in RStudio with source()
    return(dirname(sys.frames()[[1]]$ofile))
  } else {
    # Fallback: use current working directory
    return(getwd())
  }
}

script_dir <- get_script_dir()
project_root <- normalizePath(file.path(script_dir, "..", ".."))

data_file <- file.path(project_root, "OtherResults", "binaryTraceOverlaps", "binarytraceoverlap.csv")

# Check if file exists
if (!file.exists(data_file)) {
  stop(paste("Data file not found:", data_file, "\nPlease run the corresponding Jupyter notebook first to generate this file."))
}

cat("Reading data from:", data_file, "\n")
combined_data <- read.csv(data_file)

# Convert relevant columns to factors
combined_data$Pair <- as.factor(combined_data$Pair)
combined_data$Agent_Type <- as.factor(combined_data$Agent_Type)

# Reshape data to long format for TAConditions
library(tidyr)
combined_data_long <- gather(combined_data, key = "TACondition", value = "Score", 
                             TACondition_3, TACondition_4, TACondition_5)

# Convert TACondition to a factor
combined_data_long$TACondition <- as.factor(combined_data_long$TACondition)

# Fit the mixed-effects model using lmerTest to get F-tests with Kenward-Roger method
model <- lmer(Score ~ Agent_Type * TACondition + (1 | Pair), 
              data = combined_data_long, REML = TRUE)

# Perform ANOVA to report F-tests for main effects and interaction effects
anova_results <- anova(model, type = "III", ddf = "Kenward-Roger")  # Automatically reports F-tests with Kenward-Roger
print(anova_results)

# Check for significant interaction
interaction_p_value <- anova_results["Agent_Type:TACondition", "Pr(>F)"]

if (!is.na(interaction_p_value) && interaction_p_value < 0.05) {
  # Significant interaction, run simple effects analysis (split by TACondition)
  cat("Significant interaction found, running simple effects...\n")
  
  # Simple effects of Agent_Type within each TACondition
  emm_interaction <- emmeans(model, ~ Agent_Type | TACondition)
  simple_effects <- test(emm_interaction)
  print(simple_effects)
  
  # For each TACondition, check if Agent_Type is significant
  significant_conditions <- which(simple_effects$p.value < 0.05)
  
  # If there are significant simple effects, run post-hoc tests
  if (length(significant_conditions) > 0) {
    cat("Significant simple effects found, running post-hoc comparisons...\n")
    pairwise_interaction_results <- pairs(emm_interaction, adjust = "tukey")
    print(pairwise_interaction_results)
  } else {
    cat("No significant simple effects of Agent_Type found.\n")
  }
  
} else {
  cat("No significant interaction found, running post-hoc tests for main effects...\n")
  
  # No interaction, run post-hoc pairwise comparisons for main effects
  # Post-hoc pairwise comparisons for Agent_Type
  emm_agent <- emmeans(model, ~ Agent_Type)
  pairwise_agent_results <- pairs(emm_agent, adjust = "tukey")
  print(pairwise_agent_results)
  
  # Post-hoc pairwise comparisons for TACondition
  emm_condition <- emmeans(model, ~ TACondition)
  pairwise_condition_results <- pairs(emm_condition, adjust = "tukey")
  print(pairwise_condition_results)
}

# Save results to a file
capture.output(anova_results, file = "anova_results.txt")
capture.output(simple_effects, file = "simple_effects_results.txt", append = TRUE)
capture.output(pairwise_interaction_results, file = "pairwise_interaction_results.txt", append = TRUE)
