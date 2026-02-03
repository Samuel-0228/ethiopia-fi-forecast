import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Ethiopia Financial Inclusion Dashboard", layout="wide")

# ────────────────────────────────────────────────
# LOAD DATA (update paths to your files)
# ────────────────────────────────────────────────


@st.cache_data
def load_data():
    enriched_path = "../data/processed/ethiopia_fi_unified_enriched_20260131.csv"
    forecast_path = "../reports/figures/task4_annual_forecast_2025_2027.csv"  # from Task 4

    df = pd.read_csv(enriched_path, parse_dates=['observation_date'])
    try:
        forecast = pd.read_csv(forecast_path)
    except FileNotFoundError:
        forecast = pd.DataFrame({  # fallback dummy data
            'year_int': [2025, 2026, 2027],
            'baseline_access': [50, 54, 57],
            'optimistic_access': [53, 60, 65],
            'pessimistic_access': [49, 51, 53],
            'baseline_usage': [22, 26, 30],
            'optimistic_usage': [25, 32, 40],
            'pessimistic_usage': [21, 24, 27]
        })
    return df, forecast


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
    "Data enriched up to 2025; forecasts are scenario-based with wide uncertainty due to sparse historical points.")

# ────────────────────────────────────────────────
# MAIN PAGE
# ────────────────────────────────────────────────
st.title("Ethiopia Financial Inclusion Forecasting Dashboard")
st.markdown(
    "**Access** (Account Ownership) & **Usage** (Digital Payments) Trends & Projections 2025–2027")

# ────────────────────────────────────────────────
# OVERVIEW METRICS
# ────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

latest_access = obs[obs['indicator_code'] ==
                    'ACC_OWNERSHIP']['value_numeric'].max()
latest_usage = obs[obs['indicator_code'] == 'USG_DIGITAL_PAYMENT']['value_numeric'].max(
) if not obs[obs['indicator_code'] == 'USG_DIGITAL_PAYMENT'].empty else 21.0
latest_mm = obs[obs['indicator_code'] ==
                'MOBILE_MONEY_ACCOUNTS_TOTAL']['value_numeric'].max() / 1e6
active_pct = obs[obs['indicator_code'] ==
                 'ACTIVE_MM_ACCOUNTS_PCT']['value_numeric'].max()

col1.metric("Account Ownership (2024)", f"{latest_access}%")
col2.metric("Digital Payment Usage (2024)", f"{latest_usage}%")
col3.metric("Mobile Money Accounts (2025)", f"{latest_mm:.1f} million")
col4.metric("Active Rate (2025)", f"{active_pct}%")

st.markdown("---")

# ────────────────────────────────────────────────
# TRENDS TAB-LIKE SECTION
# ────────────────────────────────────────────────
st.subheader("Historical Trends")

indicator_choice = st.selectbox(
    "Select Indicator", ["ACC_OWNERSHIP", "USG_DIGITAL_PAYMENT", "ACC_MM_ACCOUNT"])

trend_data = obs[obs['indicator_code'] ==
                 indicator_choice].sort_values('observation_date')

fig_trend = px.line(trend_data, x='observation_date', y='value_numeric',
                    title=f"{indicator_choice} Historical Trend",
                    labels={'value_numeric': '% Adults',
                            'observation_date': 'Date'},
                    markers=True)

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

# Access forecast
fig_forecast.add_trace(go.Scatter(
    x=forecast['year_int'], y=forecast[access_col],
    mode='lines+markers', name='Access Forecast', line=dict(color='blue')
))

# Usage forecast (secondary axis)
fig_forecast.add_trace(go.Scatter(
    x=forecast['year_int'], y=forecast[usage_col],
    mode='lines+markers', name='Usage Forecast', line=dict(color='orange'),
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

st.markdown("**Note**: Forecasts are illustrative with wide uncertainty (±10–15 pp) due to limited historical Findex points (triennial). Key drivers: NDPS 2026–2030 activation targets and Fayda ID scale-up.")
