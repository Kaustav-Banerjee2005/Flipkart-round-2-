import streamlit as st
import pandas as pd

df = pd.read_csv(
    "data/Cleaned_Dataset.csv"
)

st.title("Live Command Dashboard")
col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric(
        "Total Incidents",
        len(df)
    )

with col2:
    st.metric(
        "High Priority",
        (df["priority"]=="High").sum()
    )

with col3:
    st.metric(
        "Road Closures",
        df["requires_road_closure"].sum()
    )

with col4:
    st.metric(
        "Corridors",
        df["corridor"].nunique()
    )
st.map(
    df[
        ["latitude","longitude"]
    ]
)