"""Exp 1 binary trace evaluator.

This script reproduces the original analysis pipeline while providing a more
structured and configurable implementation. It computes the binary trace overlap
between each human session and a library of artificial agent (AA) simulations for
trials 7–24 and saves per-session/player CSV summaries.
"""

from __future__ import annotations

import argparse
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np
import pandas as pd

from tools.traj_utils import get_binary_trace

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class BinaryTraceConfig:
    """Container for runtime parameters.

    Attributes
    ----------
    first_trial: int
        First trial (inclusive) included in the evaluation.
    last_trial: int
        Last trial (inclusive) included in the evaluation.
    aa_types: Sequence[str]
        Simulation cohort names to process.
    human_data_dir: Path
        Root directory containing human–human session folders.
    simulation_root: Path
        Root directory containing AA simulation data; subdirectories must be the
        entries in ``aa_types``.
    output_dir: Path
        Destination directory for generated CSV files.
    """

    first_trial: int
    last_trial: int
    aa_types: Sequence[str]
    human_data_dir: Path
    simulation_root: Path
    output_dir: Path

    trial_columns: Tuple[str, ...] = field(init=False)

    def __post_init__(self) -> None:  # type: ignore[override]
        if self.first_trial > self.last_trial:
            raise ValueError("first_trial must be <= last_trial")
        object.__setattr__(self, "trial_columns", tuple(str(t) for t in self.trials))

    @property
    def trials(self) -> range:
        return range(self.first_trial, self.last_trial + 1)


DEFAULT_AA_TYPES: Tuple[str, ...] = (
    "CollinearAngle",
    "CollinearDistance",
    "Angle",
    "Distance",
    "ContainmentZone",
)


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------


def _discover_sessions(human_data_dir: Path) -> List[Path]:
    """Return session directories in the supplied human data root."""

    if not human_data_dir.exists():
        raise FileNotFoundError(f"Human data directory not found: {human_data_dir}")

    sessions = [path for path in human_data_dir.iterdir() if path.is_dir()]
    if not sessions:
        raise RuntimeError(f"No session folders found under {human_data_dir}")

    return sessions


def _find_trial_file(session_dir: Path, trial_id: str) -> Path:
    """Locate the CSV file that matches ``trial_id`` within ``session_dir``."""

    matches = list(session_dir.rglob(f"*trialIdentifier{trial_id}*"))
    if not matches:
        raise FileNotFoundError(
            f"Missing trialIdentifier{trial_id} file in session {session_dir.name}"
        )

    if len(matches) > 1:
        logging.warning(
            "Multiple files matched trialIdentifier%s in %s; using %s",
            trial_id,
            session_dir,
            matches[0],
        )
    return matches[0]


def _load_background_positions(
    background_sessions: Iterable[Path], trial_id: str, player: int
) -> Tuple[np.ndarray, np.ndarray]:
    """Aggregate human positions for every background session."""

    xs: List[np.ndarray] = []
    zs: List[np.ndarray] = []
    col_x = f"p{player}x"
    col_z = f"p{player}z"

    for session in background_sessions:
        trial_file = _find_trial_file(session, trial_id)
        data = pd.read_csv(trial_file)
        xs.append(data[col_x].to_numpy())
        zs.append(data[col_z].to_numpy())

    if not xs or not zs:
        raise RuntimeError(f"Unable to collect background positions for trial {trial_id}")

    return np.concatenate(xs), np.concatenate(zs)


def _get_simulation_trial(
    cache: Dict[str, pd.DataFrame], simulation_dir: Path, trial_id: str
) -> pd.DataFrame:
    """Read and memoise the simulation trajectory for a single trial."""

    if trial_id not in cache:
        matches = list(simulation_dir.rglob(f"*trialIdentifier{trial_id}*"))
        if not matches:
            raise FileNotFoundError(
                f"Missing simulation trialIdentifier{trial_id} in {simulation_dir}"
            )
        if len(matches) > 1:
            logging.warning(
                "Multiple simulation files matched trialIdentifier%s in %s; using %s",
                trial_id,
                simulation_dir,
                matches[0],
            )
        cache[trial_id] = pd.read_csv(matches[0])
    return cache[trial_id]


# ---------------------------------------------------------------------------
# Core evaluation
# ---------------------------------------------------------------------------


def evaluate_aa_type(config: BinaryTraceConfig, sessions: List[Path], aa_type: str) -> pd.DataFrame:
    """Compute binary trace scores for a single AA simulation cohort."""

    logging.info("Processing AA type: %s", aa_type)
    simulation_dir = config.simulation_root / aa_type
    if not simulation_dir.exists():
        raise FileNotFoundError(f"Simulation directory not found: {simulation_dir}")

    cache: Dict[str, pd.DataFrame] = {}
    records: List[Dict[str, object]] = []

    for session_idx, evaluee_session in enumerate(sessions):
        logging.info(
            "Evaluating session %s (%d of %d)",
            evaluee_session.name,
            session_idx + 1,
            len(sessions),
        )
        background_sessions = [s for s in sessions if s != evaluee_session]

        for player in (0, 1):
            record: Dict[str, object] = {
                "Session": evaluee_session.name,
                "Player": player + 1,
            }

            for trial in config.trials:
                trial_id = f"{trial:02}"
                logging.debug(
                    "Session %s | player %d | trial %s",
                    evaluee_session.name,
                    player + 1,
                    trial_id,
                )

                X, Z = _load_background_positions(background_sessions, trial_id, player)
                sim_trial = _get_simulation_trial(cache, simulation_dir, trial_id)
                score = get_binary_trace(X, Z, sim_trial, f"hA{player}")
                record[str(trial)] = score

            records.append(record)

    columns = ("Session", "Player", *config.trial_columns)
    return pd.DataFrame.from_records(records, columns=columns)


def run(config: BinaryTraceConfig) -> None:
    """Entry point for the evaluation pipeline."""

    config.output_dir.mkdir(parents=True, exist_ok=True)
    sessions = _discover_sessions(config.human_data_dir)

    for aa_type in config.aa_types:
        df = evaluate_aa_type(config, sessions, aa_type)
        output_path = config.output_dir / f"AA_scores_traces_Successive{aa_type}.csv"
        df.to_csv(output_path, index=False)
        logging.info("Saved %s", output_path)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate Exp 1 binary trace scores")
    parser.add_argument("--first-trial", type=int, default=7, help="First trial (inclusive)")
    parser.add_argument("--last-trial", type=int, default=24, help="Last trial (inclusive)")
    parser.add_argument(
        "--human-data-dir",
        type=Path,
        default=None,
        help="Override path to human-human session data",
    )
    parser.add_argument(
        "--simulation-root",
        type=Path,
        default=None,
        help="Override path to AA simulation data",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Override output directory for CSV summaries",
    )
    parser.add_argument(
        "--aa-types",
        nargs="+",
        default=None,
        help="Subset of AA types to process",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging verbosity",
    )
    return parser.parse_args()


def build_config(args: argparse.Namespace) -> BinaryTraceConfig:
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent

    human_dir = args.human_data_dir or project_root / "RAW_EXPERIMENT_DATA" / "TWO-HUMAN_HAs"
    simulation_root = args.simulation_root or project_root / "OtherResults" / "AA-AA_SimulationData"
    output_dir = args.output_dir or project_root / "OtherResults" / "AA_scores_traces"

    aa_types: Sequence[str] = args.aa_types or DEFAULT_AA_TYPES

    return BinaryTraceConfig(
        first_trial=args.first_trial,
        last_trial=args.last_trial,
        aa_types=tuple(aa_types),
        human_data_dir=human_dir,
        simulation_root=simulation_root,
        output_dir=output_dir,
    )


def main() -> None:
    args = parse_args()
    logging.basicConfig(level=getattr(logging, args.log_level), format="%(levelname)s: %(message)s")
    config = build_config(args)
    run(config)


if __name__ == "__main__":
    main()
