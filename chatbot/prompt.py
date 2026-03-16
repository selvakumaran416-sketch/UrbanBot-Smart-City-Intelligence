# chatbot/prompt.py

def build_prompt(question: str, context: str) -> list:
    """
    Constructs the message list for the LLM using the UrbanBot persona.
    """
    system_content = (
        "You are UrbanBot, a Smart City AI Assistant.\n"
        "Your Name is UrbanGuard, a Smart City AI Assistant.\n"
        "1. Answer ONLY using the provided DATABASE RESULTS.\n"
        "2. If results are empty or irrelevant, say 'No data available.'\n"
        "3. Provide a brief summary and one actionable recommendation for city officials."
    )

    user_content = f"""
    DATABASE RESULTS:
    {context}

    USER QUESTION:
    {question}
    
    UrbanBot Response:"""

    return [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content}
    ]