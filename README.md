[![CI](https://github.com/Samuel-0228/ethiopia-fi-forecast/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Samuel-0228/ethiopia-fi-forecast/actions/workflows/ci.yml)

# Ethiopia Financial Inclusion Forecasting Dashboard

**Scenario-based forecasting** of **account ownership (access)** and **digital payment usage** in Ethiopia to 2027, built for regulators, DFIs, mobile operators, and fintech stakeholders.

**Reference date:** Early 2026 (Global Findex 2025 + NBE 2025/2026 indicators)

## Business Context

Ethiopia has massive digital finance supply growth:

- ~139.5 million mobile money registrations (2025)
- Telebirr: ~58.6 million users (Jan 2026)
- Fayda digital ID: >34.9 million enrolled
- NDPS 2026–2030 (launched Dec 2025): target 60% active accounts by 2030

But demand-side lags severely:

- Account ownership: **49%** (Findex 2025 / 2024 data, +3 pp since 2021)
- Digital payment usage: **~21%**
- Active rate: **~15–16%** → ~117 million dormant accounts

This "inclusion illusion" creates risk for credit assessment, fraud, policy impact, and investment decisions.

## Solution

Event-augmented time-series forecasting (trend + step dummies for Telebirr, M-Pesa, Fayda, NDPS) with three scenarios:

- Baseline: slow continuation
- Optimistic: strong activation success
- Pessimistic: persistent dormancy

**2027 projections (end-of-year):**

| Scenario    | Access (%) | Usage (%) |
| ----------- | ---------- | --------- |
| Baseline    | 54–58      | 29–35     |
| Optimistic  | 62–68      | 35–45     |
| Pessimistic | 51–54      | 24–28     |

(Uncertainty ±10–15 pp due to triennial Findex data)

## Features

- Modular Python code (`src/`) with type hints & config dataclass
- Robust data loading & validation
- 7+ pytest tests (schema, ranges, recent data)
- GitHub Actions CI pipeline (lint + tests)
- Interactive Streamlit dashboard: metrics, trends, event overlays, scenario selector, uncertainty bands, CSV export

## Quick Start

```bash
git clone https://github.com/Samuel-0228/ethiopia-fi-forecast.git
cd ethiopia-fi-forecast

pip install -r requirements.txt
pip install -e .               # makes src/ importable

# Run tests (should show 7+ passed)
pytest tests/

# Launch dashboard
streamlit run dashboard/app.py
```
