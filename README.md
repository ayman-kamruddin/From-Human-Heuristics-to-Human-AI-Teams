
# From Human Heuristics to Human–AI Teams: Modeling Multiagent First-Person Herding using Dynamical Perceptual-Motor Primitives

## Overview
This project explores multi-player multi-target environments with and dynamic policy modeling. It includes experiments for human-AI interaction and pure human experiments, along with results and visualizations.

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
1. **Running Experiments**: Use executables in `Experiment-HumanHuman` to run human-human experiments.
2. Place the data folder, present ***here***, in the root directory of the project.
3. **Analyzing and Visualising Results**: Use scripts in `Scripts` to analyze raw data and generate plots.

## Dependencies
- Unity runtime (`UnityPlayer.dll`, `MonoBleedingEdge`)
- Python scripts require Python 3.x and the following libraries:
  - `numpy`
  - `matplotlib`
  - `pandas`
  - `similaritymeasures`

## Referrence

bin Kamruddin, A., Lam, C., Ghanem, S., Patil, G., Musolesi, M., di Bernardo, M., & Richardson, M. J. (n.d.). From human heuristics to human–AI teams: Modeling multiagent first-person herding using dynamical perceptual–motor primitives [Manuscript submitted for publication].
