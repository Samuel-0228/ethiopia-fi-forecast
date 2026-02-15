# tests/test_data.py
"""
Unit tests for data loading and basic schema validation.
"""

from src.data.load import load_enriched_data
from pathlib import Path
import pandas as pd
import pytest

# Resolve project root reliably
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "processed" / \
    "ethiopia_fi_unified_enriched_20260131.csv"


@pytest.fixture
def enriched_df():
    """Fixture: load the enriched dataset once for all tests."""
    return load_enriched_data(path=DEFAULT_DATA_PATH)


def test_load_enriched_data_returns_dataframe(enriched_df):
    assert isinstance(enriched_df, pd.DataFrame)
    assert len(enriched_df) > 30


def test_has_required_columns(enriched_df):
    required = [
        'record_type', 'pillar', 'indicator_code',
        'value_numeric', 'observation_date',
        'source_name', 'source_url', 'confidence'
    ]
    missing = [col for col in required if col not in enriched_df.columns]
    assert not missing, f"Missing columns: {missing}"


def test_observation_date_is_datetime(enriched_df):
    assert pd.api.types.is_datetime64_any_dtype(
        enriched_df['observation_date'])


def test_has_observations_and_events(enriched_df):
    assert (enriched_df['record_type'] == 'observation').any()
    assert (enriched_df['record_type'] == 'event').any()


def test_confidence_levels_are_valid(enriched_df):
    valid_conf = {'high', 'medium', 'low'}
    unique_conf = set(enriched_df['confidence'].dropna().str.lower())
    invalid = unique_conf - valid_conf
    assert not invalid, f"Invalid confidence values found: {invalid}"


# ────────────────────────────────────────────────
# NEW TEST 1: Check that numeric values are sensible
# ────────────────────────────────────────────────
def test_value_numeric_range_is_reasonable(enriched_df):
    """
    Verify that value_numeric is within expected ranges for financial inclusion indicators.
    - Percentages (ownership, usage, active rate) should be between 0 and 100
    - Total accounts should be positive and realistic (millions scale)
    """
    numeric = enriched_df['value_numeric'].dropna()

    # Percentages: most indicators are 0–100 range
    pct_indicators = enriched_df[
        enriched_df['indicator_code'].str.contains(
            'OWNERSHIP|ACCOUNT|PCT|USAGE', case=False, na=False
        )
    ]['value_numeric'].dropna()

    if not pct_indicators.empty:
        assert pct_indicators.ge(0).all(), "Negative percentage values found"
        assert (pct_indicators <= 100).all(), "Percentage values > 100 found"

    # Total accounts (large numbers) should be positive
    total_accounts = enriched_df[
        enriched_df['indicator_code'].str.contains(
            'TOTAL|ACCOUNTS', case=False, na=False)
    ]['value_numeric'].dropna()

    if not total_accounts.empty:
        assert total_accounts.gt(
            0).all(), "Negative or zero total accounts found"


# ────────────────────────────────────────────────
# NEW TEST 2: Check that recent data (2024+) exists
# ────────────────────────────────────────────────
def test_has_recent_data(enriched_df):
    """
    Ensure the enriched dataset contains observations from 2024 or later
    (critical for forecasting relevance in 2026 context).
    """
    recent = enriched_df[
        (enriched_df['record_type'] == 'observation') &
        (enriched_df['observation_date'].dt.year >= 2024)
    ]

    assert not recent.empty, "No observations from 2024 or later — forecasting will be unreliable"

    # Optional: check for at least one key indicator in recent data
    key_indicators = ['ACC_OWNERSHIP',
                      'USG_DIGITAL_PAYMENT', 'ACTIVE_MM_ACCOUNTS_PCT']
    recent_keys = recent[recent['indicator_code'].isin(key_indicators)]
    assert not recent_keys.empty, f"No recent data for key indicators: {key_indicators}"
