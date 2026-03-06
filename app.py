import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="COVID Dashboard", layout="wide")

st.title("🌍 COVID-19 Global Analytics Dashboard")
st.markdown("### Final Year Project - Pandemic Data Analysis")

# ----------------------------
# LOAD DATA
# ----------------------------
df = pd.read_csv(r"C:\Users\Administrator\Downloads\Final Year Project - Covid-19\Navid\combined_covid_dashboard_dataset.csv")

# Detect country column automatically
country_column = None

for col in df.columns:
    if "country" in col.lower():
        country_column = col
        break

if country_column:
    df.rename(columns={country_column: "Country"}, inplace=True)

# Detect date column automatically
date_column = None
for col in df.columns:
    if "date" in col.lower():
        date_column = col
        break

if date_column:
    df[date_column] = pd.to_datetime(df[date_column])
    df.rename(columns={date_column: "Date"}, inplace=True)

# ----------------------------
# SIDEBAR FILTERS
# ----------------------------
st.sidebar.header("Filters")

if "Country" in df.columns:
    countries = st.sidebar.multiselect(
        "Select Country",
        df["Country"].unique()
    )
    if countries:
        df = df[df["Country"].isin(countries)]

# ----------------------------
# KPI SECTION
# ----------------------------
total_cases = df["Confirmed"].sum()
total_deaths = df["Deaths"].sum()
total_recovered = df["Recovered"].sum()

col1, col2, col3 = st.columns(3)

col1.metric("Total Confirmed Cases", f"{total_cases:,.0f}")
col2.metric("Total Deaths", f"{total_deaths:,.0f}")
col3.metric("Total Recovered", f"{total_recovered:,.0f}")

st.markdown("---")

# ----------------------------
# GLOBAL TREND
# ----------------------------
if "Date" in df.columns:
    trend = df.groupby("Date")[["Confirmed","Deaths","Recovered"]].sum().reset_index()

    fig = px.line(
        trend,
        x="Date",
        y=["Confirmed","Deaths","Recovered"],
        title="Global COVID Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# TOP COUNTRIES
# ----------------------------
if "Country" in df.columns:
    country_cases = df.groupby("Country")["Confirmed"].sum().reset_index()

    top10 = country_cases.sort_values(
        by="Confirmed",
        ascending=False
    ).head(10)

    fig2 = px.bar(
        top10,
        x="Country",
        y="Confirmed",
        title="Top 10 Countries by Cases",
        color="Country"
    )

    st.plotly_chart(fig2, use_container_width=True)

# ----------------------------
# DEATH VS RECOVERY
# ----------------------------
country_stats = df.groupby("Country")[["Deaths","Recovered"]].sum().reset_index()

fig3 = px.bar(
    country_stats.head(10),
    x="Country",
    y=["Deaths","Recovered"],
    barmode="group",
    title="Deaths vs Recoveries"
)

st.plotly_chart(fig3, use_container_width=True)

# ----------------------------
# DATA TABLE
# ----------------------------
st.markdown("### Dataset Preview")

st.dataframe(df.head(50))