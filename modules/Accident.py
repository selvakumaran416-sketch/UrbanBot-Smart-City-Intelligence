import os
import cv2
import logging
import smtplib
import mysql.connector
import pandas as pd
import streamlit as st
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ultralytics import YOLO
from dotenv import load_dotenv

# =================================================================
# 1. CONFIGURATION & EMERGENCY SERVICES
# =================================================================
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Config:
    """System-wide configuration for accident response."""
    UPLOAD_DIR = "uploads/accidents"
    # Replace with your actual accident detection model path
    MODEL_PATH = "C:/Users/Selva.M/Downloads/data_science/final_project/models/accident_best.pt"
    
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

os.makedirs(Config.UPLOAD_DIR, exist_ok=True)

# =================================================================
# 2. EMERGENCY SERVICE LAYER
# =================================================================
class EmergencyService:
    """Handles high-priority email notifications to emergency responders."""
    @staticmethod
    def trigger_sos(city, area, severity):
        if not Config.SENDER_EMAIL or not Config.EMERGENCY_EMAIL:
            return

        subject = f"🚨 URGENT: {severity} ACCIDENT DETECTED IN {area.upper()}, {city.upper()}"
        body = f"""
        EMERGENCY ALERT: VEHICLE ACCIDENT DETECTED
        ------------------------------------------
        Location: {area}, {city}
        Severity Level: {severity}
        Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        This is an automated AI dispatch alert. Please send emergency responders to the coordinates logged in the system.
        """
        
        msg = MIMEMultipart()
        msg['From'], msg['To'], msg['Subject'] = Config.SENDER_EMAIL, Config.EMERGENCY_EMAIL, subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
                server.starttls()
                server.login(Config.SENDER_EMAIL, Config.SENDER_PASSWORD)
                server.send_message(msg)
            logger.info("SOS Alert dispatched successfully.")
        except Exception as e:
            logger.error(f"Failed to dispatch SOS: {e}")

class DatabaseManager:
    """Logs accident incidents for forensic analysis."""
    @staticmethod
    def save_report(data):
        try:
            with mysql.connector.connect(**Config.DB_CONFIG) as conn:
                with conn.cursor() as cursor:
                    query = """INSERT INTO accident_reports 
                               (city, area, latitude, longitude, accident_count, severity, image_name) 
                               VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                    cursor.execute(query, (data['city'], data['area'], data['lat'], data['lon'], 
                                     data['count'], data['severity'], data['img']))
                conn.commit()
            return True
        except Exception as e:
            logger.error(f"DB Error: {e}")
            return False

# =================================================================
# 3. AI LOGIC & STREAMLIT UI
# =================================================================
@st.cache_resource
def get_accident_model():
    return YOLO(Config.MODEL_PATH)

def determine_severity(detections):
    count=len(detections)
    if count >= 4: return "CRITICAL"
    if count >= 3: return "HEAVY"
    if count >= 2: return "MODERATE"
    return "LOW"


# =================================================================
# 4. STREAMLIT UI & MULTI-INPUT HANDLING
# =================================================================

def main():
    st.set_page_config(page_title="SafeCity: Accident AI", layout="wide", page_icon="🚑")
    st.title("🚑 Smart City: Real-Time Accident Detection System")
    st.markdown("---")

    # Shared Location Data
    CITY_DATA = {
        "Chennai": {"Guindy High Road": (13.01, 80.22), "OMR Junction": (12.97, 80.24)},
        "Mumbai": {"Marine Drive": (18.94, 72.82), "Sion Flyover": (19.04, 72.86)}
    }
    # Sidebar Setup
    st.sidebar.header("🕹️ Monitoring Setup")
    mode = st.sidebar.radio("Input Source", ["Static Image","Live Accident Feed"])
    city = st.sidebar.selectbox("Select City", list(CITY_DATA.keys()))
    area = st.sidebar.selectbox("Select Area", list(CITY_DATA[city].keys()))
    lat, lon = CITY_DATA[city][area]

    model = get_accident_model()
    col_input, col_output = st.columns([1, 1.2], gap="medium")

    # --- MODE: STATIC IMAGE ---
    if mode == "Static Image":
        with col_input:
            uploaded_file = st.file_uploader("Upload Image", type=['jpg','png','jpeg'])
            if uploaded_file and st.button("🚀 Analyze Image", width="stretch"):
                img_path = os.path.join(Config.UPLOAD_DIR, f"IMG_{datetime.now().strftime('%H%M%S')}.jpg")
                with open(img_path, "wb") as f: f.write(uploaded_file.getbuffer())
                
                img = cv2.imread(img_path)
                results = model.predict(img, verbose=False)
                detections = [model.names[int(c)] for c in results[0].boxes.cls]
                severity = determine_severity(detections)
                
                with col_output:
                    st.image(results[0].plot(), channels="BGR", caption="Static Analysis")
                    st.metric("Defects Found", len(detections))
                    st.metric("Severity", severity)

                if "CRITICAL" in severity or "HEAVY" in severity or "MODERATE" in severity:
                    DatabaseManager.save_report({
                    "city": city, "area": area, "lat": lat, "lon": lon,"count": len(detections),
                    "severity": severity, "img": os.path.basename(img_path)
                    })
                    st.toast("Report saved to database!", icon="✅")
                            
                    EmergencyService.trigger_sos(city, area, severity)
                    st.toast("Emergency services notified!", icon="🚑")

    # --- LIVE TRAFFIC FEED ---
    else:
        with col_input:
            st.info("Monitoring CCTV Feed...")
            run = st.toggle("Activate Live Monitoring", value=False)
            
        if run:
            cap = cv2.VideoCapture(0) # Index 0 for local testing
            st_frame = col_output.empty()
            status_box = col_output.empty()
            metrics_placeholder = col_output.empty()
            
            # Prevent spamming alerts: only send alert once every 60 seconds for the same event
            if 'last_alert_time' not in st.session_state:
                st.session_state.last_alert_time = datetime.now()

            while run:
                ret, frame = cap.read()
                if not ret: break
                
                results = model.predict(frame, conf=0.5, verbose=False)
                detections = [model.names[int(c)] for c in results[0].boxes.cls]
                severity = determine_severity(detections)

                annotated = results[0].plot()

                st_frame.image(annotated, channels="BGR", width="stretch")
                metrics_placeholder.markdown(f"**Current Status:** {severity} | **Defects:** {len(detections)}")
                if "CRITICAL" in severity or "HEAVY" in severity  or "MODERATE" in severity:
                    status_box.error(f"🚨 Accident Detected at {area}!")
                    
                    # Logic: Auto-log and alert if 60 seconds have passed since last alert
                    current_time = datetime.now()
                    if (current_time - st.session_state.last_alert_time).total_seconds() > 60:
                        img_name = f"ALERT_{datetime.now().strftime('%H%M%S')}.jpg"
                        img_path = os.path.join(Config.UPLOAD_DIR, img_name)
                        cv2.imwrite(img_path, annotated)
                        
                        DatabaseManager.save_report({
                            "city": city, "area": area, "lat": lat, "lon": lon,"count": len(detections),
                            "severity": severity, "img": img_name
                        })
                        EmergencyService.trigger_sos(city, area, severity)
                        st.session_state.last_alert_time = current_time
                        st.toast("Emergency services notified!", icon="🚑")
                else:
                    status_box.success("✅ Traffic Flowing Normal")
            cap.release()

    # ================= FOOTER =================
    st.divider()
    st.markdown(
        "<p style='text-align: center; color: grey;'>© Selvakumaran Muthusamy | Accident Detection Page</p>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()


