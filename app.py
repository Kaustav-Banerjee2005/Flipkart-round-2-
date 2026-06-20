import streamlit as st

st.set_page_config(
    page_title="AI Traffic Command Center",
    page_icon="🚦",
    layout="wide"
)

st.title("🚦 Bengaluru Traffic Command Center")

st.markdown("""
### AI-Powered Event Driven Congestion Management

This system helps Bengaluru Traffic Police:

- Predict Incident Priority
- Recommend Barricades
- Recommend Diversions
- Recommend Manpower Deployment
- Visualize City-wide Traffic Risks

Use the navigation panel on the left.
""")

st.image(
    "https://images.unsplash.com/photo-1519501025264-65ba15a82390",
    use_container_width=True
)