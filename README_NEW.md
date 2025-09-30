# From Human Heuristics to Human–AI Teams

**Modeling Multiagent First-Person Herding using Dynamical Perceptual-Motor Primitives**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![DOI](https://img.shields.io/badge/DOI-10.DATA%2FMENDELEY-blue)](https://data.mendeley.com/datasets/kpxp5zkh5f/2)

---

## Overview

This repository contains the complete codebase for reproducing the analyses and figures from:

> **bin Kamruddin, A., Lam, C., Ghanem, S., Patil, G., Musolesi, M., di Bernardo, M., & Richardson, M. J.** (n.d.). From human heuristics to human–AI teams: Modeling multiagent first-person herding using dynamical perceptual–motor primitives. *[Manuscript submitted for publication]*.

### Research Summary

We introduce a first-person, multi-herder, multi-target shepherding paradigm to evaluate whether **low-dimensional movement dynamics** combined with **simple heuristic decision policies** can effectively reproduce human behavior. Our findings demonstrate that:

1. **Experiment 1** (Human-Human pairs, N=21 pairs): A simple target-selection heuristic (Successive Collinear Angle - SCA) captured 78.8% of human decisions, and a DPMP navigation model achieved >92% trajectory congruence with human movement.

2. **Experiment 2** (Human-AI pairs, N=22 participants): An artificial agent governed by the DPMP-SCA model matched or exceeded human baselines in goal-selection overlap (>90%) and produced nearly indistinguishable movement patterns, while human teammates seamlessly coordinated with the agent.

These results show that coupling dynamical movement models with transparent decision rules yields interpretable, high-fidelity artificial collaborators for human-AI teams.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Repository Structure](#repository-structure)
- [Data Download](#data-download)
- [Running the Analyses](#running-the-analyses)
- [Reproducing Paper Figures](#reproducing-paper-figures)
- [Code-to-Paper Mapping](#code-to-paper-mapping)
- [Citation](#citation)
- [Authors](#authors)
- [License](#license)

---

## Quick Start

For reviewers and researchers who want to quickly reproduce the main results:

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/From-Human-Heuristics-to-Human-AI-Teams.git
cd From-Human-Heuristics-to-Human-AI-Teams

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download data from Mendeley
# Visit: https://data.mendeley.com/datasets/kpxp5zkh5f/2
# Extract the data folder to the project root directory

# 4. Run analyses (choose one experiment)
cd Scripts

# For Experiment 1 (Human-Human baseline):
python binary_trace_evaluator_Exp1.py
jupyter notebook exp1_BinaryTrace_Analysis.ipynb

# For Experiment 2 (Human-AI collaboration):
python traj_evals_binary_trace_scores.py
jupyter notebook exp2_BinaryTrace_Analysis.ipynb
```

**Expected Runtime**: Each experiment's full analysis pipeline takes approximately 30-60 minutes on a standard laptop.

---

## Installation

### Prerequisites

- **Python**: 3.8 or higher
- **R**: 4.0 or higher (for statistical analyses)
- **Operating System**: Windows, macOS, or Linux
- **RAM**: 8 GB minimum, 16 GB recommended
- **Storage**: ~10 GB free space (for data and outputs)

### Python Environment Setup

We recommend using a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### R Environment Setup

Required R packages (install in R console):

```r
install.packages(c("lme4", "lmerTest", "emmeans", "ggplot2", "dplyr", "tidyr"))
```

---

## Repository Structure

```
From-Human-Heuristics-to-Human-AI-Teams/
│
├── README.md                          # This file
├── CODE_TO_PAPER_MAPPING.md          # Detailed code-to-paper mapping
├── DATA_README.md                     # Data dictionary and schema
├── requirements.txt                   # Python dependencies
├── figure_config.yaml                 # Standardized figure styling
│
├── Experiment-HumanHuman/             # Unity executable for human-human experiment
│   ├── FirstPersonHerding.exe
│   ├── FirstPersonHerding_Data/
│   └── ...
│
├── Experiment-HumanAA/                # Unity executables for human-AI experiments
│   ├── Heuristic/                     # DPMP-SCA model (main paper results)
│   ├── Model1HumanSensitivePlay/
│   ├── Model1SelfPlay/
│   └── ...
│
├── RAW_EXPERIMENT_DATA/               # Raw experimental data (download separately)
│   ├── TWO-HUMAN_HAs/                 # Experiment 1: Human-human pairs
│   │   ├── Session1001/
│   │   ├── Session1002/
│   │   └── ... (21 sessions)
│   └── HUMAN_AA_HAs/                  # Experiment 2: Human-AI pairs
│       └── ...
│
├── OtherResults/                      # Simulation data and analysis outputs
│   ├── AA-AA_SimulationData/          # Simulated agent trajectories
│   │   ├── CollinearAngle/            # SCA policy
│   │   ├── CollinearDistance/         # SCD policy
│   │   ├── Angle/                     # SA policy
│   │   ├── Distance/                  # SD policy
│   │   └── ContainmentZone/           # DCZ policy
│   ├── TS_Dynamic_Policy/             # Target selection time series
│   ├── AA_scores_traces/              # Binary trace overlap scores
│   └── binaryTraceOverlaps/           # Human-AI trace comparisons
│
└── Scripts/                           # Analysis scripts
    ├── README.md                      # Detailed pipeline instructions
    ├── figure_config.yaml             # Figure styling configuration
    │
    ├── tools/                         # Utility functions
    │   ├── __init__.py
    │   ├── utils.py                   # General utilities
    │   ├── traj_utils.py              # Trajectory analysis
    │   └── plot_utils.py              # Plotting functions
    │
    ├── Experiment 1 Pipeline:
    │   ├── get_actual_TS_Dynamic_Policy_as_csv.py
    │   ├── compare_dynamic_policies_by_TA_and_Participant_TS_DTW.py
    │   ├── DTW_TSp_and_Surrogate.py
    │   ├── binary_trace_evaluator_Exp1.py
    │   ├── exp1_TSOverlap_Analysis.ipynb
    │   ├── exp1_BinaryTrace_Analysis.ipynb
    │   └── mixed_linear_model_exp1.r
    │
    ├── Experiment 2 Pipeline:
    │   ├── get_actual_Dynamic_Policy_as_csv_Human-AA.py
    │   ├── calcAllDTW.py
    │   ├── convert_scores_exp2.py
    │   ├── traj_evals_binary_trace_scores.py
    │   ├── exp2_TargetOverlap_Analysis.ipynb
    │   ├── exp2_BinaryTrace_Analysis.ipynb
    │   └── R_Analysis_Exp2.R
    │
    └── simReader-AA_AA.ipynb          # Exploratory simulation analysis
```

---

## Data Download

### Experimental Data (Required)

**Download from Mendeley Data**: https://data.mendeley.com/datasets/kpxp5zkh5f/2

The data package includes:
- **Experiment 1**: 21 participant pairs × 24 trials = 504 trial files
- **Experiment 2**: 22 participants × 24 trials = 528 trial files
- **Simulation Data**: 5 policies × 21 simulated pairs × 24 trials = 2,520 simulation files

**Total size**: ~8 GB

**Installation Instructions**:
1. Download the data package from Mendeley
2. Extract the ZIP file
3. Place the extracted data folder in the project root directory
4. Verify the following structure exists:
   ```
   RAW_EXPERIMENT_DATA/
   ├── TWO-HUMAN_HAs/
   │   ├── Session1001/
   │   ├── Session1002/
   │   └── ...
   OtherResults/
   └── AA-AA_SimulationData/
       ├── CollinearAngle/
       ├── CollinearDistance/
       └── ...
   ```

### Data Verification

To verify your data download:

```python
import os
from pathlib import Path

# Check Experiment 1 data
exp1_path = Path("RAW_EXPERIMENT_DATA/TWO-HUMAN_HAs/")
num_sessions = len([d for d in exp1_path.iterdir() if d.is_dir()])
print(f"Experiment 1 sessions found: {num_sessions}/21")

# Check simulation data
sim_path = Path("OtherResults/AA-AA_SimulationData/CollinearAngle/")
if sim_path.exists():
    num_sim_sessions = len([d for d in sim_path.iterdir() if d.is_dir()])
    print(f"Simulation sessions found: {num_sim_sessions}/21")
else:
    print("ERROR: Simulation data not found!")
```

**Expected Output**:
```
Experiment 1 sessions found: 21/21
Simulation sessions found: 21/21
```

---

## Running the Analyses

### Experiment 1: Human-Human Baseline

**Research Question**: Which target-selection policy best captures human behavior?

#### Step 1: Target Selection Analysis

```bash
cd Scripts

# Extract target selection time series from human data
python get_actual_TS_Dynamic_Policy_as_csv.py

# Compute DTW overlap between human and simulated policies
python compare_dynamic_policies_by_TA_and_Participant_TS_DTW.py

# Analyze results and generate Figure 4 (top)
jupyter notebook exp1_TSOverlap_Analysis.ipynb

# Run statistical analysis (in R)
Rscript mixed_linear_model_exp1.r
```

**Outputs**:
- `OtherResults/TS_Dynamic_Policy/` - Target engagement time series
- `exp1_TSOverlap_Analysis.ipynb` - Figure 4 (top panel)
- Statistical tables showing SCA > DCZ (p < 0.05)

#### Step 2: Binary Trace Analysis

```bash
# Compute binary trace overlap scores
python binary_trace_evaluator_Exp1.py

# Analyze results and generate Figure 4 (bottom)
jupyter notebook exp1_BinaryTrace_Analysis.ipynb

# Run statistical analysis (same R script as above)
Rscript mixed_linear_model_exp1.r
```

**Outputs**:
- `OtherResults/AA_scores_traces/` - Binary trace overlap scores
- `exp1_BinaryTrace_Analysis.ipynb` - Figure 4 (bottom panel)
- Statistical tables showing SCA achieves >90% trajectory congruence

---

### Experiment 2: Human-AI Collaboration

**Research Question**: Can humans seamlessly coordinate with DPMP-SCA artificial agents?

#### Step 1: Target Selection Analysis

```bash
cd Scripts

# Extract target selection for human-AI pairs
python get_actual_Dynamic_Policy_as_csv_Human-AA.py

# Compute DTW overlap (3-way comparison: AI, Human, Surrogate)
python calcAllDTW.py

# Format data for statistical analysis
python convert_scores_exp2.py

# Analyze results and generate Figure 5 (top)
jupyter notebook exp2_TargetOverlap_Analysis.ipynb

# Run statistical analysis (in R)
Rscript R_Analysis_Exp2.R
```

**Outputs**:
- `OtherResults/TS_Dynamic_Policy/Human-AA/` - Target engagement time series
- `exp2_TargetOverlap_Analysis.ipynb` - Figure 5 (top panel)
- Statistical tables showing Artificial > Human (p < .001)

#### Step 2: Binary Trace Analysis

```bash
# Compute binary trace scores for human-AI pairs
python traj_evals_binary_trace_scores.py

# Format data for statistical analysis
python convert_scores_exp2.py

# Analyze results and generate Figure 5 (bottom)
jupyter notebook exp2_BinaryTrace_Analysis.ipynb

# Run statistical analysis (same R script as above)
Rscript R_Analysis_Exp2.R
```

**Outputs**:
- `OtherResults/binaryTraceOverlaps/` - Binary trace overlap scores
- `exp2_BinaryTrace_Analysis.ipynb` - Figure 5 (bottom panel)
- Statistical tables showing no difference Human vs. Surrogate (p > .25)

---

## Reproducing Paper Figures

All figures use consistent styling defined in `Scripts/figure_config.yaml`.

### Figure 2: Task Environment
- **Source**: Unity game screenshots
- **Reproduction**: Screen captures from `Experiment-HumanHuman/FirstPersonHerding.exe`

### Figure 3: Example Trajectories and Binary Traces
- **Notebook**: `Scripts/exp1_BinaryTrace_Analysis.ipynb`
- **Section**: "Trajectory Visualization"
- **Trial**: First experimental trial (trial #7) for each participant

### Figure 4: Experiment 1 Results
- **Top Panel** (Target Selection Overlap): `Scripts/exp1_TSOverlap_Analysis.ipynb`
- **Bottom Panel** (Binary Trace Overlap): `Scripts/exp1_BinaryTrace_Analysis.ipynb`
- **Format**: Box plots with 5 policies × 3 target conditions

### Figure 5: Experiment 2 Results
- **Top Panel** (Target Selection Overlap): `Scripts/exp2_TargetOverlap_Analysis.ipynb`
- **Bottom Panel** (Binary Trace Overlap): `Scripts/exp2_BinaryTrace_Analysis.ipynb`
- **Format**: Box plots with 3 agent types × 3 target conditions

**Note**: To ensure figures match the paper exactly, make sure `figure_config.yaml` settings are loaded in each notebook.

---

## Code-to-Paper Mapping

For a detailed mapping of code to specific paper sections, figures, and statistical results, see:

**[CODE_TO_PAPER_MAPPING.md](CODE_TO_PAPER_MAPPING.md)**

This document includes:
- Table mapping paper sections to code files
- Step-by-step reproduction instructions for each result
- Expected outputs and statistical values
- Troubleshooting common issues

---

## Key Model Parameters

### DPMP Navigation Model (Equation 4)

```python
# Integration parameters
dt = 0.02  # seconds (50 Hz sampling rate)

# Damping
b = 0.2  # s^-1

# Stiffness coefficients (values from bin Kamruddin et al., 2024)
kg = ?  # Goal attraction
ko = ?  # Obstacle repulsion

# Distance modulation
c1, c2, c3, c4 = ?  # Constants (see source paper)
```

### Target Selection Policy (SCA - Table 1 in paper)

```python
# Thresholds
COLLINEAR_THRESHOLD = 20  # degrees
INFLUENCE_RADIUS = 10     # meters (di in Eq. 3)

# Timing
DECISION_DELAY = 0.25     # seconds between decisions
POST_CONTAIN_DELAY = 1.0  # seconds after target contained
```

---

## Troubleshooting

### Common Issues

**Issue 1: "File not found" errors**
- **Cause**: Data not downloaded or in wrong location
- **Solution**: Verify data structure using verification script above

**Issue 2: Path errors on Windows**
- **Cause**: Some scripts use Unix-style paths
- **Solution**: We're working on cross-platform compatibility. For now, run in Git Bash or WSL

**Issue 3: Figures look different from paper**
- **Cause**: matplotlib version or settings mismatch
- **Solution**: Ensure `figure_config.yaml` is loaded in notebooks

**Issue 4: R script errors**
- **Cause**: Missing R packages
- **Solution**: Install all packages listed in [Installation](#installation)

### Getting Help

If you encounter problems:
1. Check the [CODE_TO_PAPER_MAPPING.md](CODE_TO_PAPER_MAPPING.md) troubleshooting section
2. Review the [DATA_README.md](DATA_README.md) for data format details
3. Open an issue on GitHub with:
   - Operating system
   - Python version (`python --version`)
   - Error message (full traceback)
   - Which script/notebook you're running

---

## Citation

If you use this code or data in your research, please cite:

```bibtex
@article{binkamruddin2025human,
  title={From human heuristics to human--AI teams: Modeling multiagent first-person herding using dynamical perceptual--motor primitives},
  author={bin Kamruddin, Ayman and Lam, Christopher and Ghanem, Sala and Patil, Gaurav and Musolesi, Mirco and di Bernardo, Mario and Richardson, Michael J},
  journal={[Manuscript submitted for publication]},
  year={2025}
}
```

**Data Citation**:
```
bin Kamruddin, A., Lam, C., Ghanem, S., Patil, G., Musolesi, M., di Bernardo, M., & Richardson, M. J. (2024).
From Human Heuristics to Human-AI Teams: Multi-agent Herding Data [Dataset].
Mendeley Data. https://data.mendeley.com/datasets/kpxp5zkh5f/2
```

---

## Authors

- **Ayman bin Kamruddin**¹'² - Lead developer and first author
- **Christopher Lam**³ - Data collection
- **Sala Ghanem**³ - Data collection
- **Gaurav Patil**³ - Model development
- **Mirco Musolesi**⁴ - Supervision
- **Mario di Bernardo**¹'² - Supervision
- **Michael J. Richardson**³ - Principal investigator

¹Scuola Superiore Meridionale (Italy)
²University of Naples Federico II (Italy)
³School of Psychological Sciences, Macquarie University (Australia)
⁴Performance and Expertise Research Center, Macquarie University (Australia)
⁵University College London (UK)

---

## Funding

This work was supported by:
- PhD fellowship for Dr. bin Kamruddin in Modelling and Engineering Risk and Complexity from the Scuola Superiore Meridionale (Naples, Italy)
- Australian Department of Defence—Defence Science and Technology Group's Human Performance Research Network (HPRnet)
- Centre for Advanced Defence Research in Robotics and Autonomous Systems (CADR-RAS)
- Australian Research Council Future Fellowship (FT180100447) awarded to Prof. Richardson

---

## License

[Specify license here - check with lab policy]

**Suggested**: MIT License or Creative Commons BY 4.0

---

## Changelog

### Version 1.0 (2025-09-30)
- Initial public release
- Code refactoring for reproducibility
- Added comprehensive documentation
- Created figure configuration system

---

## Acknowledgments

We thank Hanna Sandison, Dr. Elliot Saltzman, Prof. Benoît G. Bardy, and Dr. Simon Hosking for assistance and helpful comments on this work.

---

*For questions about the code or data, please open an issue on GitHub or contact the corresponding author.*

**Corresponding Author**: Michael J. Richardson (michael.richardson@mq.edu.au)