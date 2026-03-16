from .llm_client import llm

def classify_intent(question: str) -> str:
    """
    Uses the LLM to determine which database table to query based on user input.
    """
    system_instruction = "You are an intent classifier for a Smart City system. Return ONLY the category word."
    
    prompt = f"""
    Classify this query into EXACTLY ONE:
    - traffic
    - accident
    - air_quality
    - crowd
    - road_damage
    - citizen_complaints

    User Question: {question}
    Category:"""

    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": prompt}
    ]

    response = llm.ask(messages)

    if not response or "error" in response.lower():
        return "unknown"

    # Clean the response to ensure it's just the lowercase word
    return response.strip().lower()
