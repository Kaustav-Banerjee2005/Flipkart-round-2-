import streamlit as st

st.set_page_config(layout="wide")

st.title("🚔 AI Resource Planning")

st.markdown("""
Generate operational recommendations for Bengaluru Traffic Police.
""")
priority = st.selectbox(
    "Predicted Priority",
    ["Low", "High"]
)

barricade = st.selectbox(
    "Barricade Required",
    ["No", "Yes"]
)

diversion = st.selectbox(
    "Diversion Required",
    ["No", "Yes"]
)

manpower = st.selectbox(
    "Manpower Level",
    ["Low", "Medium", "High"]
)
officers = 0
barricades = 0
tow_vehicles = 0

if manpower == "Low":
    officers = 2

elif manpower == "Medium":
    officers = 5

elif manpower == "High":
    officers = 8
if barricade == "Yes":
    barricades = 4
if priority == "High":
    tow_vehicles = 1
st.subheader("📋 AI Action Plan")

col1,col2,col3 = st.columns(3)

with col1:
    st.metric(
        "Police Officers",
        officers
    )

with col2:
    st.metric(
        "Barricades",
        barricades
    )

with col3:
    st.metric(
        "Tow Vehicles",
        tow_vehicles
    )
