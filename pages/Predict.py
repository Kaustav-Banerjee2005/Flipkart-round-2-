import streamlit as st
import pandas as pd
import joblib
import os 
priority_model = joblib.load(
    "models/priority_early.pkl"
)

barricade_model = joblib.load(
    "models/barricade_early.pkl"
)

diversion_model = joblib.load(
    "models/diversion_early.pkl"
)

manpower_model = joblib.load(
    "models/manpower_early.pkl"
)
encoders = joblib.load(
    "encoders/early_encoders.pkl"
)
df = pd.read_csv(
    "data/Cleaned_Dataset.csv"
)
event_type = st.selectbox(
    "Event Type",
    sorted(df["event_type"].unique())
)

event_cause = st.selectbox(
    "Event Cause",
    sorted(df["event_cause"].unique())
)

veh_type = st.selectbox(
    "Vehicle Type",
    sorted(df["veh_type"].unique())
)
latitude = st.number_input(
    "Latitude",
    value=float(df["latitude"].mean())
)

longitude = st.number_input(
    "Longitude",
    value=float(df["longitude"].mean())
)
hour = st.slider(
    "Hour",
    0,
    23,
    12
)
is_weekend = st.checkbox(
    "Weekend"
)
peak_hour = (
    1 if (
        7 <= hour <= 10
        or
        17 <= hour <= 20
    )
    else 0
)
month = st.slider(
    "Month",
    1,
    12,
    1
)
vehicle_severity = st.slider(
    "Vehicle Severity",
    1,
    5,
    3
)

cause_severity = st.slider(
    "Cause Severity",
    1,
    5,
    3
)
event_type_enc = (
    encoders["event_type"]
    .transform([event_type])[0]
)

event_cause_enc = (
    encoders["event_cause"]
    .transform([event_cause])[0]
)

veh_type_enc = (
    encoders["veh_type"]
    .transform([veh_type])[0]
)
input_data = pd.DataFrame({

    "event_type":[event_type_enc],

    "event_cause":[event_cause_enc],

    "veh_type":[veh_type_enc],

    "latitude":[latitude],

    "longitude":[longitude],

    "hour":[hour],

    "peak_hour":[peak_hour],

    "month":[month],

    "is_weekend":[int(is_weekend)],

    "vehicle_severity":[vehicle_severity],

    "cause_severity":[cause_severity]

})
if st.button("Generate AI Assessment"):
    priority = priority_model.predict(input_data)[0]
    priority_conf = (priority_model.predict_proba(input_data).max() * 100)
    st.metric("Priority Confidence",f"{priority_conf:.2f}%")
    barricade = barricade_model.predict(input_data)[0]
    diversion = diversion_model.predict(input_data)[0]
    manpower = manpower_model.predict(input_data)[0]
    st.success(f"Priority : {priority}")
    st.info(f"Barricade : {barricade}")
    st.warning(f"Diversion : {diversion}")
    st.error(f"Manpower : {manpower}")


