# Interim Progress Report – January 31, 2026

## Key Findings

- Access (Account Ownership): Stuck at 49% (2024 Findex 2025 data). Supply-side (222M+ digital accounts) not translating to unique/active users.
- Usage: Digital payments ~21% (2024); active mobile money ~15-16% (2025).
- Momentum: Telebirr 58.6M users, 6.88T ETB cumulative tx; M-Pesa growing.
- Policy shift: NDPS 2026-2030 emphasizes usage (60% active by 2030), gaps closure.

## Preliminary Forecasts (Illustrative)

- 2026: Access 51-55%, Usage 25-32%
- 2027: Access 55-62%, Usage 32-42%
  (Scenarios depend on active usage interventions)

## Next Steps

- Ingest full `ethiopia_fi_unified_data` (observations + events + impact_links)
- Build event dummies / interrupted time series
- Fit Prophet with regressors or ARIMAX
- Dashboard (Streamlit) with scenarios & confidence bands

Data sources documented; uncertainty high due to sparse demand-side data.
