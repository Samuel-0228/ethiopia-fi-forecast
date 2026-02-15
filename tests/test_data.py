# tests/test_data.py
"""
Unit tests for data loading functionality.
"""

from src.data.load import load_enriched_data
from pathlib import Path
import pandas as pd
import pytest

# Dynamically resolve the project root (works regardless of cwd)
# From tests/ folder → go up 1 level to reach project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Construct the expected path to the enriched data file
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "processed" / \
    "ethiopia_fi_unified_enriched_20260131.csv"

# Import the function we want to test
# (assuming src/ is now importable via editable install or PYTHONPATH)


def test_load_enriched_data_returns_dataframe():
    """
    Test that load_enriched_data() returns a pandas DataFrame
    and contains expected columns.
    """
    # Use the dynamically resolved path
    df = load_enriched_data(path=DEFAULT_DATA_PATH)

    # Basic assertions
    assert isinstance(
        df, pd.DataFrame), "Loaded data should be a pandas DataFrame"
    assert len(df) > 0, "DataFrame should not be empty"

    # Check for critical columns that must exist in the unified schema
    expected_columns = [
        'record_type',
        'pillar',
        'indicator_code',
        'value_numeric',
        'observation_date',
        'source_name',
        'source_url',
        'confidence'
    ]
    missing_cols = [col for col in expected_columns if col not in df.columns]
    assert not missing_cols, f"Missing expected columns: {missing_cols}"

    # Optional: check that we have some observation records
    assert (df['record_type'] == 'observation').any(), \
        "Dataset should contain at least some 'observation' records"


def test_load_enriched_data_raises_error_on_missing_file():
    """
    Test that load_enriched_data raises FileNotFoundError when file doesn't exist.
    """
    fake_path = PROJECT_ROOT / "data" / "processed" / "this_file_does_not_exist.csv"

    with pytest.raises(FileNotFoundError) as exc_info:
        load_enriched_data(path=fake_path)

    assert "not found" in str(exc_info.value).lower(), \
           "Error message should mention that the file was not found"
