import pytest
from src.data.load import load_enriched_data


def test_load_enriched_data_returns_dataframe():
    df = load_enriched_data()
    assert isinstance(df, pd.DataFrame)
    assert 'record_type' in df.columns
    assert len(df) > 30  # rough check
