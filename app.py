# If not already installed, do: pip install pandas fastparquet
import pandas as pd

URL_DATA = 'https://storage.dosm.gov.my/population/population_district.parquet'

df = pd.read_parquet(URL_DATA)
if 'date' in df.columns: df['date'] = pd.to_datetime(df['date'])

print(df)

import streamlit as st
import pandas as pd
import plotly.express as px

st.title("DOSM Population Dashboard (District Level)")

# Load data
@st.cache_data
def load_data():
    URL_DATA = "https://storage.dosm.gov.my/population/population_district.parquet"
    df = pd.read_parquet(URL_DATA)

    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])

    return df

df = load_data()

# Show data
st.subheader("Raw Data")
st.dataframe(df)

# Filters 
st.subheader("Filters")

if 'state' in df.columns:
    state = st.selectbox("Select State", df['state'].unique())
    df = df[df['state'] == state]

if 'date' in df.columns:
    date_range = st.date_input("Select Date Range",
                               [df['date'].min(), df['date'].max()])
    df = df[(df['date'] >= pd.to_datetime(date_range[0])) &
            (df['date'] <= pd.to_datetime(date_range[1]))]

# Chart options
st.subheader("Visualization")

columns = df.select_dtypes(include=['number']).columns.tolist()

if len(columns) >= 1:
    y_axis = st.selectbox("Select Value Column", columns)

    if 'date' in df.columns:
        fig = px.line(df, x='date', y=y_axis, title="Trend Over Time")
    else:
        fig = px.bar(df, y=y_axis, title="Value Distribution")

    st.plotly_chart(fig)

st.success("Dashboard ready")