import streamlit as st

# --- IMPORTING FROM THE PAGES FOLDER ---
from modules.Introduction import main as introduction_page
from modules.Dashboard import main as Dashboard_page
from modules.About_Me import main as about_me_page
from modules.Accident import main as accident_page
from modules.Traffic import main as traffic_page
from modules.Crowd import main as crowd_page
from modules.Road_Damage import main as road_page
from modules.Air_Quality import main as air_page
from modules.Sentiment import main as sentiment_page
from modules.Chatbot import main as chatbot_page

# --- GLOBAL CONFIG ---
st.set_page_config(
    page_title="UrbanGuard AI | Smart City OS",
    page_icon="🏙️",
    layout="wide"
)

def main():
    # --- SIDEBAR NAV ---
    st.sidebar.title("🏙️ UrbanGuard AI")
    st.sidebar.caption("SaaS Edition v2.0")
    
    # Dictionary mapping for clean navigation logic
    nav_menu = {
        "Project Introduction": introduction_page,
        "Executive Dashboard": Dashboard_page,
        "Accident Detection": accident_page,
        "Traffic Flow Analysis": traffic_page,
        "Crowd Density Monitoring": crowd_page,
        "Road Damage Assessment": road_page,
        "Air Quality Predictor": air_page,
        "Sentiment Analysis": sentiment_page,
        "UrbanChatbot":chatbot_page,
        "Developer Portfolio": about_me_page
    }
    
    # Sidebar Radio for selection
    selection = st.sidebar.radio("Navigation Menu", list(nav_menu.keys()))
    
    # --- RENDER THE SELECTED PAGE ---
    # This executes the function you imported above
    nav_menu[selection]()


if __name__ == "__main__":
    main()