import os
import logging
import smtplib
import mysql.connector
import pandas as pd
import streamlit as st
import joblib
import numpy as np
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# =================================================================
# 1. CONFIGURATION & DATABASE
# =================================================================
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Config:
    """Centralized AQI system configuration."""
    # Ensure this path points to your actual .pkl file
    MODEL_PATH = "C:/Users/Selva.M/Downloads/data_science/final_project/models/best_model.pkl"
    
    DB_CONFIG = {
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME")
    }

    SMTP_SERVER, SMTP_PORT = "smtp.gmail.com", 587
    SENDER_EMAIL = os.getenv("EMAIL_USER")
    SENDER_PASSWORD = os.getenv("EMAIL_PASS")
    EMERGENCY_EMAIL = os.getenv("EMERGENCY_EMAIL")


# =================================================================
# 2. EMERGENCY SERVICE LAYER
# =================================================================

class EmergencyService:
    """Handles high-priority email notifications to emergency responders."""
    @staticmethod
    def trigger_sos(city, area, severity):
        if not Config.SENDER_EMAIL or not Config.EMERGENCY_EMAIL:
            return
        
        subject = f"🚨 URGENT: {severity} BAD AIR QUALITY DETECTED IN {area.upper()}, {city.upper()}"
        body = f"""
        EMERGENCY ALERT: BAD AIR QUALITY DETECTED
        ------------------------------------------
        Location: {area}, {city}
        Severity Level: {severity}
        Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        This is an automated AI dispatch alert. Please send emergency responders to the coordinates logged in the system."""

        msg = MIMEMultipart()
        msg['From'], msg['To'], msg['Subject'] = Config.SENDER_EMAIL, Config.EMERGENCY_EMAIL, subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            # Fix: Use 587 for standard STARTTLS connection
            with smtplib.SMTP("smtp.gmail.com", 587, timeout=60) as server:
                server.starttls()
                server.login(Config.SENDER_EMAIL, Config.SENDER_PASSWORD)
                server.send_message(msg)
            logger.info("SOS Alert dispatched successfully.")
        except Exception as e:
            logger.error(f"Failed to dispatch SOS: {e}")

class AQIDatabase:
    """Logs user-driven AQI predictions for historical tracking."""
    @staticmethod
    def save_report(data):
        try:
            # Use a context manager for the connection
            with mysql.connector.connect(**Config.DB_CONFIG) as conn:
                with conn.cursor() as cursor:
                    query = """INSERT INTO aqi_history 
                               (city, area, latitude, longitude, pm25, pm10, no2, co, so2, o3, predicted_aqi, health_status) 
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    cursor.execute(query, (data['city'], data['area'], data['latitude'], data['longitude'], data['pm25'], data['pm10'], data['no2'], 
                        data['co'], data['so2'], data['o3'], data['aqi'], data['status']))
                conn.commit()
            return True
        except Exception as e:
            st.error(f"Database Error: {e}")
            return False

# =================================================================
# 3. ML MODEL & LOGIC LAYER
# =================================================================
@st.cache_resource
def load_aqi_model():
    """Loads the pre-trained Pickle model."""
    try:
        with open(Config.MODEL_PATH, 'rb') as file:
            model = joblib.load(file)
        return model
    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        return None

def get_health_status(aqi):
    """Categorizes AQI based on standard environmental scales."""
    if aqi <= 50: return "Good", "🟢"
    elif aqi <= 100: return "Moderate", "🟡"
    elif aqi <= 150: return "Unhealthy for Sensitive Groups", "🟠"
    elif aqi <= 200: return "Unhealthy", "🔴"
    elif aqi <= 300: return "Very Unhealthy", "🟣"
    else: return "Hazardous", "🟤"

# =================================================================
# 4. STREAMLIT UI
# =================================================================
def main():
    st.set_page_config(page_title="PureAir AI", layout="wide", page_icon="🍃")
    st.title("🍃 Smart City: AI-Powered Air Quality Predictor")
    st.markdown("---")

    

    CITY_DATA = {
        "Chennai": {"Anna Nagar": (13.08, 80.21), "T Nagar": (13.04, 80.23)},
        "Mumbai": {"Bandra": (19.05, 72.82), "Andheri": (19.11, 72.86)}
    }
    
    city = st.sidebar.selectbox("Select City", list(CITY_DATA.keys()))
    area = st.sidebar.selectbox("Select Area", list(CITY_DATA[city].keys()))
    lat, lon = CITY_DATA[city][area]

    # Load the Pickle Model
    model = load_aqi_model()
    
    col_input, col_output = st.columns([1, 1], gap="large")

    with col_input:
        st.subheader("📊 Enter Pollutant Concentrations (µg/m³)")

        PM25 = st.number_input("PM2.5", 0.0, 1000.0, 45.0)
        PM10 = st.number_input("PM10", 0.0, 1000.0, 85.0)
        NO2 = st.number_input("NO2 (Nitrogen Dioxide)", 0.0, 500.0, 28.0)
        CO = st.slider("CO (Carbon Monoxide)", 0.0, 50.0, 1.1)
        SO2 = st.slider("SO2 (Sulfur Dioxide)", 0.0, 200.0, 14.0)
        O3 = st.slider("O3 (Ozone)", 0.0, 300.0, 35.0)

    predict_btn = st.button("🚀 Predict Air Quality", width="stretch", type="primary")

    with col_output:
        st.subheader("🏁 Prediction Result")
        
        if predict_btn:
            if model is not None:
                with st.spinner("Model performing inference..."):
                    # 1. Prepare input array for the model
                    # Order must match the features used during training
                    input_data = np.array([[PM25, PM10, NO2, CO, SO2, O3]])
                    
                    # 2. Model Inference
                    try:
                        prediction = model.predict(input_data)
                        aqi_val = float(prediction[0])
                        
                        status, icon = get_health_status(aqi_val)
                        
                        # 3. Display Results
                        st.metric(label="Predicted AQI", value=round(aqi_val, 2))
                        st.markdown(f"### Status: {icon} {status}")
                        
                        if aqi_val > 100:
                            st.warning("⚠️ High pollution levels. Outdoor exertion should be limited.")
                        else:
                            st.success("✅ Air quality is safe for most individuals.")
                        
                    except Exception as e:
                        st.error(f"Prediction Error: {e}")
                 # 4. Save to Database
                if "Good" not in status or "Moderate" not in status:
                    AQIDatabase.save_report({
                    "city": city, "area": area, "latitude": lat, "longitude": lon, 
                    "pm25": PM25, "pm10": PM10, "no2": NO2, "co": CO, "so2": SO2, "o3": O3,
                    "aqi": aqi_val, "status": status
                    })
                    st.toast("Result logged to database!", icon="💾")
                    
                    EmergencyService.trigger_sos(city, area, status)
                    st.toast("Emergency services notified!",icon="⚠️")
            else:
                st.error("Model not found. Please check the MODEL_PATH in Config.")
        else:
            st.info("Input local pollutant data to calculate the current AQI.")

    # ================= FOOTER =================
    st.divider()
    st.markdown(
        "<p style='text-align: center; color: grey;'>© Selvakumaran Muthusamy | Air Quality Detection Page</p>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
    