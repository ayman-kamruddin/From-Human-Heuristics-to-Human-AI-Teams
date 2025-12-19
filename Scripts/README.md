# Analysis Scripts

This folder contains all the scripts needed to reproduce the analyses from the paper, now organized into clear subdirectories.

## Folder Structure

```
Scripts/
├── exp1_human_human/          # Experiment 1 (Human-Human) analysis scripts
├── exp2_human_aa/             # Experiment 2 (Human-AA) analysis scripts
├── simulation/                # Simulation exploration scripts
├── tools/                     # Shared utility functions
├── trialTAConditions.csv      # Trial configuration data
└── README.md                  # This file
```

## Overview

The analysis is divided into:
- **Experiment 1 (Exp1)**: Human-Human experiments → `exp1_human_human/`
- **Experiment 2 (Exp2)**: Human-AA (Artificial Agent) experiments → `exp2_human_aa/`
- **Simulation Analysis**: AA-AA simulation data → `simulation/`

## Before You Start

1. Make sure you've run `check_setup.py` from the root directory to verify your setup
2. Ensure all Python dependencies are installed: `pip install -r requirements.txt`
3. For R scripts, ensure you have R installed with the following packages:
   - `lme4`, `lmerTest`, `emmeans`, `pbkrtest`, `tidyverse`, `crayon`
4. The scripts will create output directories automatically in `OtherResults/`

## Analysis Workflow Overview

Both experiments follow a similar pipeline:

```
Python Preprocessing → Jupyter Notebook Analysis → R Statistical Analysis
```

**Key points:**
- Each analysis requires completing ALL steps sequentially before running R scripts
- Jupyter notebooks must complete successfully to generate the CSV files needed by R
- Experiment 2 TSp analysis requires Experiment 1 TSp step 1 to be completed first
- R scripts need manual editing to switch between TSp and Binary Trace analyses (see notes in each section)

## Getting Familiar with the Data

**Optional - Explore Simulation Data:**

Navigate to the `simulation/` subfolder and run `simReader-AA_AA.ipynb` to explore the AA-AA simulation data and generate exploratory plots. 


---

## Experiment 1: Human-Human Analysis

All scripts for Experiment 1 are in the `exp1_human_human/` subfolder.

**Important**: For both analyses below, you must complete ALL preprocessing steps (Python scripts AND Jupyter notebooks) before running the R statistical analysis script. The R script requires CSV files that are only generated after the Jupyter notebooks complete successfully.

### Analysis 1a: TSp Overlap in Exp 1

Target Selection Policy (TSp) overlap analysis for human-human teams.

**Steps:**

1. **Generate dynamic policies**
   ```bash
   cd Scripts/exp1_human_human # or 'cd exp1_human_human' if already in Scripts folder
   python get_actual_TS_Dynamic_Policy_as_csv.py
   ```
   - **Input**: Raw experimental data from `RAW_EXPERIMENT_DATA/TWO-HUMAN_HAs/`
   - **Output**: Dynamic policies saved to `OtherResults/TS_Dynamic_Policy/`

2. **Calculate DTW values**
   ```bash
   python compare_dynamic_policies_by_TA_and_Participant_TS_DTW.py
   ```
   - **Input**: Dynamic policies from step 1
   - **Output**: Normalized DTW values saved to `OtherResults/DTW_TS_Errors/combined_targetselectionoverlap_data_for_R.csv`

3. **Generate box plots and prepare data for R**
   ```bash
   jupyter notebook exp1_TSOverlap_Analysis.ipynb
   ```
   - Run all cells in the notebook
   - **Input**: CSV file from step 2
   - **Output**: Box plots and formatted data for statistical analysis

4. **Run statistical analysis**
   ```bash
   Rscript exp1_mixed_linear_model_TSOverlap.r
   ```
   - **Prerequisites**: Steps 1-3 must complete successfully first
   - **Output**: Statistical results and mixed-effects model outputs

### Analysis 1b: Binary Trace Comparison in Exp 1

Compares spatial trajectories using binary trace overlap.

**Steps:**

1. **Calculate binary trace values**
   ```bash
   cd Scripts/exp1_human_human # or 'cd exp1_human_human' if not already there
   python binary_trace_evaluator_Exp1.py
   ```
   - **Input**: Raw experimental data from `RAW_EXPERIMENT_DATA/TWO-HUMAN_HAs/`
   - **Output**: Binary trace scores saved to `OtherResults/AA_scores_traces/combined_binarytraceoverlap_data_for_R.csv`

2. **Analyze and visualize**
   ```bash
   jupyter notebook exp1_BinaryTrace_Analysis.ipynb
   ```
   - Run all cells in the notebook
   - **Input**: CSV file from step 1
   - **Output**: Visualizations and formatted data for statistical analysis

3. **Run statistical analysis**
   ```bash
   Rscript exp1_mixed_linear_model_BinaryTrace.r
   ```
   - **Prerequisites**: Steps 1-2 must complete successfully first
   - **Output**: Statistical results and mixed-effects model outputs  

---

## Experiment 2: Human-AA Team Analysis

All scripts for Experiment 2 are in the `exp2_human_aa/` subfolder.

This analysis compares human-AA teams against human-human baselines using three comparison types:
1. **Surrogate human data**: Human data compared to itself (leave-one-out analysis)
2. **Human players** from human-AA pairs compared to Exp 1's human-human data
3. **AA agents** from human-AA pairs compared to Exp 1's human-human data

**Important**: For both analyses below, you must complete ALL preprocessing steps (Python scripts AND Jupyter notebooks) before running the R statistical analysis script. The R script requires CSV files that are only generated after the Jupyter notebooks complete successfully. Additionally, Analysis 2a requires that Analysis 1a step 1 has been completed (to generate Exp1 dynamic policies for comparison).

### Analysis 2a: TSp Overlap in Exp 2

Comparing Target Selection Policies between human-AA teams and human-human baselines.

**Steps:**

1. **Generate TSp vectors for Human-AA teams**
   ```bash
   cd exp2_human_aa
   python get_actual_Dynamic_Policy_as_csv_Human-AA.py
   ```
   - **Input**: Raw Human-AA data from `RAW_EXPERIMENT_DATA/HUMAN-AA_TEAM/`
   - **Output**: TSp binary encoded vectors for all agent types (Heuristic, Human-Sensitive, SelfPlay)
   - Saved to `OtherResults/Actual_Dynamic_Policies_HumanAA/`

2. **Calculate all DTW comparisons**
   ```bash
   python calcAllDTW.py
   ```
   - **Input**: Dynamic policies from Exp1 (step 1 from Analysis 1a) and Exp2 (step 1 above)
   - **Output**: DTW scores saved as CSV files in `OtherResults/TSp_DTWs/`:
     - `AA_scores_heur.csv`, `AA_scores_hybr.csv`, `AA_scores_self.csv`
     - `human_scores_heur.csv`, `human_scores_hybr.csv`, `human_scores_self.csv`
     - `humanTeamDTWs.csv`

3. **Convert to analysis format**
   ```bash
   python convert_scores_exp2.py
   ```
   - **Note**: Edit the script to set `input_folder = "TSp_DTWs"` (line 17)
   - **Input**: CSV files from step 2
   - **Output**: `targetselectionoverlap.csv` in `OtherResults/TSp_DTWs/`

4. **Generate visualizations and prepare data for R**
   ```bash
   jupyter notebook exp2_TargetOverlap_Analysis.ipynb
   ```
   - Run all cells to generate box plots
   - **Input**: `targetselectionoverlap.csv` from step 3
   - **Output**: Visualizations and formatted data for statistical analysis

5. **Run statistical analysis**
   ```bash
   Rscript Exp2_Stats_Analysis_TSOverlap.R
   ```
   - **Prerequisites**: Steps 1-4 must complete successfully first
   - **Input**: `OtherResults/TSp_DTWs/targetselectionoverlap.csv`
   - **Output**: Statistical comparisons across agent types

### Analysis 2b: Binary Trace in Exp 2

Comparing spatial trajectories using binary trace overlap metrics.

**Steps:**

1. **Calculate binary trace scores**
   ```bash
   cd exp2_human_aa  # if not already there
   python traj_evals_binary_trace_scores.py
   ```
   - **Input**: Raw experimental data from `RAW_EXPERIMENT_DATA/HUMAN-AA_TEAM/` and `TWO-HUMAN_HAs/`
   - **Output**: Binary trace overlaps saved to `OtherResults/binaryTraceOverlaps/` as individual CSV files

2. **Convert to analysis format**
   ```bash
   python convert_scores_exp2.py
   ```
   - **Note**: Edit the script to set `input_folder = "binaryTraceOverlaps"` (line 17)
   - **Input**: CSV files from step 1
   - **Output**: `binarytraceoverlap.csv` in `OtherResults/binaryTraceOverlaps/`

3. **Generate visualizations and prepare data for R**
   ```bash
   jupyter notebook exp2_BinaryTrace_Analysis.ipynb
   ```
   - Run all cells to generate box plots
   - **Input**: `binarytraceoverlap.csv` from step 2
   - **Output**: Visualizations and formatted data for statistical analysis

4. **Run statistical analysis**
   ```bash
   Rscript Exp2_Stats_Analysis_BinaryTrace.R
   ```
   - **Prerequisites**: Steps 1-3 must complete successfully first
   - **Input**: `OtherResults/binaryTraceOverlaps/binarytraceoverlap.csv`
   - **Output**: Statistical comparisons across agent types

---

## Notes for General Users

### Working Directory
- Scripts should be run from their respective subfolders (`exp1_human_human/` or `exp2_human_aa/`)
- Scripts automatically detect the project root using relative paths
- Output folders are created automatically in the root `OtherResults/` directory

### Script Execution Time
- Some scripts may take several minutes to hours depending on your machine
- Progress bars (via `tqdm`) will show you the processing status

### Editing Scripts

**For Experiment 2 convert_scores_exp2.py:**
- Edit line 17 to switch between analyses:
  - `input_folder = "TSp_DTWs"` for Target Selection analysis
  - `input_folder = "binaryTraceOverlaps"` for Binary Trace analysis

**For Experiment 1 R script (mixed_linear_model_exp1.r):**
- Edit lines 29-33 to select which analysis to run:
  - Uncomment line 30 for TSp DTW analysis
  - Uncomment line 33 (default) for Binary Trace analysis

**For Experiment 2 R script (R_Analysis_Exp2.R):**
- Edit lines 28-32 to select which analysis to run:
  - Uncomment line 29 for Binary Trace analysis
  - Uncomment line 32 (default) for TSp DTW analysis

### Platform Compatibility
- All scripts now use `os.path.join()` for cross-platform path handling
- Works on Windows, macOS, and Linux

### Common Issues
- **FileNotFoundError when running R scripts**: Ensure you've completed ALL preprocessing steps (Python scripts AND Jupyter notebooks) before running R analysis
- **FileNotFoundError for raw data**: Verify data folders exist using `python ../check_setup.py`
- **ModuleNotFoundError**: Install dependencies with `pip install -r ../requirements.txt`
- **Permission errors**: Check write access to the `OtherResults/` folder
- **R package errors**: Install required R packages listed in "Before You Start" section
- **Exp2 Analysis 2a fails**: Ensure Experiment 1 Analysis 1a step 1 has completed (generates dynamic policies needed for comparison)
