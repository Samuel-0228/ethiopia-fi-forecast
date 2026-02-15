# src/data/load.py
"""Data loading utilities for Ethiopia financial inclusion forecasting."""

from pathlib import Path
from typing import Union

import pandas as pd


def get_project_root() -> Path:
    """
    Return the absolute path to the project root folder.
    Works regardless of where the script/test is executed from.
    """
    # __file__ is src/data/load.py → parents[2] = project root
    return Path(__file__).resolve().parents[2]


DEFAULT_DATA_PATH = (
    get_project_root()
    / "data"
    / "processed"
    / "ethiopia_fi_unified_enriched_20260131.csv"
)


def load_enriched_data(
    path: Union[str, Path, None] = None,
) -> pd.DataFrame:
    """
    Load the enriched unified dataset for Ethiopia financial inclusion.

    Args:
        path: Optional custom path. If None, uses default location relative to project root.

    Returns:
        pandas DataFrame with parsed dates.

    Raises:
        FileNotFoundError: If the file does not exist at the resolved path.
    """
    if path is None:
        path = DEFAULT_DATA_PATH
    else:
        path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            f"Cannot find enriched data file.\n"
            f"Expected: {DEFAULT_DATA_PATH}\n"
            f"Given:    {path}\n"
            "Check that the file exists in data/processed/"
        )

    df = pd.read_csv(path, parse_dates=["observation_date"])
    return df
