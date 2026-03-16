import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_db_stats():
    """Fetch counts, all map coordinates, and latest AQI."""
    try:
        # Create SQLAlchemy URL object
        url_object = URL.create(
            "mysql+mysqlconnector",
            username=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=3306,
            database=os.getenv("DB_NAME")
        )

        engine = create_engine(url_object)
        with engine.connect() as conn:
            # 1. Fetch ALL Incidents (Removed limits to show all points on map)
            acc_df = pd.read_sql("SELECT latitude, longitude, 'Accident' as type FROM accident_reports", conn)
            tra_df = pd.read_sql("SELECT latitude, longitude, 'Traffic' as type FROM traffic_reports", conn)
            pot_df = pd.read_sql("SELECT latitude, longitude, 'Pothole' as type FROM road_damage_reports", conn)
            
            # Combine all records into one DataFrame for mapping
            map_df = pd.concat([acc_df, tra_df, pot_df], ignore_index=True)
            
            # Clean data: Remove rows where coordinates might be missing
            map_df = map_df.dropna(subset=['latitude', 'longitude'])

            # 2. Fetch Latest Air Quality
            try:
                # Fixed: Changed index key to 'predicted_aqi' to match your SELECT statement
                aqi_query = "SELECT predicted_aqi FROM aqi_history ORDER BY created_at DESC LIMIT 1"
                aqi_res = pd.read_sql(aqi_query, conn)
                aqi_val = aqi_res['predicted_aqi'][0] if not aqi_res.empty else 72
            except Exception as aqi_err:
                # Fallback if table doesn't exist yet
                aqi_val = 72 

            # 3. Summary counts for metrics
            acc_count, tra_count, pot_count = len(acc_df), len(tra_df), len(pot_df)

            chart_data = pd.DataFrame({
                "Module": ["Accidents", "Traffic", "Potholes"],
                "Incidents": [acc_count, tra_count, pot_count]
            })

        return acc_count, tra_count, pot_count, aqi_val, chart_data, map_df
        
    except Exception as e:
        st.error(f"Database Connection Error: {e}")
        return 0, 0, 0, 0, pd.DataFrame(), pd.DataFrame()

def main():
    # Set layout to wide to prevent map from being cramped
    st.set_page_config(page_title="Executive Dashboard", layout="wide")
    
    st.title("📊 Executive Command Dashboard")
    st.caption("Real-time Analytics from AWS Cloud Instance")

    # Unpack the returned database values
    acc, tra, pot, aqi, df, map_df = get_db_stats()

    # --- TOP ROW: KPI METRICS ---
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total Accidents", acc, delta="-5%")
    m2.metric("Traffic Alerts", tra, delta="High", delta_color="inverse")
    m3.metric("Road Damage", pot, delta="High", delta_color="inverse")
    m4.metric("System Uptime", "99.9%", delta="Stable")
    m5.metric("Avg AQI", aqi, delta="Real-time")

    st.divider()

    # --- SECOND ROW: VISUALIZATIONS ---
    left, right = st.columns([1, 1.5]) # Widened the map column

    with left:
        st.subheader("📈 Incident Distribution")
        if not df.empty:
            fig = px.bar(df, x="Module", y="Incidents", color="Module", 
                         color_discrete_map={"Accidents": "#EF553B", "Traffic": "#FECB52", "Potholes": "#00CC96"},
                         template="plotly_dark")
            st.plotly_chart(fig, width="stretch")
        else:
            st.warning("No incident data found.")

    with right:
        st.subheader("📍 Real-time Incident Map")
        if not map_df.empty:
            # Scatter Mapbox showing ALL points
            fig_map = px.scatter_mapbox(
                map_df, 
                lat="latitude", 
                lon="longitude", 
                color="type",
                hover_name="type",
                color_discrete_map={"Accident": "red", "Traffic": "orange", "Pothole": "yellow"},
                zoom=3, # Zoomed out slightly to ensure all points fit initially
                mapbox_style="carto-darkmatter",
                height=400
            )
            # This ensures the map expands to fill the column
            fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map, width="stretch")
        else:
            st.info("No location data available to map.")

    # ================= FOOTER =================
    st.divider()
    st.markdown(f"<p style='text-align: center; color: grey;'>© Selvakumaran Muthusamy | Project Dashboard</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
