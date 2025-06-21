
import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("dashboard_data.csv")
df = df.dropna(subset=["crude_mortality", "year", "country"])

# Page layout
st.set_page_config(layout="wide")
st.title("📊 Global Suicide Analytics Dashboard")
st.markdown("**Powered by WHO & OWID | Designed for MSBA350**")

# Sidebar Filters
st.sidebar.header("🔍 Filter")
year = st.sidebar.slider("Year", int(df["year"].min()), int(df["year"].max()), 2019)
country = st.sidebar.selectbox("Country", sorted(df["country"].dropna().unique()))

filtered_df = df[df["year"] == year]
country_df = df[df["country"] == country]

# === TOP METRICS (KPI cards in a row) ===
latest = country_df[country_df["year"] == year]

st.markdown("### 🔢 Key Indicators")
kpi1, kpi2, kpi3 = st.columns(3)
if not latest.empty:
    kpi1.metric("Crude Mortality", f"{latest['crude_mortality'].values[0]:.2f} / 100k")
    kpi2.metric("Male-to-Female Ratio", f"{latest['male_to_female_suicide_death_rate_ratio_age_standardized'].values[0]:.2f}")
    if "incidence_per_100k" in latest.columns:
        kpi3.metric("Incidence Rate", f"{latest['incidence_per_100k'].values[0]:.2f} / 100k")

# === ROW 1: Trend by Year, Age Distribution, Gender Ratio ===
st.markdown("### 📈 Suicide Trends & Demographics")
col1, col2, col3 = st.columns(3)

# Line chart: trend over time
with col1:
    fig = px.line(country_df, x="year", y="crude_mortality", markers=True,
                  title=f"Crude Mortality Over Time — {country}")
    st.plotly_chart(fig, use_container_width=True)

# Bar chart: age distribution
with col2:
    age_cols = [c for c in df.columns if "aged_" in c and "both_sexes" in c]
    if age_cols and not latest.empty:
        age_data = latest[age_cols].T.dropna()
        age_data.columns = ["rate"]
        age_data = age_data.sort_values("rate")
        st.bar_chart(age_data)

# Gender trend
with col3:
    if "male_to_female_suicide_death_rate_ratio_age_standardized" in country_df.columns:
        fig = px.line(country_df.dropna(subset=["male_to_female_suicide_death_rate_ratio_age_standardized"]),
                      x="year", y="male_to_female_suicide_death_rate_ratio_age_standardized",
                      title=f"M:F Suicide Ratio — {country}", markers=True)
        st.plotly_chart(fig, use_container_width=True)

# === ROW 2: Map, Top 10 Countries, Country Comparison ===
st.markdown("### 🌍 Regional Analysis & Rankings")
col4, col5, col6 = st.columns(3)

# Map: Global distribution
with col4:
    map_fig = px.choropleth(filtered_df,
                            locations="country",
                            locationmode="country names",
                            color="crude_mortality",
                            color_continuous_scale="Reds",
                            title=f"Suicide Rate Map — {year}")
    st.plotly_chart(map_fig, use_container_width=True)

# Bar: Top 10 countries
with col5:
    top10 = filtered_df.sort_values("crude_mortality", ascending=False).head(10)
    fig = px.bar(top10, x="country", y="crude_mortality", color="country",
                 title=f"Top 10 Countries — {year}", text_auto=".2s")
    st.plotly_chart(fig, use_container_width=True)

# Pie: Region/country share (Optional Placeholder)
with col6:
    region_data = top10.groupby("country")["crude_mortality"].mean().reset_index()
    fig = px.pie(region_data, names="country", values="crude_mortality", title="Top 10 Country Share")
    st.plotly_chart(fig, use_container_width=True)
