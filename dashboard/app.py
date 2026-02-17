import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="Ethiopia Financial Inclusion Dashboard", layout="wide")

# ────────────────────────────────────────────────
# LOAD DATA – Use absolute paths relative to project root
# ────────────────────────────────────────────────


@st.cache_data
def load_data():
    # Resolve project root from dashboard/app.py location
    # dashboard/app.py -> parents[1] = project root (ethiopia-fi-forecast/)
    PROJECT_ROOT = Path(__file__).resolve().parents[1]

    # Define expected file paths
    enriched_path = PROJECT_ROOT / "data" / "processed" / \
        "ethiopia_fi_unified_enriched_20260131.csv"
    forecast_path = PROJECT_ROOT / "reports" / \
        "figures" / "task4_annual_forecast_2025_2027.csv"

    # Load enriched data – required
    try:
        df = pd.read_csv(enriched_path, parse_dates=['observation_date'])
        st.success("Enriched data loaded successfully from: " +
                   str(enriched_path))
    except FileNotFoundError as e:
        st.error(
            f"**Critical Error**: Cannot find the enriched data file!\n\n"
            f"Expected path:\n{enriched_path}\n\n"
            f"Error details: {e}\n\n"
            "Please verify the file exists in **data/processed/** and the filename matches exactly.\n"
            "Common fixes: Check spelling, case sensitivity, or move the file to the correct folder."
        )
        st.stop()  # Stop execution – no unbound variables

    # Load forecast data – optional with fallback
    forecast = None
    try:
        forecast = pd.read_csv(forecast_path)
        st.info(f"Forecast data loaded from: {forecast_path}")
    except FileNotFoundError:
        st.warning(
            "Forecast CSV not found – using fallback dummy data for demo purposes.\n"
            f"Expected: {forecast_path}\n"
            "You can generate it from notebooks/04_task4_forecasting.ipynb"
        )
        forecast = pd.DataFrame({
            'year_int': [2025, 2026, 2027],
            'baseline_access': [50.0, 54.0, 57.0],
            'optimistic_access': [53.0, 60.0, 65.0],
            'pessimistic_access': [49.0, 51.0, 53.0],
            'baseline_usage': [22.0, 26.0, 30.0],
            'optimistic_usage': [25.0, 32.0, 40.0],
            'pessimistic_usage': [21.0, 24.0, 27.0]
        })

    return df, forecast


# Load data once
df, forecast = load_data()

obs = df[df['record_type'] == 'observation'].copy()

# ────────────────────────────────────────────────
# SIDEBAR
# ────────────────────────────────────────────────
st.sidebar.title("Ethiopia FI Dashboard")
scenario = st.sidebar.radio(
    "Forecast Scenario", ["Baseline", "Optimistic", "Pessimistic"])
st.sidebar.markdown("---")
st.sidebar.info(
    "Data enriched up to 2025; forecasts are scenario-based with wide uncertainty "
    "due to sparse historical points (triennial Findex surveys)."
)

# ────────────────────────────────────────────────
# MAIN PAGE
# ────────────────────────────────────────────────
st.title("Ethiopia Financial Inclusion Forecasting Dashboard")
st.markdown(
    "**Access** (Account Ownership) & **Usage** (Digital Payments) Trends & Projections 2025–2027"
)

# ────────────────────────────────────────────────
# OVERVIEW METRICS
# ────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

latest_access = obs[obs['indicator_code'] ==
                    'ACC_OWNERSHIP']['value_numeric'].max()
latest_usage = obs[obs['indicator_code'] == 'USG_DIGITAL_PAYMENT']['value_numeric'].max() \
    if not obs[obs['indicator_code'] == 'USG_DIGITAL_PAYMENT'].empty else 21.0
latest_mm = obs[obs['indicator_code'] ==
                'MOBILE_MONEY_ACCOUNTS_TOTAL']['value_numeric'].max() / 1e6
active_pct = obs[obs['indicator_code'] ==
                 'ACTIVE_MM_ACCOUNTS_PCT']['value_numeric'].max()

col1.metric("Account Ownership (2024)", f"{latest_access:.1f}%")
col2.metric("Digital Payment Usage (2024)", f"{latest_usage:.1f}%")
col3.metric("Mobile Money Accounts (2025)", f"{latest_mm:.1f} million")
col4.metric("Active Rate (2025)", f"{active_pct:.1f}%")

st.markdown("---")

# ────────────────────────────────────────────────
# TRENDS SECTION
# ────────────────────────────────────────────────
st.subheader("Historical Trends")

indicator_choice = st.selectbox(
    "Select Indicator", ["ACC_OWNERSHIP",
                         "USG_DIGITAL_PAYMENT", "ACC_MM_ACCOUNT"]
)

trend_data = obs[obs['indicator_code'] ==
                 indicator_choice].sort_values('observation_date')

fig_trend = px.line(
    trend_data,
    x='observation_date',
    y='value_numeric',
    title=f"{indicator_choice} Historical Trend",
    labels={'value_numeric': '% Adults', 'observation_date': 'Date'},
    markers=True
)

# Add event lines
fig_trend.add_vline(x='2021-05-01', line_dash="dash",
                    line_color="red", annotation_text="Telebirr")
fig_trend.add_vline(x='2023-08-01', line_dash="dash",
                    line_color="green", annotation_text="M-Pesa")
fig_trend.add_vline(x='2025-12-09', line_dash="dash",
                    line_color="purple", annotation_text="NDPS Launch")

st.plotly_chart(fig_trend, use_container_width=True)

# ────────────────────────────────────────────────
# FORECASTS SECTION
# ────────────────────────────────────────────────
st.subheader(f"{scenario} Scenario Forecast (Access & Usage)")

if scenario == "Optimistic":
    access_col = 'optimistic_access'
    usage_col = 'optimistic_usage'
elif scenario == "Pessimistic":
    access_col = 'pessimistic_access'
    usage_col = 'pessimistic_usage'
else:
    access_col = 'baseline_access'
    usage_col = 'baseline_usage'

fig_forecast = go.Figure()

fig_forecast.add_trace(go.Scatter(
    x=forecast['year_int'],
    y=forecast[access_col],
    mode='lines+markers',
    name='Access Forecast',
    line=dict(color='blue')
))

fig_forecast.add_trace(go.Scatter(
    x=forecast['year_int'],
    y=forecast[usage_col],
    mode='lines+markers',
    name='Usage Forecast',
    line=dict(color='orange'),
    yaxis='y2'
))

fig_forecast.update_layout(
    title=f"{scenario} Scenario: Access & Usage 2025–2027",
    xaxis_title="Year",
    yaxis_title="Access (%)",
    yaxis2=dict(title="Usage (%)", overlaying='y', side='right'),
    legend=dict(orientation="h", yanchor="bottom",
                y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig_forecast, use_container_width=True)

# ────────────────────────────────────────────────
# DOWNLOAD DATA
# ────────────────────────────────────────────────
st.markdown("---")
csv = forecast.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Forecast CSV",
    data=csv,
    file_name="ethiopia_fi_forecast_2025_2027.csv",
    mime="text/csv"
)

st.markdown(
    "**Note**: Forecasts are illustrative with wide uncertainty (±10–15 pp) due to limited historical Findex points (triennial). "
    "Key drivers: NDPS 2026–2030 activation targets and Fayda ID scale-up."
)
