# Data Dictionary and Schema

This document describes the structure, format, and contents of all data files in this repository.

---

## Table of Contents

- [Overview](#overview)
- [File Naming Conventions](#file-naming-conventions)
- [Data Files Structure](#data-files-structure)
- [Column Definitions](#column-definitions)
- [Data Collection Procedures](#data-collection-procedures)
- [Data Quality and Validation](#data-quality-and-validation)
- [Accessing the Data](#accessing-the-data)

---

## Overview

### Data Collection Summary

- **Experiment 1** (Human-Human):
  - **N = 21 participant pairs** (42 individuals)
  - **24 trials per pair** (6 practice + 18 experimental)
  - **3 target conditions**: 3, 4, or 5 targets per trial
  - **Total trial files**: 21 pairs × 24 trials = 504 files

- **Experiment 2** (Human-AI):
  - **N = 22 human participants**
  - **24 trials per participant** (6 practice + 18 experimental)
  - **AI agent types**: Heuristic (DPMP-SCA), Model1/2 HumanSensitivePlay, Model1/2 SelfPlay
  - **Total trial files**: 22 participants × 24 trials = 528 files

- **Simulation Data**:
  - **5 target-selection policies**: CollinearAngle (SCA), CollinearDistance (SCD), Angle (SA), Distance (SD), ContainmentZone (DCZ)
  - **21 simulated pairs** per policy (matching human sample size)
  - **24 trials per pair**
  - **Total simulation files**: 5 policies × 21 pairs × 24 trials = 2,520 files

### Data Format

- **File Type**: CSV (Comma-Separated Values)
- **Sampling Rate**: 50 Hz (0.02 second intervals)
- **Coordinate System**: Cartesian (X, Z horizontal plane; Y vertical)
- **Origin**: Center of the containment zone (0, 0)
- **Game Field Size**: 120m × 90m
- **Containment Zone**: Circular, radius = 4m, centered at (0, 0)

---

## File Naming Conventions

### Experiment 1: Human-Human Data

**Pattern**: `FirstPersonHerding_session[SessionID]_[Player1ID]_[Player2ID]__trialIdentifier[TrialID]_trialOrder[Order]_[Timestamp].csv`

**Example**: `FirstPersonHerding_session1001_1001_2001__trialIdentifier14_trialOrder10_2023314_155756.csv`

**Components**:
- `SessionID`: 1001-1021 (21 sessions)
- `Player1ID`, `Player2ID`: Unique participant identifiers
- `TrialID`: 01-24 (zero-padded)
  - Trials 01-06: Practice (excluded from analysis)
  - Trials 07-24: Experimental (N=18 trials, 6 per target condition)
- `Order`: Randomized trial presentation order (01-24)
- `Timestamp`: YYYYMMDDHHmmss format

**Directory Structure**:
```
RAW_EXPERIMENT_DATA/TWO-HUMAN_HAs/
├── Session1001/
│   └── ExperimentData/
│       ├── FirstPersonHerding_session1001_..._trialIdentifier01_....csv
│       ├── FirstPersonHerding_session1001_..._trialIdentifier02_....csv
│       └── ... (24 files)
├── Session1002/
│   └── ExperimentData/
│       └── ... (24 files)
└── ... (21 sessions total)
```

### Experiment 2: Human-AI Data

**Pattern**: `FirstPersonHerding_session[SessionID]_[PlayerID]_[AgentID]__trialIdentifier[TrialID]_trialOrder[Order]_[Timestamp].csv`

**Directory Structure**:
```
RAW_EXPERIMENT_DATA/HUMAN_AA_HAs/
├── Heuristic/              # DPMP-SCA model (main paper results)
│   ├── Session2001/
│   │   └── ExperimentData/
│   └── ... (22 sessions)
├── Model1HumanSensitivePlay/
│   └── ... (22 sessions)
├── Model1SelfPlay/
│   └── ... (22 sessions)
└── ... (other agent types)
```

### Simulation Data

**Pattern**: `FirstPersonHerding_session[SimID]_..._trialIdentifier[TrialID]_....csv`

**Directory Structure**:
```
OtherResults/AA-AA_SimulationData/
├── CollinearAngle/         # SCA policy
│   ├── Session_Sim_001/
│   │   └── ExperimentData/
│   └── ... (21 simulated pairs)
├── CollinearDistance/      # SCD policy
│   └── ... (21 simulated pairs)
├── Angle/                  # SA policy
│   └── ... (21 simulated pairs)
├── Distance/               # SD policy
│   └── ... (21 simulated pairs)
└── ContainmentZone/        # DCZ policy
    └── ... (21 simulated pairs)
```

---

## Data Files Structure

### CSV Format

Each trial CSV contains time-series data with **one row per frame** (50 Hz sampling).

**Column Count**:
- **3 targets**: 50 columns
- **4 targets**: 63 columns
- **5 targets**: 76 columns

(Columns increase by 13 per additional target: position (3), orientation (4), velocity (3), containment status (1), running status (1), timing (1))

### Header Row

The first row contains column names (see [Column Definitions](#column-definitions)).

### Data Rows

- **Typical trial length**: 10-60 seconds (500-3000 rows at 50 Hz)
- **Data types**:
  - Positions, velocities: `float`
  - Quaternions: `float` (normalized, magnitude = 1)
  - Booleans: `True`/`False` (Python boolean strings)
  - Time: `float` (seconds since experiment start)

---

## Column Definitions

### Player/Herder Agent (HA) Columns

Each herder (2 total: p0 and p1) has the following columns:

| Column Pattern | Type | Units | Description |
|---------------|------|-------|-------------|
| `p[N]x` | float | meters | X position (horizontal, East-West) |
| `p[N]y` | float | meters | Y position (vertical, up-down) - always 1.0 for ground level |
| `p[N]z` | float | meters | Z position (horizontal, North-South) |
| `p[N]xq` | float | - | Orientation quaternion X component |
| `p[N]yq` | float | - | Orientation quaternion Y component (heading direction) |
| `p[N]zq` | float | - | Orientation quaternion Z component |
| `p[N]wq` | float | - | Orientation quaternion W component |

**Notes**:
- `N` = 0 or 1 (Player 0 or Player 1)
- For simulations, column prefix changes to `hA[N]` (e.g., `hA0x`, `hA1z`)
- Y-coordinate is always 1.0 (all entities at ground level)
- Quaternion (xq, yq, zq, wq) represents 3D rotation; convert to Euler angles using `scipy.spatial.transform.Rotation`

**Example**:
```
p0x = 6.824507   # Player 0 is 6.8m east of center
p0y = 1.0        # Ground level
p0z = 31.97111   # Player 0 is 32m north of center
p0yq = 0.6786    # Heading rotation component
```

### Target Agent (TA) Columns

Each target (up to 5: t0, t1, t2, t3, t4) has the following columns:

| Column Pattern | Type | Units | Description |
|---------------|------|-------|-------------|
| `t[N]x` | float | meters | X position |
| `t[N]y` | float | meters | Y position (always 0.5) |
| `t[N]z` | float | meters | Z position |
| `t[N]xq` | float | - | Orientation quaternion X |
| `t[N]yq` | float | - | Orientation quaternion Y |
| `t[N]zq` | float | - | Orientation quaternion Z |
| `t[N]wq` | float | - | Orientation quaternion W |
| `t[N]xv` | float | m/s | X velocity component |
| `t[N]yv` | float | m/s | Y velocity component (usually ~0) |
| `t[N]zv` | float | m/s | Z velocity component |
| `t[N]ct` | bool | - | **Currently in containment zone** (True/False) |
| `t[N]run` | bool | - | **Currently being repulsively influenced** (True/False) |

**Notes**:
- `N` = 0, 1, 2, 3, or 4 (Target ID)
- Not all trials have all targets (check for missing columns)
- TAs have Y = 0.5 (slightly lower than HAs at Y = 1.0)
- `t[N]run = True` when any HA is within 10m influence radius (see Equation 3 in paper)
- `t[N]ct = True` when TA is stationary within containment zone

**Example**:
```
t0x = -15.78733   # Target 0 is 15.8m west of center
t0z = -30.09593   # Target 0 is 30.1m south of center
t0run = False     # Not currently being influenced by herder
t0ct = False      # Not in containment zone
```

### Containment Zone Columns

| Column | Type | Units | Description |
|--------|------|-------|-------------|
| `cZxpos` | float | meters | Containment zone X position (always 0) |
| `cZy` | float | meters | Containment zone Y position (always 0.2) |
| `cZz` | float | meters | Containment zone Z position (always 0) |

**Notes**:
- Containment zone is always centered at (0, 0.2, 0)
- Radius = 4 meters (fixed)
- Y = 0.2 for visual floor indicator

### Time Column

| Column | Type | Units | Description |
|--------|------|-------|-------------|
| `time` | float | seconds | Time elapsed since experiment session start |

**Notes**:
- Increases by ~0.02 seconds per row (50 Hz sampling)
- May have slight jitter due to game engine timing
- Used to synchronize events across trials

---

## Data Collection Procedures

### Experiment 1: Human-Human

**Apparatus**:
- Unity-based first-person herding game (`Experiment-HumanHuman/FirstPersonHerding.exe`)
- 27-inch monitor (1920×1080p)
- Keyboard (WASD movement) + Mouse (head rotation)

**Procedure**:
1. Participants completed 5 single-herder practice trials (data not included)
2. Pairs completed 6 multi-player practice trials (Trials 01-06, excluded from analysis)
3. Pairs completed 18 experimental trials (Trials 07-24, analyzed in paper)
   - 6 trials with 3 targets
   - 6 trials with 4 targets
   - 6 trials with 5 targets
   - Trial order randomized across pairs

**Trial Structure**:
- **Start**: All HAs and TAs stationary at predetermined positions
- **Gameplay**: HAs navigate to influence and corral TAs into containment zone
- **End**: All TAs stationary within containment zone

**Data Recording**:
- Continuous recording at 50 Hz throughout trial
- Position, orientation, velocity updated every frame
- `t[N]run` and `t[N]ct` status updated based on game physics

### Experiment 2: Human-AI

**Differences from Experiment 1**:
- One human participant paired with one artificial agent
- AI agent controlled by DPMP model (Equation 4) + target-selection policy
- Human participants naive to AI agent behavior
- Multiple AI agent types tested (only Heuristic/DPMP-SCA reported in paper)

**AI Agent**:
- **Navigation**: DPMP model with parameters from bin Kamruddin et al. (2024)
- **Decision**: SCA target-selection policy (Table 1 in paper)
- **Integration**: 50 Hz update rate, same as human input

### Simulation Data

**Generation**:
- Unity environment with two DPMP-controlled agents
- Each policy (SCA, SCD, SA, SD, DCZ) simulated separately
- Same initial conditions as Experiment 1 (21 × 24 trials)

**Purpose**:
- Evaluate trajectory congruence between human and model
- Compare different target-selection policies

---

## Data Quality and Validation

### Data Integrity Checks

**Verify data download**:
```python
from pathlib import Path
import pandas as pd

# Check file count
exp1_path = Path("RAW_EXPERIMENT_DATA/TWO-HUMAN_HAs/")
sessions = list(exp1_path.glob("Session*/ExperimentData/*.csv"))
print(f"Experiment 1 files: {len(sessions)}/504")

# Check data structure (sample file)
sample = pd.read_csv(sessions[0])
print(f"Columns: {len(sample.columns)}")
print(f"Rows: {len(sample)}")
print(f"Sampling rate: {1 / sample['time'].diff().median():.1f} Hz")
```

**Expected Output**:
```
Experiment 1 files: 504/504
Columns: 50, 63, or 76 (depending on target number)
Rows: 500-3000 (10-60 seconds at 50 Hz)
Sampling rate: ~50 Hz
```

### Known Data Issues

1. **Missing Columns**:
   - Some 3-target trials may not have `t3*` or `t4*` columns (expected)
   - Check for column existence before accessing: `if 't3x' in df.columns:`

2. **Slight Timing Jitter**:
   - Sampling rate may vary between 49-51 Hz due to game engine
   - Use `time` column for precise synchronization, not row count

3. **Quaternion Sign Ambiguity**:
   - Quaternions q and -q represent the same rotation
   - When comparing orientations, consider both q and -q

4. **Velocity Spikes**:
   - Occasional velocity spikes due to Unity physics engine
   - Consider smoothing or filtering velocities if analyzing acceleration

5. **Practice Trials**:
   - Trials 01-06 are practice and EXCLUDED from all analyses
   - Only analyze Trials 07-24 (trialIdentifier 07-24)

---

## Accessing the Data

### Download

**Mendeley Data**: https://data.mendeley.com/datasets/kpxp5zkh5f/2

**File Size**: ~8 GB compressed

**DOI**: [To be assigned upon publication]

### Loading Data in Python

```python
import pandas as pd
from pathlib import Path

# Load a single trial
trial_path = Path("RAW_EXPERIMENT_DATA/TWO-HUMAN_HAs/Session1001/ExperimentData")
trial_file = list(trial_path.glob("*trialIdentifier07*"))[0]
df = pd.read_csv(trial_file)

# Get trial info
num_targets = sum(1 for col in df.columns if col.startswith('t') and col.endswith('x'))
duration = df['time'].iloc[-1] - df['time'].iloc[0]
print(f"Targets: {num_targets}, Duration: {duration:.1f}s, Rows: {len(df)}")

# Extract herder positions
p0_x = df['p0x'].values
p0_z = df['p0z'].values
p1_x = df['p1x'].values
p1_z = df['p1z'].values

# Extract target positions (check if target exists)
if 't0x' in df.columns:
    t0_x = df['t0x'].values
    t0_z = df['t0z'].values
    t0_running = df['t0run'].values
    t0_contained = df['t0ct'].values
```

### Loading Data in R

```r
library(readr)

# Load trial
trial_path <- "RAW_EXPERIMENT_DATA/TWO-HUMAN_HAs/Session1001/ExperimentData/"
trial_file <- list.files(trial_path, pattern = "trialIdentifier07", full.names = TRUE)[1]
df <- read_csv(trial_file)

# Extract positions
p0_x <- df$p0x
p0_z <- df$p0z

# Check target count
num_targets <- sum(grepl("^t[0-9]x$", colnames(df)))
print(paste("Number of targets:", num_targets))
```

---

## Processed Data Formats

### Target Selection Time Series

**Location**: `OtherResults/TS_Dynamic_Policy/`

**Format**: CSV with binary-encoded engagement

**Columns**:
- `time`: Timestamp (seconds)
- `TrialID`: Trial number (1-24)
- `numTargs`: Number of targets in trial (3, 4, or 5)
- `HA0_engagement`: Target ID that HA0 is engaging (-1 if none, 0-4 for target ID)
- `HA1_engagement`: Target ID that HA1 is engaging (-1 if none, 0-4 for target ID)

**Generation**: `Scripts/get_actual_TS_Dynamic_Policy_as_csv.py`

**Example**:
```
time,TrialID,numTargs,HA0_engagement,HA1_engagement
593.52,14,4,0,1
593.54,14,4,0,1
593.56,14,4,0,2
...
```

### Binary Trace Overlap Scores

**Location**: `OtherResults/AA_scores_traces/`

**Format**: CSV with one row per session/player

**Columns**:
- `Session`: Session ID (e.g., Session1001)
- `Player`: Player number (1 or 2)
- `7` through `24`: Binary trace overlap score for each trial (0-1 range)

**Generation**: `Scripts/binary_trace_evaluator_Exp1.py`

---

## Coordinate System Details

### Spatial Layout

```
                    North (+Z)
                        ↑
                        |
        (-X, +Z)        |         (+X, +Z)
            ╔═══════════╬═══════════╗
            ║           |           ║
            ║           |           ║
            ║           |           ║
West (-X) ←─║───────── (0,0) ──────║─→ East (+X)
            ║      Containment     ║
            ║         Zone         ║
            ║           |           ║
            ╚═══════════╬═══════════╝
        (-X, -Z)        |         (+X, -Z)
                        |
                        ↓
                    South (-Z)

Game Field: 120m (X) × 90m (Z)
Containment Zone: Radius = 4m, Center = (0, 0)
Walls: X = ±60m, Z = ±45m
```

### Distance Calculations

```python
# Euclidean distance between two points
def distance(x1, z1, x2, z2):
    return np.sqrt((x2 - x1)**2 + (z2 - z1)**2)

# Distance from containment zone center
def dist_from_center(x, z):
    return np.sqrt(x**2 + z**2)

# Within containment zone?
def in_containment(x, z, radius=4):
    return dist_from_center(x, z) <= radius

# Within influence radius? (TA repulsion distance)
def in_influence(ha_x, ha_z, ta_x, ta_z, radius=10):
    return distance(ha_x, ha_z, ta_x, ta_z) <= radius
```

### Angle Calculations

```python
import numpy as np

# Angle from HA to TA relative to containment zone
def angle_to_target(ha_x, ha_z, ta_x, ta_z):
    """
    Returns angle in radians [-π, π]
    0 = North, π/2 = East, -π/2 = West, ±π = South
    """
    vec_ha = np.array([ha_x, ha_z])
    vec_ta = np.array([ta_x, ta_z])
    angle = np.arctan2(vec_ta[0], vec_ta[1]) - np.arctan2(vec_ha[0], vec_ha[1])
    # Wrap to [-π, π]
    angle = (angle + np.pi) % (2 * np.pi) - np.pi
    return angle

# Angular distance (used in SCA policy)
def angular_distance(ha_x, ha_z, ta_x, ta_z):
    """
    Angular distance from HA to TA measured from containment zone center
    Returns absolute angle in degrees [0, 180]
    """
    angle_ha = np.arctan2(ha_z, ha_x)
    angle_ta = np.arctan2(ta_z, ta_x)
    diff = np.abs(angle_ta - angle_ha)
    # Wrap to [0, π]
    if diff > np.pi:
        diff = 2 * np.pi - diff
    return np.degrees(diff)
```

---

## Data Usage Examples

### Example 1: Extract Trial Duration

```python
import pandas as pd
from pathlib import Path

def get_trial_duration(trial_file):
    df = pd.read_csv(trial_file)
    return df['time'].iloc[-1] - df['time'].iloc[0]

# Get durations for all trials in a session
session_path = Path("RAW_EXPERIMENT_DATA/TWO-HUMAN_HAs/Session1001/ExperimentData")
for trial_file in sorted(session_path.glob("*trialIdentifier*.csv")):
    duration = get_trial_duration(trial_file)
    trial_id = trial_file.stem.split("trialIdentifier")[1].split("_")[0]
    print(f"Trial {trial_id}: {duration:.1f}s")
```

### Example 2: Detect Target Engagement

```python
def detect_target_engagement(df, herder_id=0, target_id=0, influence_radius=10):
    """
    Returns boolean array indicating when herder is engaging target
    """
    ha_x = df[f'p{herder_id}x'].values
    ha_z = df[f'p{herder_id}z'].values
    ta_x = df[f't{target_id}x'].values
    ta_z = df[f't{target_id}z'].values

    distances = np.sqrt((ha_x - ta_x)**2 + (ha_z - ta_z)**2)
    return distances <= influence_radius

# Usage
df = pd.read_csv("path/to/trial.csv")
engagement = detect_target_engagement(df, herder_id=0, target_id=0)
print(f"HA0 engaged T0 for {engagement.sum() / 50:.1f} seconds")
```

### Example 3: Visualize Trajectories

```python
import matplotlib.pyplot as plt

def plot_trajectories(df):
    """
    Plot herder and target trajectories
    """
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot game field
    ax.set_xlim(-60, 60)
    ax.set_ylim(-45, 45)
    ax.set_aspect('equal')

    # Plot containment zone
    circle = plt.Circle((0, 0), 4, color='red', fill=False, linewidth=2)
    ax.add_patch(circle)

    # Plot herder trajectories
    ax.plot(df['p0x'], df['p0z'], 'b-', linewidth=1, label='Herder 0')
    ax.plot(df['p1x'], df['p1z'], 'r-', linewidth=1, label='Herder 1')

    # Plot target trajectories
    for i in range(5):
        if f't{i}x' in df.columns:
            ax.plot(df[f't{i}x'], df[f't{i}z'], 'k--', linewidth=0.5, alpha=0.5,
                    label=f'Target {i}' if i == 0 else "")

    ax.set_xlabel('X Position (m)')
    ax.set_ylabel('Z Position (m)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.title('Trial Trajectories')
    plt.show()

# Usage
df = pd.read_csv("path/to/trial.csv")
plot_trajectories(df)
```

---

## Citation

When using this data, please cite:

```bibtex
@dataset{binkamruddin2024data,
  author = {bin Kamruddin, Ayman and Lam, Christopher and Ghanem, Sala and
            Patil, Gaurav and Musolesi, Mirco and di Bernardo, Mario and
            Richardson, Michael J},
  title = {From Human Heuristics to Human-AI Teams: Multi-agent Herding Data},
  year = {2024},
  publisher = {Mendeley Data},
  version = {2},
  doi = {10.17632/kpxp5zkh5f.2},
  url = {https://data.mendeley.com/datasets/kpxp5zkh5f/2}
}
```

---

## Contact

For questions about the data or data access issues:
- **Corresponding Author**: Michael J. Richardson (michael.richardson@mq.edu.au)
- **Lead Developer**: Ayman bin Kamruddin
- **GitHub Issues**: [Repository URL]/issues

---

*Last updated: 2025-09-30*
*Data version: 2*