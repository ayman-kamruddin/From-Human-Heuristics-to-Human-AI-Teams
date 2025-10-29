# Load necessary libraries
library(lme4)       # For mixed-effects models
library(lmerTest)   # For p-values and F-tests with Kenward-Roger method
library(emmeans)    # For post-hoc comparisons
library(tidyverse)  # For data manipulation and visualization
library(crayon)     # For colorized console output

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

data_file <- file.path(project_root, "OtherResults", "DTW_TS_Errors", "combined_targetselectionoverlap_data_for_R.csv")

# Check if file exists
if (!file.exists(data_file)) {
  stop(paste("Data file not found:", data_file, "\nPlease run the corresponding Jupyter notebook first to generate this file."))
}

cat("Reading data from:", data_file, "\n")
data <- read.csv(data_file)
# Ensure factors are properly set for categorical variables
data$Policy <- as.factor(data$Policy)
data$TACondition <- as.factor(data$TACondition)
data$Session <- as.factor(data$Session)    # Random effect
data$Player <- as.factor(data$Player)      # Nested random effect within Session

# Fit the mixed-effects model
model <- lmer(Average_Score ~ Policy * TACondition + (1 | Session/Player), data = data, REML = TRUE)

# Perform ANOVA (Type III sum of squares, Kenward-Roger degrees of freedom)
anova_results <- anova(model, type = "III", ddf = "Kenward-Roger")
cat(cyan("\nMixed-Effects Model ANOVA Results:\n")); print(anova_results)

# Post-hoc analysis
interaction_p_value <- anova_results["Policy:TACondition", "Pr(>F)"]

if (!is.na(interaction_p_value) && interaction_p_value < 0.05) {
  cat(yellow("\nSignificant interaction found. Performing simple effects analysis...\n"))
  
  # Simple effects of Policy within each level of TACondition
  emm_interaction <- emmeans(model, ~ Policy | TACondition)
  simple_effects <- test(emm_interaction)
  cat(cyan("\nSimple Effects Analysis:\n")); print(simple_effects)
  
  # Post-hoc pairwise comparisons for the interaction
  pairwise_interaction <- pairs(emm_interaction, adjust = "tukey")
  cat(cyan("\nPairwise Comparisons for Interaction:\n")); print(pairwise_interaction)
} else {
  cat(yellow("\nNo significant interaction found. Performing post-hoc tests for main effects...\n"))
  
  # Post-hoc pairwise comparisons for main effects
  emm_policy <- emmeans(model, ~ Policy)
  pairwise_policy <- pairs(emm_policy, adjust = "tukey")
  cat(cyan("\nPairwise Comparisons for Policy:\n")); print(pairwise_policy)
  
  emm_tacondition <- emmeans(model, ~ TACondition)
  pairwise_tacondition <- pairs(emm_tacondition, adjust = "tukey")
  cat(cyan("\nPairwise Comparisons for TACondition:\n")); print(pairwise_tacondition)
}

# Generate box plot
box_plot <- ggplot(data, aes(x = TACondition, y = Average_Score, fill = Policy)) +
  geom_boxplot(outlier.shape = 21, outlier.size = 2, position = position_dodge(width = 0.8)) +
  scale_fill_manual(values = c("#0072B2", "#E69F00", "#009E73", "#F0E442", "#CC79A7")) +
  labs(x = "TACondition", y = "Average Score", fill = "Policy") +
  theme_minimal() +
  theme(
    text = element_text(size = 12),
    axis.title = element_text(size = 14),
    legend.position = "bottom"
  )

# Save the plot as an image
ggsave("box_plot.png", plot = box_plot, width = 8, height = 6)

# Display the plot
print(box_plot)
