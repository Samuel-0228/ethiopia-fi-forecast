"""Configuration dataclass for Ethiopia financial inclusion forecasting."""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(frozen=True)  # immutable config – safer for finance/reproducibility
class ForecastConfig:
    """Global configuration parameters."""

    base_year: int = 2024
    forecast_years: List[int] = field(
        default_factory=lambda: [2025, 2026, 2027])
    uncertainty_pp: float = 12.0  # wide band due to sparse Findex data

    # Event dates (ISO format strings)
    events: Dict[str, str] = field(default_factory=lambda: {
        "telebirr_launch": "2021-05-01",
        "mpesa_entry":    "2023-08-01",
        "ndps_fayda":     "2025-12-01"   # NDPS launch + Fayda acceleration
    })

    # Latest known benchmarks (early 2026 context)
    latest_access_pct: float = 49.0       # Findex 2025 (2024 data)
    latest_usage_pct: float = 21.0
    latest_mm_accounts_m: float = 139.5   # million
    latest_active_pct: float = 16.0

    def get_forecast_horizon(self) -> int:
        """Number of years to forecast ahead."""
        return max(self.forecast_years) - self.base_year
