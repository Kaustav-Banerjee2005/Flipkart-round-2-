import streamlit as st
import pandas as pd
import plotly.express as px
df = pd.read_csv(
    "data/Cleaned_Dataset.csv"
)
st.title("📊 City Traffic Analytics")
corridor_df = (
    df["corridor"]
    .value_counts()
    .reset_index()
)

corridor_df.columns = [
    "Corridor",
    "Events"
]
fig = px.bar(
    corridor_df.head(10),
    x="Corridor",
    y="Events",
    title="Top Congested Corridors"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
cause_df = (
    df["event_cause"]
    .value_counts()
    .reset_index()
)

cause_df.columns = [
    "Cause",
    "Count"
]
fig = px.pie(
    cause_df.head(10),
    names="Cause",
    values="Count",
    title="Event Cause Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
veh_df = (
    df["veh_type"]
    .value_counts()
    .reset_index()
)

veh_df.columns = [
    "Vehicle",
    "Count"
]
fig = px.bar(
    veh_df,
    x="Vehicle",
    y="Count",
    title="Vehicle Type Analysis"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
priority_df = (
    df["priority"]
    .value_counts()
    .reset_index()
)

priority_df.columns = [
    "Priority",
    "Count"
]
fig = px.pie(
    priority_df,
    names="Priority",
    values="Count",
    title="Priority Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
closure_df = (
    df["requires_road_closure"]
    .value_counts()
    .reset_index()
)

closure_df.columns = [
    "Road Closure",
    "Count"
]
fig = px.bar(
    closure_df,
    x="Road Closure",
    y="Count",
    title="Road Closure Requirements"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
