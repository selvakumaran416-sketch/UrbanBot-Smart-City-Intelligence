from .sql_agent import run_query
from .llm_client import llm
from .prompt import build_prompt
from .intent_classifier import classify_intent

def format_rows(rows):
    if isinstance(rows, str): return rows # Handle error strings
    return "\n".join([", ".join(map(str, row)) for row in rows])

def chatbot_response(user_query: str):
    # Pro Tip: Use the LLM Intent Classifier first for better accuracy
    intent = classify_intent(user_query)
    
    queries = {
        "traffic": "SELECT city, severity, COUNT(*) FROM traffic_reports GROUP BY city, severity",
        "accident": "SELECT city, severity, COUNT(*) FROM accident_reports GROUP BY city, severity",
        "air_quality": "SELECT city, pm25, pm10, health_status FROM aqi_history ORDER BY id DESC LIMIT 5",
        "crowd": "SELECT city, area, AVG(people_count) FROM crowd_reports GROUP BY city, area",
        "road_damage": "SELECT city, area, severity FROM road_damage_reports LIMIT 10",
        "citizen_complaints": "SELECT citizen_name, complaint_type, sentiment FROM citizen_complaints LIMIT 10"
    }

    sql = queries.get(intent)
    
    if not sql:
        return "I can help with Traffic, Accidents, AQI, Crowds, Road Damage, and Complaints. What's on your mind?"

    data = run_query(sql)
    
    if not data or isinstance(data, str) or len(data) == 0:
        return "No recent data available in the system for your request."

    context = format_rows(data)
    prompt = build_prompt(user_query, context)
    
    return llm.ask(prompt)
