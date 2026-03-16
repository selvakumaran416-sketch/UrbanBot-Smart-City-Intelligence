import streamlit as st
import mysql.connector
from datetime import datetime
import os
from dotenv import load_dotenv
from textblob import TextBlob
import time

# =================================================================
# 1. CONFIGURATION & DATABASE
# =================================================================
load_dotenv()

class Config:
    """System configuration for sentiment tracking."""
    # Using .get() to prevent NoneType errors if .env is missing
    DB_CONFIG = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": os.getenv("DB_PORT", "3306"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME")
    }

class SentimentDatabase:
    """Logs customer feedback for business intelligence."""
    @staticmethod
    def save_review(citizen_name, complaint_text, complaint_type, sentiment, polarity):
        # Check if DB credentials exist before attempting connection
        if not Config.DB_CONFIG["user"] or not Config.DB_CONFIG["database"]:
            st.warning("⚠️ Database credentials missing. Logging to session state instead.")
            return False

        try:
            with mysql.connector.connect(**Config.DB_CONFIG) as conn:
                with conn.cursor() as cursor:
                    query = """INSERT INTO citizen_complaints 
                               (citizen_name, complaint_text, complaint_type, sentiment, polarity_score) 
                               VALUES (%s, %s, %s, %s, %s)"""
                    cursor.execute(query, (citizen_name, complaint_text, complaint_type, sentiment, polarity))
                conn.commit()
            return True
        except Exception as e:
            st.error(f"Database Error: {e}")
            return False

# =================================================================
# 2. SENTIMENT LOGIC LAYER
# =================================================================
def analyze_sentiment(text):
    """
    Analyzes text and returns sentiment category and polarity score.
    Polarity is between -1 (Negative) and 1 (Positive).
    """
    analysis = TextBlob(text)
    score = analysis.sentiment.polarity
    
    if score > 0.1:
        return "Positive", "😊", score
    elif score < -0.1:
        return "Negative", "😡", score
    else:
        return "Neutral", "😐", score

# =================================================================
# 3. STREAMLIT UI
# =================================================================
def main():
    st.set_page_config(page_title="Smart City Citizen Complaints Platform", layout="wide", page_icon="🤝")
    st.title("🚨 Smart City Citizen Complaints System")
    st.caption("Submit your complaints or ideas for a better Smart City")
    st.markdown("---")

    # Initialize session state for history if not exists
    if "submissions" not in st.session_state:
        st.session_state.submissions = []

    col_input, col_output = st.columns([1, 1], gap="large")

    with col_input:
        st.subheader("📝 Submit Your Complaint or Suggestion")

        citizen_name = st.text_input("Your Name (Optional)", placeholder="Anonymous")
        complaint_text = st.text_area(
            "Enter Your Complaint or Suggestion", 
            placeholder="Describe your issue or idea here...",
            height=200
        )
        complaint_type = st.selectbox(
            "Select Type of Complaint",
            options=[
                "Accident or Incident", 
                "Traffic Congestion", 
                "Crowd or Congestion", 
                "Road Damage", 
                "Air Quality or Pollution", 
                "Other (Specify)"
            ]
        )
        
        analyze_btn = st.button("🚀 Analyze Sentiment", use_container_width=True, type="primary")

    with col_output:
        st.subheader("📊 Analysis Result")

        if analyze_btn and complaint_text:
            with st.spinner("Processing text..."):
                sentiment, emoji, score = analyze_sentiment(complaint_text)
                
                # Display Results
                st.markdown(f"## Result: {emoji} {sentiment}")
                
                # Progress bar to show intensity
                # Normalizing -1 to 1 into 0.0 to 1.0 for the progress bar
                normalized_score = (score + 1) / 2
                st.write(f"**Sentiment Intensity (Polarity): {score:.2f}**")
                st.progress(normalized_score)
                
                # Business Insight
                if sentiment == "Negative":
                    st.error("⚠️ This complaint requires immediate attention from the authorities.")
                elif sentiment == "Positive":
                    st.success("✅ Your feedback is valuable for improving our city!")
                else:
                    st.info("ℹ️ This feedback is recorded for general city maintenance.")
                
                # Save to Database
                success = SentimentDatabase.save_review(
                    citizen_name or "Anonymous",
                    complaint_text, 
                    complaint_type, 
                    sentiment, 
                    score
                )
                
                # Always save to session state for immediate UI update
                st.session_state.submissions.append({
                    "name": citizen_name or "Anonymous",
                    "type": complaint_type,
                    "sentiment": sentiment,
                    "score": score,
                    "time": datetime.now().strftime("%H:%M:%S")
                })
                
                if success:
                    st.toast("Logged to Database!", icon="💾")
        
        elif analyze_btn and not complaint_text:
            st.warning("Please enter a complaint or idea before analyzing.")
        else:
            st.info("Awaiting input for analysis.")

    # Complainant Timeline Display
    st.markdown("---")
    st.subheader("👥 Recent Submissions (Current Session)")

    if st.session_state.submissions:
        for sub in reversed(st.session_state.submissions):
            st.write(f"**{sub['name']}** ({sub['time']}) - *{sub['type']}*")
            st.caption(f"Sentiment: {sub['sentiment']} (Score: {sub['score']:.2f})")
    else:
        st.write("No submissions yet in this session.")

    # ================= FOOTER =================
    st.divider()
    st.markdown(
        "<p style='text-align: center; color: grey;'>© Selvakumaran Muthusamy | Citizen Complaint Page</p>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()