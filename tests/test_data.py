# tests/test_data.py
"""
Unit tests for data loading and basic schema validation.
"""

from src.data.load import load_enriched_data
from pathlib import Path
import pandas as pd
import pytest

# Resolve project root reliably (from tests/ → up 1 level)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Expected data file
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "processed" / \
    "ethiopia_fi_unified_enriched_20260131.csv"

# Import function under test


@pytest.fixture
def enriched_df():
    """Fixture: load the enriched dataset once for all tests."""
    return load_enriched_data(path=DEFAULT_DATA_PATH)


def test_load_enriched_data_returns_dataframe(enriched_df):
    """Basic check: returns DataFrame."""
    assert isinstance(enriched_df, pd.DataFrame)
    assert len(enriched_df) > 30, "Dataset should have at least 30+ rows"


def test_has_required_columns(enriched_df):
    """Check core schema columns exist."""
    required = [
        'record_type', 'pillar', 'indicator_code',
        'value_numeric', 'observation_date',
        'source_name', 'source_url', 'confidence'
    ]
    missing = [col for col in required if col not in enriched_df.columns]
    assert not missing, f"Missing columns: {missing}"


def test_observation_date_is_datetime(enriched_df):
    """observation_date should be parsed as datetime64."""
    assert pd.api.types.is_datetime64_any_dtype(
        enriched_df['observation_date'])


def test_has_observations_and_events(enriched_df):
    """Dataset should contain both observations and events."""
    assert (enriched_df['record_type'] ==
            'observation').any(), "No observation records"
    assert (enriched_df['record_type'] == 'event').any(), "No event records"


def test_confidence_levels_are_valid(enriched_df):
    """confidence should be one of known values."""
    valid_conf = {'high', 'medium', 'low'}
    unique_conf = set(enriched_df['confidence'].dropna().str.lower())
    invalid = unique_conf - valid_conf
    assert not invalid, f"Invalid confidence values: {invalid}"
