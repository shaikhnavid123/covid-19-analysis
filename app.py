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

page = st.sidebar.radio(
    "Navigation",
    ["Overview", "Global Trends", "Country Analysis", "Forecast", "Dataset Explorer"]
)

if page == "Overview":

    st.header("🌍 Global Overview")

    total_cases = df["Confirmed"].sum()
    total_deaths = df["Deaths"].sum()
    total_recovered = df["Recovered"].sum()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Cases", f"{total_cases:,}")
    col2.metric("Total Deaths", f"{total_deaths:,}")
    col3.metric("Total Recovered", f"{total_recovered:,}")

    country_cases = df.groupby("Country/Region")["Confirmed"].sum().reset_index()

    fig = px.bar(
        country_cases.sort_values(by="Confirmed", ascending=False).head(10),
        x="Country/Region",
        y="Confirmed",
        title="Top 10 Countries by Cases"
    )

    st.plotly_chart(fig, use_container_width=True)

elif page == "Country Analysis":

    st.header("🌎 Country Analysis")

    country = st.selectbox("Select Country", df["Country/Region"].unique())

    country_df = df[df["Country/Region"] == country]

    trend = country_df.groupby("Date")[["Confirmed","Deaths","Recovered"]].sum().reset_index()

    fig = px.line(
        trend,
        x="Date",
        y=["Confirmed","Deaths","Recovered"],
        title=f"COVID Trend in {country}"
    )

    st.plotly_chart(fig, use_container_width=True)

elif page == "Forecast":

    st.header("📊 COVID Case Forecast")

    data = df.groupby("Date")["Confirmed"].sum().reset_index()

    data["Day"] = range(len(data))

    from sklearn.linear_model import LinearRegression
    model = LinearRegression()

    X = data[["Day"]]
    y = data["Confirmed"]

    model.fit(X,y)

    future_days = 30
    future_X = [[i] for i in range(len(data), len(data)+future_days)]

    predictions = model.predict(future_X)

    future_dates = pd.date_range(data["Date"].max(), periods=future_days+1)[1:]

    forecast_df = pd.DataFrame({
        "Date":future_dates,
        "Forecast":predictions
    })

    fig = px.line(data, x="Date", y="Confirmed", title="COVID Forecast")

    fig.add_scatter(
        x=forecast_df["Date"],
        y=forecast_df["Forecast"],
        mode="lines",
        name="Predicted Cases"
    )

    st.plotly_chart(fig, use_container_width=True)

elif page == "Dataset Explorer":

    st.header("📂 Dataset Explorer")

    st.write("Dataset Shape:", df.shape)

    st.dataframe(df)

    st.download_button(
        "Download Dataset",
        df.to_csv(index=False),
        "covid_dataset.csv",
        "text/csv"
    )



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
