from .sql_agent import execute_query

def get_accident_insights():
    return execute_query("""
        SELECT city, area, severity, COUNT(*) as total_cases
        FROM accident_reports
        WHERE DATE(created_at) = CURDATE()
        GROUP BY city, area, severity
        ORDER BY total_cases DESC
    """)

def get_traffic_insights():
    return execute_query("""
        SELECT city, area, AVG(vehicle_count) as avg_vehicle, severity
        FROM traffic_reports
        WHERE DATE(created_at) = CURDATE()
        GROUP BY city, area, severity
        ORDER BY avg_vehicle DESC
    """)

def get_aqi_insights():
    return execute_query("""
        SELECT city, area, ROUND(AVG(predicted_aqi),2) as avg_aqi, health_status
        FROM aqi_history
        WHERE DATE(created_at) = CURDATE()
        GROUP BY city, area, health_status
        ORDER BY avg_aqi DESC
    """)

def get_citizen_complaints_insights(): 
    return execute_query("""
        SELECT citizen_name, sentiment, polarity_score
        FROM citizen_complaints
        WHERE DATE(created_at) = CURDATE()
        ORDER BY polarity_score DESC
    """)

def get_road_damage_insights():
    return execute_query("""
        SELECT city, area, severity, COUNT(*) as total_cases
        FROM road_damage_reports
        WHERE DATE(created_at) = CURDATE()
        GROUP BY city, area, severity
        ORDER BY total_cases DESC
    """)

def get_crowd_insights():
    return execute_query("""
        SELECT city, area, severity, COUNT(*) as total_cases
        FROM crowd_reports
        WHERE DATE(created_at) = CURDATE()
        GROUP BY city, area, severity
        ORDER BY total_cases DESC
    """)