import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="UAC Care Load Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("System Capacity & Care Load Analytics")
st.caption(
    "Unaccompanied Children Care System"
)

@st.cache_data
def load_data():
    return pd.read_csv(
        "data/processed/uac_features.csv",
        parse_dates=["Date"]
    )

df = load_data()

st.sidebar.header("Filters")

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

start_date = st.sidebar.date_input(
    "Start Date",
    min_date
)

end_date = st.sidebar.date_input(
    "End Date",
    max_date
)
filtered_df = df[
    (df["Date"].dt.date >= start_date) &
    (df["Date"].dt.date <= end_date)
]

if filtered_df.empty:
    st.warning("No data found for the selected date range. Please select a valid date range.")
    st.stop()

latest = filtered_df.iloc[-1]

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Under Care",
    f"{latest['total_system_load']:,.0f}"
)

col2.metric(
    "CBP Load",
    f"{latest['Children in CBP custody']:,.0f}"
)

col3.metric(
    "HHS Load",
    f"{latest['Children in HHS Care']:,.0f}"
)

col4.metric(
    "Net Intake",
    f"{latest['net_intake']:,.0f}"
)
fig = px.line(
    filtered_df,
    x="Date",
    y="total_system_load",
    title="Total System Load"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
fig = px.line(
    filtered_df,
    x="Date",
    y=[
        "Children in CBP custody",
        "Children in HHS Care"
    ],
    title="CBP vs HHS Care"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
fig = px.line(
    filtered_df,
    x="Date",
    y=[
        "Children transferred out of CBP custody",
        "Children discharged from HHS Care"
    ],
    title="Transfers vs Discharges"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

fig = px.bar(
    filtered_df,
    x="Date",
    y="net_intake",
    title="Net Intake Pressure"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("Data Quality")

quality_count = int(
    df["data_quality_flag"].sum()
)

st.write(
    f"Flagged transfer/discharge records: {quality_count}"
)

st.write(
    "The dataset contains missing calendar dates. "
    "Missing dates are not assumed to represent zero activity."
)