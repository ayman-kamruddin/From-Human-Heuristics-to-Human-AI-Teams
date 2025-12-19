
# From Human Heuristics to Human–AI Teams: Modeling Multiagent First-Person Herding using Dynamical Perceptual-Motor Primitives

## Overview
This project explores multi-player multi-target environments with and dynamic policy modeling. It includes experiments for human-AI interaction and pure human experiments, along with results and visualizations.

## Quick Start

### Prerequisites
- **Python 3.x** (Python 3.7 or higher recommended)
- **R** (for statistical analysis)
- Required Python packages (see Installation below)

### Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd From-Human-Heuristics-to-Human-AI-Teams
   ```

2. **Create a virtual environment** (recommended)

   Choose one of the following options:

   **Option A: Using conda (recommended for data science)**
   ```bash
   # Create a new conda environment
   conda create -n herding-analysis python=3.11

   # Activate the environment
   conda activate herding-analysis
   ```

   **Option B: Using venv (built-in Python)**
   ```bash
   # Create a new virtual environment
   python -m venv venv

   # Activate the environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download the data**
   - Download data from: [Mendeley Data](https://data.mendeley.com/datasets/kpxp5zkh5f/2)
   - Extract the data files to the root directory of this project
   - The expected folder structure is:
     ```
     RAW_EXPERIMENT_DATA/
     ├── TWO-HUMAN_HAs/
     ├── HUMAN-AA_TEAM/
     └── AA-AA-simulation/
     OtherResults/
     └── AA-AA_SimulationData/
     ```

5. **Verify your setup**
   ```bash
   python check_setup.py
   ```
   This script will check if all dependencies are installed and data folders are in the correct location.

### Platform Compatibility
This codebase is cross-platform compatible and works on:
- **Windows**
- **macOS**
- **Linux**

All file paths use `os.path.join()` for proper path handling across different operating systems.

### Important Notes
- **Always activate your virtual environment** before running scripts:
  - Conda: `conda activate herding-analysis`
  - venv (macOS/Linux): `source venv/bin/activate`
  - venv (Windows): `venv\Scripts\activate`
- To deactivate the environment when done: `conda deactivate` or `deactivate`

## Folder Structure

### 1. `Experiment-HumanAA`
Includes executables for experiments involving human-AA interaction:
- **`Heuristic`**: Heuristic-based models.
- **`Model1HumanSensitivePlay`**: Pretrained RL model interacting in a human-sensitive mode.
- **`Model1SelfPlay`**: Pretrained RL model trained in self-play mode.
- **`Model2HumanSensitivePlay`**: An alternate RL model in human-sensitive mode.
- **`Model2SelfPlay`**: An alternate RL model in self-play mode.

### 2. `Experiment-HumanHuman`
Contains data and executables for experiments involving human-human interaction:
- **`FirstPersonHerding_Data`**: Contains initial condition data.
- **`FirstPersonHerding.exe`**: Executable for running the human-human experiment.
- **`UnityPlayer.dll` & `MonoBleedingEdge`**: Unity runtime dependencies.

### 3. `Scripts`
Contains utility scripts for processing data and generating figures:
- **`tools/`**: Miscellaneous tools for experiment analysis.
- everything else: please see the Readme file in the `Scripts` directory for more information.


### 4. Miscellaneous
- **`.gitignore`**: Specifies files and directories to be ignored by Git.
- **`README.md`**: Documentation for the project.

---

## Usage

### 1. Running Experiments
Use executables in `Experiment-HumanHuman` folder to run human-human experiments, or executables in `Experiment-HumanAA` for human-AI experiments.

### 2. Setting Up Data
Download the data folder from [Mendeley Data](https://data.mendeley.com/datasets/kpxp5zkh5f/2) and place it in the root directory of the project. Run `python check_setup.py` to verify correct placement.

### 3. Analyzing and Visualizing Results
Navigate to the `Scripts` folder and follow the analysis workflow described in `Scripts/README.md`.

**Key analysis workflows:**
- **Experiment 1 (Human-Human)**: TSp overlap analysis and binary trace comparison
- **Experiment 2 (Human-AA)**: Comparing human-AA teams to human-human baselines

See `Scripts/README.md` for detailed step-by-step instructions.

## Referrence

bin Kamruddin, A., Lam, C., Ghanem, S., Patil, G., Musolesi, M., di Bernardo, M., & Richardson, M. J. (n.d.). From human heuristics to human–AI teams: Modeling multiagent first-person herding using dynamical perceptual–motor primitives [Manuscript submitted for publication].
