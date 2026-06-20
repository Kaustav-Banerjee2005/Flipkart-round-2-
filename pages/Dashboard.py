import streamlit as st
import pandas as pd
import pydeck as pdk

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Traffic Command Center",
    page_icon="🚦",
    layout="wide"
)

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv("data/Cleaned_Dataset.csv")

# ==========================================
# DATA CLEANING
# ==========================================

df["latitude"] = pd.to_numeric(
    df["latitude"],
    errors="coerce"
)

df["longitude"] = pd.to_numeric(
    df["longitude"],
    errors="coerce"
)

df = df.dropna(
    subset=[
        "latitude",
        "longitude"
    ]
)

# ==========================================
# TITLE
# ==========================================

st.title("🚦 Live Command Dashboard")

# ==========================================
# KPI SECTION
# ==========================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Incidents",
        len(df)
    )

with col2:
    st.metric(
        "High Priority",
        len(
            df[
                df["priority"] == "High"
            ]
        )
    )

with col3:
    st.metric(
        "Road Closures",
        len(
            df[
                df["requires_road_closure"] == True
            ]
        )
    )

with col4:
    st.metric(
        "Corridors",
        df["corridor"].nunique()
    )

st.divider()

# ==========================================
# SIDEBAR FILTERS
# ==========================================

st.sidebar.header("Filters")

priority_filter = st.sidebar.multiselect(
    "Priority",
    options=sorted(
        df["priority"]
        .dropna()
        .unique()
        .tolist()
    ),
    default=sorted(
        df["priority"]
        .dropna()
        .unique()
        .tolist()
    )
)

zone_filter = st.sidebar.selectbox(
    "Zone",
    ["All"] +
    sorted(
        df["zone"]
        .dropna()
        .unique()
        .tolist()
    )
)

corridor_filter = st.sidebar.selectbox(
    "Corridor",
    ["All"] +
    sorted(
        df["corridor"]
        .dropna()
        .unique()
        .tolist()
    )
)

cause_filter = st.sidebar.selectbox(
    "Event Cause",
    ["All"] +
    sorted(
        df["event_cause"]
        .dropna()
        .unique()
        .tolist()
    )
)

# ==========================================
# APPLY FILTERS
# ==========================================

filtered_df = df.copy()

# Priority

filtered_df = filtered_df[
    filtered_df["priority"]
    .isin(priority_filter)
]

# Zone

if zone_filter != "All":

    filtered_df = filtered_df[
        filtered_df["zone"]
        == zone_filter
    ]

# Corridor

if corridor_filter != "All":

    filtered_df = filtered_df[
        filtered_df["corridor"]
        == corridor_filter
    ]

# Event Cause

if cause_filter != "All":

    filtered_df = filtered_df[
        filtered_df["event_cause"]
        == cause_filter
    ]

# ==========================================
# MAP COLORS
# ==========================================

filtered_df["color"] = (
    filtered_df["priority"]
    .map({
        "High": [255, 0, 0, 220],
        "Low": [0, 255, 0, 220]
    })
)

# ==========================================
# MAP SECTION
# ==========================================

st.subheader("🗺 Bengaluru Traffic Incident Map")

view_state = pdk.ViewState(
    latitude=12.9716,
    longitude=77.5946,
    zoom=11,
    pitch=35
)

layer = pdk.Layer(
    "ScatterplotLayer",
    data=filtered_df,
    get_position='[longitude, latitude]',
    get_fill_color='color',
    get_radius=150,
    pickable=True,
    auto_highlight=True
)

tooltip = {
    "html": """
    <b>🚨 Event:</b> {event_type}<br/>
    <b>⚠ Cause:</b> {event_cause}<br/>
    <b>🔥 Priority:</b> {priority}<br/>
    <b>🛣 Corridor:</b> {corridor}<br/>
    <b>📍 Zone:</b> {zone}
    """
}

st.pydeck_chart(
    pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style="road"
    )
)

st.divider()

# ==========================================
# ANALYTICS
# ==========================================

col1, col2 = st.columns(2)

# Top Corridors

with col1:

    st.subheader("📊 Top Risk Corridors")

    corridor_stats = (
        filtered_df["corridor"]
        .value_counts()
        .head(10)
    )

    st.bar_chart(corridor_stats)

# Top Causes

with col2:

    st.subheader("⚠ Top Event Causes")

    cause_stats = (
        filtered_df["event_cause"]
        .value_counts()
        .head(10)
    )

    st.bar_chart(cause_stats)

# ==========================================
# AI INSIGHTS
# ==========================================

st.divider()

st.subheader("🤖 AI Insights")

if len(filtered_df) > 0:

    top_corridor = (
        filtered_df["corridor"]
        .value_counts()
        .idxmax()
    )

    top_cause = (
        filtered_df["event_cause"]
        .value_counts()
        .idxmax()
    )

    st.info(
        f"""
Highest Risk Corridor: {top_corridor}

Most Frequent Event Cause: {top_cause}

Visible Incidents After Filters: {len(filtered_df)}

Recommendation:
Traffic authorities should prioritize monitoring the highest-risk corridors and recurring incident causes to reduce congestion impact.
"""
    )

else:

    st.warning(
        "No incidents match the selected filters."
    )