from typing import Tuple
import pandas as pd


def load_enriched_data(path: str = "../data/processed/ethiopia_fi_unified_enriched_20260131.csv") -> pd.DataFrame:
    """Load and parse enriched unified dataset."""
    df = pd.read_csv(path, parse_dates=['observation_date'])
    return df
