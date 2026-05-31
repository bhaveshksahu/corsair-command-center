import streamlit as st
import requests

# Set page configuration for a dark-themed, professional look
st.set_page_config(
    page_title="Corsair Student Cockpit",
    page_icon="🏴‍☠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and Description
st.title("🏴‍☠️ Corsair Student Command Center")
st.markdown("---")

# Sidebar Configuration for control mechanics
with st.sidebar:
    st.header("⚡ Control Deck")
    # The Winner Feature: The Hackathon Mode Toggle Switch
    hackathon_mode = st.toggle("Activate Hackathon Mode", value=False)
    
    st.markdown("---")
    st.markdown("### 🔌 Core Engines Status")
    st.success("FastAPI Backend: Online")
    st.success("Coral Data Protocol: Ready")

# Backend integration API URL
API_URL = "http://127.0.0.1:8000/api/intelligence"

# Display dynamic headers based on the toggle state
if hackathon_mode:
    st.warning("⚠️ **HACKATHON MODE ACTIVATED** — Academic tasks deprioritized. Displaying active dev repositories & sprint issues.")
else:
    st.info("📚 **STANDARD MODE** — Displaying unified view of academic tasks synced with repository issues.")

# Fetching the unified cross-source data payload
try:
    with st.spinner("Coral Engine executing cross-source relational query..."):
        response = requests.post(API_URL, json={"hackathon_mode": hackathon_mode})
        
    if response.status_code == 200:
        payload = response.json()
        items = payload.get("data", [])
        
        if not items:
            st.info("No active cross-source matches found. Seed your Notion or GitHub with matching tags to view relational links.")
        else:
            # Layout the matched records dynamically into cards
            for idx, item in enumerate(items):
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.subheader(f"🔗 {item.get('academic_task', 'Untitled Task')}")
                        st.write(f"**Linked Issue:** {item.get('repository_issue')}")
                    with col2:
                        st.write("")
                        st.write("")
                        st.link_button("View Code Issue", item.get('direct_link', '#'))
                    st.markdown("---")
    else:
        st.error(f"Backend Server returned an error: {response.text}")

except requests.exceptions.ConnectionError:
    st.error("Could not connect to the FastAPI backend. Make sure main.py is running on port 8000.")