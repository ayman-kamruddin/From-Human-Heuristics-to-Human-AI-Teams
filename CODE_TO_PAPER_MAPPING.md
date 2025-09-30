# Code to Paper Mapping

This document maps the code in this repository to specific sections, figures, and results in the published manuscript:

**bin Kamruddin, A., Lam, C., Ghanem, S., Patil, G., Musolesi, M., di Bernardo, M., & Richardson, M. J. From human heuristics to human–AI teams: Modeling multiagent first-person herding using dynamical perceptual–motor primitives. *Journal of Experimental Psychology: Human Perception and Performance***

---

## Quick Reference Table

| Paper Section | Figure/Table | Code Location | Key Scripts |
|--------------|--------------|---------------|-------------|
| Experiment 1 Methods | Figure 2 | `Experiment-HumanHuman/` | Unity game executable |
| Experiment 1 Results | Figure 3 | `Scripts/exp1_*_Analysis.ipynb` | `binary_trace_evaluator_Exp1.py` |
| Experiment 1 Results | Figure 4 (top) | `Scripts/exp1_TSOverlap_Analysis.ipynb` | `get_actual_TS_Dynamic_Policy_as_csv.py`, `compare_dynamic_policies_by_TA_and_Participant_TS_DTW.py` |
| Experiment 1 Results | Figure 4 (bottom) | `Scripts/exp1_BinaryTrace_Analysis.ipynb` | `binary_trace_evaluator_Exp1.py` |
| Experiment 1 Statistics | Table 1 | `Scripts/mixed_linear_model_exp1.r` | R mixed-effects models |
| Experiment 2 Results | Figure 5 (top) | `Scripts/exp2_TargetOverlap_Analysis.ipynb` | `get_actual_Dynamic_Policy_as_csv_Human-AA.py`, `calcAllDTW.py` |
| Experiment 2 Results | Figure 5 (bottom) | `Scripts/exp2_BinaryTrace_Analysis.ipynb` | `traj_evals_binary_trace_scores.py` |
| Experiment 2 Statistics | Table 2 | `Scripts/R_Analysis_Exp2.R` | R mixed-effects models |

---

## Detailed Mapping

### **Experiment 1: Human-Human Baseline**

#### Methods Section

**Task Environment (Figure 2)**
- **Figure 2a**: First-person view screenshot
  - Source: `Experiment-HumanHuman/FirstPersonHerding.exe` (Unity game)
  - Screen capture during gameplay

- **Figure 2b**: Birds-eye view of game field
  - Source: Unity editor view (not directly reproducible from data)
  - Illustrative diagram

**Participants & Procedure**
- N = 21 pairs (42 participants)
- Data location: `RAW_EXPERIMENT_DATA/TWO-HUMAN_HAs/`
- Session folders: `Session1001` through `Session1021`
- Each session contains 24 trial CSV files

#### Analysis Pipeline - Target Selection (Figure 4, top)

**Paper Result**: "*the SCA and SCD policies were overall more representative of human data than the other three policies*"

**Analysis Steps**:

1. **Extract Target Selection Policies** (Human data)
   ```
   Script: Scripts/get_actual_TS_Dynamic_Policy_as_csv.py
   Input:  RAW_EXPERIMENT_DATA/TWO-HUMAN_HAs/Session*/ExperimentData/*.csv
   Output: OtherResults/TS_Dynamic_Policy/Human/Session*/trialIdentifier_*.csv
   ```
   - Determines which target each herder is engaging at each timepoint
   - Produces binary-encoded engagement time series

2. **Generate Simulated Target Selection Policies** (5 policies tested)
   ```
   Policies: CollinearAngle (SCA), CollinearDistance (SCD), Angle (SA),
             Distance (SD), ContainmentZone (DCZ)
   Simulation data: OtherResults/AA-AA_SimulationData/[PolicyName]/
   Output: OtherResults/TS_Dynamic_Policy/Simulation/[PolicyName]/
   ```
   - Same script processes simulation data (see `simulation_bool` flag in code)

3. **Compute DTW Overlap Scores**
   ```
   Script: Scripts/compare_dynamic_policies_by_TA_and_Participant_TS_DTW.py
   Input:  TS_Dynamic_Policy outputs from steps 1 & 2
   Output: Normalized DTW distance → target selection overlap scores
   ```
   - Compares each policy's target selection sequence to human data
   - Uses Dynamic Time Warping to handle different trial lengths
   - Produces overlap percentage (1.0 = perfect match)

4. **Statistical Analysis & Visualization**
   ```
   Notebook: Scripts/exp1_TSOverlap_Analysis.ipynb
   R Script: Scripts/mixed_linear_model_exp1.r
   Output:   Figure 4 (top panel) - box plots of target selection overlap
   ```
   - Mixed-effects linear model: overlap ~ policy × target_number + (1|pair)
   - Post-hoc comparisons with Tukey HSD correction
   - **Key Finding**: SCA > DCZ (p < 0.05); SCD > DCZ (p < 0.05)

#### Analysis Pipeline - Movement Trajectories (Figure 4, bottom)

**Paper Result**: "*the DPMP-SCA agent matched or exceeded human baselines in goal-selection overlap (> 90%) and produced movement paths nearly indistinguishable from human partners (> 92% trajectory congruence)*"

**Analysis Steps**:

1. **Compute Binary Trace Maps** (Human trajectories)
   ```
   Script: Scripts/binary_trace_evaluator_Exp1.py
   Input:  RAW_EXPERIMENT_DATA/TWO-HUMAN_HAs/Session*/ExperimentData/*.csv
   Method:
     - Bin game field into 5m × 5m spatial bins
     - Apply square-root filter to spatial frequencies
     - Threshold at cutoff = 10 to create binary map
   Output: Per-session binary trace maps (90% confidence interval of trajectories)
   ```

2. **Evaluate Simulation Trajectories Against Human Maps**
   ```
   Script: Scripts/binary_trace_evaluator_Exp1.py (continued)
   Input:  OtherResults/AA-AA_SimulationData/[PolicyName]/*.csv
   Output: OtherResults/AA_scores_traces/AA_scores_traces_Successive[PolicyName].csv
   ```
   - For each simulated agent, calculate % of trajectory within binary trace map
   - Leave-one-out analysis: exclude each participant pair when creating map

3. **Statistical Analysis & Visualization**
   ```
   Notebook: Scripts/exp1_BinaryTrace_Analysis.ipynb
   R Script: Scripts/mixed_linear_model_exp1.r
   Output:   Figure 4 (bottom panel) - box plots of binary trace overlap
   ```
   - Mixed-effects linear model: overlap ~ policy × target_number + (1|pair/player)
   - **Key Finding**: SCA and SCD achieve >90% trajectory overlap with human data

**Figure 3**: Example trajectory visualization
```
Notebook: Scripts/exp1_BinaryTrace_Analysis.ipynb
Shows:    - Participant trajectories (gray lines)
          - Simulated trajectories (red lines)
          - Weighted trace heatmap
          - Binary trace map
Trial:    First experimental trial (trial #7) for illustration
```

---

### **Experiment 2: Human-AI Collaboration**

#### Methods Section

**Participants & Procedure**
- N = 22 human participants paired with AI agent
- Data location: `RAW_EXPERIMENT_DATA/HUMAN_AA_HAs/` (inferred, check Mendeley data)
- AI agent controlled by DPMP model (Eq. 4) + SCA target selection policy

#### Analysis Pipeline - Target Selection (Figure 5, top)

**Paper Result**: "*the AHA's SCA-driven selection overlap matched or exceeded human baseline performance*"

**Analysis Steps**:

1. **Extract Target Selection Policies** (Human-AI pairs)
   ```
   Script: Scripts/get_actual_Dynamic_Policy_as_csv_Human-AA.py
   Input:  RAW_EXPERIMENT_DATA/HUMAN_AA_HAs/[AgentType]/*.csv
          Where AgentType = Heuristic, Model1HumanSensitivePlay, Model2SelfPlay, etc.
   Output: OtherResults/TS_Dynamic_Policy/Human-AA/[AgentType]/
   ```
   - Processes both human player and AI agent engagement sequences
   - Note: Paper focuses on "Heuristic" agent (= DPMP-SCA model)

2. **Compute DTW Overlap Scores** (Three comparisons)
   ```
   Script: Scripts/calcAllDTW.py
   Outputs:
     a) AA_scores_heur.csv     - AI agent vs. Exp1 human-human baseline
     b) human_scores_heur.csv  - Human partner vs. Exp1 human-human baseline
     c) humanTeamDTWs.csv      - Surrogate: Exp1 human vs. itself (leave-one-out)
   ```

3. **Format Data for Statistical Analysis**
   ```
   Script: Scripts/convert_scores_exp2.py
   Input:  DTW overlap scores from step 2
   Output: Reformatted CSVs for R analysis
   ```

4. **Statistical Analysis & Visualization**
   ```
   Notebook: Scripts/exp2_TargetOverlap_Analysis.ipynb
   R Script: Scripts/R_Analysis_Exp2.R
   Output:   Figure 5 (top panel) - box plots comparing agent types
   ```
   - Mixed-effects linear model: overlap ~ agent_type × target_number + (1|pair)
   - **Key Finding**: Artificial > Human (p < .001); Artificial > Surrogate (p < .001)
   - Note: AI agent deterministic, so higher consistency than variable humans

#### Analysis Pipeline - Movement Trajectories (Figure 5, bottom)

**Paper Result**: "*binary trace overlap scores were significantly higher for the 5-target conditions*"

**Analysis Steps**:

1. **Compute Binary Trace Scores** (Human-AI pairs vs. Exp1 maps)
   ```
   Script: Scripts/traj_evals_binary_trace_scores.py
   Input:
     - RAW_EXPERIMENT_DATA/HUMAN_AA_HAs/[AgentType]/*.csv (Exp2 trajectories)
     - Binary trace maps computed from RAW_EXPERIMENT_DATA/TWO-HUMAN_HAs/ (Exp1)
   Output: OtherResults/binaryTraceOverlaps/
     - AA_scores_heur.csv     (AI agent trace overlap)
     - human_scores_heur.csv  (Human partner trace overlap)
     - humanTeamTraces.csv    (Surrogate baseline)
   ```

2. **Format Data for Statistical Analysis**
   ```
   Script: Scripts/convert_scores_exp2.py
   (Same script as target selection, different input files)
   ```

3. **Statistical Analysis & Visualization**
   ```
   Notebook: Scripts/exp2_BinaryTrace_Analysis.ipynb
   R Script: Scripts/R_Analysis_Exp2.R
   Output:   Figure 5 (bottom panel) - box plots comparing agent types
   ```
   - Mixed-effects linear model: overlap ~ agent_type × target_number + (1|pair)
   - **Key Finding**: No difference Human vs. Surrogate (p > .25)
     - i.e., humans behaved naturally when paired with AI

---

## Supporting Analyses

### Simulation Data Exploration

**Purpose**: Understand simulated agent trajectories before analysis
```
Notebook: Scripts/simReader-AA_AA.ipynb
Input:    OtherResults/AA-AA_SimulationData/
Output:   Exploratory plots (not in paper)
```

### Utility Functions

**Trajectory Analysis**
- `Scripts/tools/traj_utils.py` - Binary trace computation
- `Scripts/tools/utils.py` - Distance calculations, angle functions, target engagement detection

**Plotting**
- `Scripts/tools/plot_utils.py` - Standardized plotting functions (check for consistency!)

---

## Statistical Models in Detail

### Experiment 1 Mixed Model
```r
# File: Scripts/mixed_linear_model_exp1.r

# Target Selection Model
model_ts <- lmer(overlap ~ policy * target_number + (1|pair), data = data_ts)
# Fixed effects: policy (5 levels), target_number (3, 4, 5)
# Random effects: random intercept per participant pair

# Binary Trace Model
model_bt <- lmer(overlap ~ policy * target_number + (1|pair/player), data = data_bt)
# Fixed effects: same as above
# Random effects: player nested within pair
```

### Experiment 2 Mixed Model
```r
# File: Scripts/R_Analysis_Exp2.R

# Target Selection Model
model_ts <- lmer(overlap ~ agent_type * target_number + (1|pair), data = data_ts)
# Fixed effects: agent_type (Human, Artificial, Surrogate), target_number
# Random effects: random intercept per pair

# Binary Trace Model
model_bt <- lmer(overlap ~ agent_type * target_number + (1|pair), data = data_bt)
# Same structure as target selection
```

---

## Key Model Parameters

### DPMP Navigation Model (Equation 4 in paper)
```python
# Model parameters used in simulations (from bin Kamruddin et al., 2024)
# File: OtherResults/AA-AA_SimulationData/[PolicyName]/

b = 0.2              # Damping coefficient (s^-1)
kg = ?               # Goal attraction stiffness (check source paper)
ko = ?               # Obstacle repulsion stiffness (check source paper)
c1, c2, c3, c4 = ?   # Distance modulation constants (check source paper)

# Integration timestep
dt = 0.02  # seconds (50 Hz)
```

### Target Selection Policies
```python
# File: Scripts/get_actual_TS_Dynamic_Policy_as_csv.py

# SCA Policy (Table 1 in paper)
COLLINEAR_THRESHOLD = 20  # degrees
DECISION_DELAY = 0.25     # seconds between decisions
POST_CONTAIN_DELAY = 1.0  # seconds after target contained

# Target engagement distance
INFLUENCE_RADIUS = 10  # meters (di in paper)
```

---

## Reproducing Specific Paper Results

### Main Effect: SCA Policy Superiority (Exp1)

**Paper Statement**: "*SCA and SCD policies exhibited significantly better target selection overlap compared to the SCZ policy (all p < 0.05)*"

**To Reproduce**:
1. Run complete Exp1 pipeline (target selection analysis)
2. Open `exp1_TSOverlap_Analysis.ipynb`
3. Look for post-hoc comparison table
4. Verify SCA vs. DCZ contrast

**Expected Output**: SCA mean ≈ 0.950, DCZ mean ≈ 0.925, p < 0.05

### Main Effect: Human-AI Equivalence (Exp2)

**Paper Statement**: "*there was no difference in binary trace overlap between human co-herders and the surrogate human data (both p > .25)*"

**To Reproduce**:
1. Run complete Exp2 pipeline (binary trace analysis)
2. Open `exp2_BinaryTrace_Analysis.ipynb`
3. Look for post-hoc comparison: Human vs. Surrogate
4. Verify p-value > 0.25

**Expected Output**: Human mean ≈ 0.80, Surrogate mean ≈ 0.82, p > 0.25

---

## Data Provenance

### Raw Experimental Data
- **Source**: Collected 2023-2024 at Macquarie University
- **Ethics Approval**: Macquarie University Human Research Ethics Committee
- **Storage**: Mendeley Data (DOI: https://data.mendeley.com/datasets/kpxp5zkh5f/2)
- **Format**: CSV files with 50 Hz sampling rate

### Simulated Data
- **Generation Method**: DPMP model (Eq. 4) implemented in Unity
- **Parameters**: From bin Kamruddin et al. (2024)
- **Location**: `OtherResults/AA-AA_SimulationData/`
- **Policies Generated**: 5 target selection policies × 21 simulated pairs × 24 trials

---

## Troubleshooting Common Issues

### Issue: "File not found" errors in scripts
**Solution**: Ensure data folder from Mendeley is placed in project root directory

### Issue: Figures don't match paper exactly
**Solution**:
1. Check that you're using `figure_config.yaml` settings
2. Verify R package versions match (see `requirements.txt`)
3. Ensure matplotlib settings are consistent

### Issue: DTW scores differ slightly from paper
**Solution**: Check that you're using correct:
- Trial range (7-24 for Exp1 analysis, excluding practice trials 1-6)
- Leave-one-out surrogate method
- Normalization: DTW distance / (length1 × length2)

---

## Questions or Issues?

If you encounter problems reproducing results:
1. Check this mapping document first
2. Verify data download is complete (see `DATA_README.md`)
3. Review the paper's Methods section for additional details
4. Open an issue on GitHub with:
   - Which paper result you're trying to reproduce
   - What output you're getting
   - Error messages (if any)

---

## Citation

If you use this code, please cite:

```
bin Kamruddin, A., Lam, C., Ghanem, S., Patil, G., Musolesi, M., di Bernardo, M., & Richardson, M. J. (n.d.).
From human heuristics to human–AI teams: Modeling multiagent first-person herding using dynamical
perceptual–motor primitives [Manuscript submitted for publication].
```

---

*Last updated: 2025-09-30*
*Corresponds to manuscript version submitted to JEP: HPP*