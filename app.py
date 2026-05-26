import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Malaysia Demographic Dashboard", layout="wide")

st.title("Malaysia Population Demographic Dashboard (DOSM)")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    url = "https://storage.dosm.gov.my/population/population_district.parquet"
    df = pd.read_parquet(url)

    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()


# =========================
# KPI SECTION
# =========================
st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Population", f"{df['population'].sum():,.0f}")
col2.metric("Average Population", f"{df['population'].mean():,.0f}")
col3.metric("Total Districts", df["district"].nunique())

# =========================
# 1. TREND OVER TIME
# =========================
st.subheader("Population Trend Over Time")

trend = df.groupby("date")["population"].sum().reset_index()

fig1 = px.line(
    trend,
    x="date",
    y="population",
    markers=True,
    title="Population Growth Over Time"
)

st.plotly_chart(fig1, use_container_width=True)

# =========================
# 2. TOP DISTRICTS
# =========================
st.subheader("Top 10 Districts by Population")

top_district = df.groupby("district")["population"].sum().nlargest(10).reset_index()

fig2 = px.bar(
    top_district,
    x="district",
    y="population",
    text_auto=True,
    title="Top 10 Districts"
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# 3. SEX DISTRIBUTION
# =========================
st.subheader("Gender Distribution")

sex_df = df.groupby("sex")["population"].sum().reset_index()

fig3 = px.pie(
    sex_df,
    names="sex",
    values="population",
    title="Population by Gender"
)

st.plotly_chart(fig3, use_container_width=True)

# =========================
# 4. AGE DISTRIBUTION
# =========================
st.subheader("Age Distribution")

age_df = df.groupby("age")["population"].sum().reset_index()

fig4 = px.bar(
    age_df,
    x="age",
    y="population",
    title="Population by Age Group"
)

st.plotly_chart(fig4, use_container_width=True)

# =========================
# 5. ETHNICITY DISTRIBUTION
# =========================
st.subheader("Ethnicity Distribution")

eth_df = df.groupby("ethnicity")["population"].sum().reset_index()

fig5 = px.pie(
    eth_df,
    names="ethnicity",
    values="population",
    title="Population by Ethnicity"
)

st.plotly_chart(fig5, use_container_width=True)