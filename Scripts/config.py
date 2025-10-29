"""
Configuration file for experimental constants and parameters.

This file centralizes all magic numbers and experimental parameters used across
the analysis scripts for reproducibility and maintainability.
"""

# ============================================================================
# EXPERIMENT PARAMETERS
# ============================================================================

# Trial range for analysis
FIRST_TRIAL = 7
LAST_TRIAL = 25  # Python-friendly (no need for +1)

# Number of agents
NUM_HERDERS = 2
MAX_TARGETS = 5

# Target conditions
TARGET_CONDITIONS = [3, 4, 5]

# ============================================================================
# FIELD DIMENSIONS (meters)
# ============================================================================

FIELD_XLIM = 60
FIELD_YLIM = 45

# ============================================================================
# TRAJECTORY ANALYSIS PARAMETERS
# ============================================================================

# Binning size for 2D histograms (meters)
BIN_SIZE = 5

# Threshold for binary heatmap
THRESHOLD = 10

# ============================================================================
# AGENT INTERACTION PARAMETERS
# ============================================================================

# Distance at which target repulsion starts (meters)
REPULSION_DISTANCE = 10

# ============================================================================
# SIMULATION TYPES
# ============================================================================

SIMULATION_TYPES = [
    "CollinearAngle",
    "CollinearDistance",
    "Angle",
    "Distance",
    "ContainmentZone"
]

# ============================================================================
# AI AGENT TYPES
# ============================================================================

# Only Heuristic agent type is used in this study
AA_TYPES = ["Heuristic"]

# ============================================================================
# DATA COLUMN NAMES
# ============================================================================

# Column prefixes for different agent types
HUMAN_PREFIX = "p"  # e.g., p0x, p0z
AI_PREFIX = "hA"    # e.g., hA0x, hA0z
TARGET_PREFIX = "t" # e.g., t0x, t0z

# ============================================================================
# NOTES
# ============================================================================

# To use these constants in your scripts:
#   from config import FIRST_TRIAL, LAST_TRIAL, FIELD_XLIM, etc.
#
# Or import all:
#   from config import *
