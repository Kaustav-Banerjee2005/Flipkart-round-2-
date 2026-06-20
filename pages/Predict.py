import streamlit as st
import pandas as pd
import joblib

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Incident Prediction",
    page_icon="🚦",
    layout="wide"
)

st.title("🚦 AI Traffic Incident Assessment")

# ==========================================
# LOAD MODELS
# ==========================================

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

# ==========================================
# LOAD ENCODERS
# ==========================================

encoders = joblib.load(
    "encoders/early_encoders.pkl"
)

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(
    "data/Cleaned_Dataset.csv"
)

# ==========================================
# INPUT SECTION
# ==========================================

st.subheader("Incident Details")

col1, col2 = st.columns(2)

with col1:

    event_type = st.selectbox(
        "Event Type",
        sorted(
            df["event_type"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    event_cause = st.selectbox(
        "Event Cause",
        sorted(
            df["event_cause"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    veh_type = st.selectbox(
        "Vehicle Type",
        sorted(
            df["veh_type"]
            .dropna()
            .unique()
            .tolist()
        )
    )

with col2:

    location = st.selectbox(
        "Incident Location",
        sorted(
            df["address"]
            .dropna()
            .unique()
            .tolist()
        )
    )

# ==========================================
# LOCATION LOOKUP
# ==========================================

location_row = df[
    df["address"] == location
].iloc[0]

latitude = location_row["latitude"]

longitude = location_row["longitude"]

zone = location_row["zone"]

corridor = location_row["corridor"]

st.info(
    f"""
📍 Location: {location}

🏙 Zone: {zone}

🛣 Corridor: {corridor}
"""
)

# ==========================================
# TIME FEATURES
# ==========================================

st.subheader("Time Information")

col1, col2, col3 = st.columns(3)

with col1:

    hour = st.slider(
        "Hour",
        0,
        23,
        12
    )

with col2:

    month = st.slider(
        "Month",
        1,
        12,
        1
    )

with col3:

    is_weekend = st.checkbox(
        "Weekend"
    )

# ==========================================
# PEAK HOUR
# ==========================================

peak_hour = (
    1
    if (
        7 <= hour <= 10
        or
        17 <= hour <= 20
    )
    else 0
)

# ==========================================
# SEVERITY FEATURES
# ==========================================

st.subheader("Severity Assessment")

col1, col2 = st.columns(2)

with col1:

    vehicle_severity = st.slider(
        "Vehicle Severity",
        1,
        5,
        3
    )

with col2:

    cause_severity = st.slider(
        "Cause Severity",
        1,
        5,
        3
    )

# ==========================================
# ENCODING
# ==========================================

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

# ==========================================
# MODEL INPUT
# ==========================================

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

# ==========================================
# PREDICTION
# ==========================================

if st.button("🚀 Generate AI Assessment"):

    priority = priority_model.predict(
        input_data
    )[0]

   

    barricade = (
        barricade_model
        .predict(input_data)[0]
    )

    diversion = (
        diversion_model
        .predict(input_data)[0]
    )

    manpower = (
        manpower_model
        .predict(input_data)[0]
    )

    # ======================================
    # RESULTS
    # ======================================

    st.subheader("AI Assessment Results")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.success(
            f"Priority\n\n{priority}"
        )

    with col2:
        st.info(
            f"Barricade\n\n{barricade}"
        )

    with col3:
        st.warning(
            f"Diversion\n\n{diversion}"
        )

    with col4:
        st.error(
            f"Manpower\n\n{manpower}"
        )



    # ======================================
    # AI INTERPRETATION
    # ======================================

    st.subheader("🤖 AI Incident Interpretation")

    st.info(
        f"""
Incident Type: {event_type}

Cause: {event_cause}

Vehicle Type: {veh_type}

Location: {location}

Zone: {zone}

Corridor: {corridor}

Predicted Priority: {priority}

Diversion Required: {diversion}

Manpower Requirement: {manpower}

The AI system analyzed incident characteristics, location, traffic timing and severity indicators to estimate operational response requirements.
"""
    )

    # ======================================
    # RECOMMENDED ACTION
    # ======================================

    st.subheader("🚔 Recommended Response Plan")

    if manpower == "High":
        officers = 8
    elif manpower == "Medium":
        officers = 5
    else:
        officers = 2

    st.success(
        f"""
Deploy Officers: {officers}

Barricade Required: {barricade}

Diversion Required: {diversion}

Location: {location}

Zone: {zone}

Corridor: {corridor}
"""
    )
