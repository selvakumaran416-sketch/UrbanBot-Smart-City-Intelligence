import streamlit as st

def main():
    st.title("🚀 UrbanGuard AI: The Future of Urban Safety")
    
    st.markdown("""
    ### 🎯 Project Vision
    UrbanGuard AI is an integrated ecosystem designed to automate city-wide monitoring. 
    By combining **Computer Vision**, **Predictive Modeling**, and **Cloud Computing**, 
    we reduce emergency response times and improve urban living standards.

    ### 🏗️ Integrated Modules
    """)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("#### 🚑 Accident Response")
        st.write("Real-time Accident & Pothole detection with automated SOS dispatch to emergency services.")
    with c2:
        st.success("#### 🍃 Air Quality")
        st.write("AQI prediction using ML to provide health advisories based on pollutant levels.")
    with c3:
        st.warning("#### 🚦 Traffic & Crowd")
        st.write("Dynamic congestion analysis to prevent gridlock and ensure public safety.")

    st.divider()

    # Section: Tech Stack
    st.markdown("#### 🛠️ Professional Tech Stack")

    st.code("""
    - Frontend: Streamlit (Python-based Web Framework)
    - AI/CV: Ultralytics YOLOv8, Scikit-Learn, Gemini 1.5 Flash
    - Database: Amazon RDS (MySQL)
    - Intelligence: TextBlob NLP & Scikit-Learn Regression
    - Infrastructure: Amazon EC2 (Ubuntu 24.04 LTS)
    - Communication: SMTP (Secure Email Dispatch)
    """, language="text")

    # ================= FOOTER =================
    st.divider()
    st.markdown(
        "<p style='text-align: center; color: grey;'>© Selvakumaran Muthusamy | Project Introduction Page</p>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
