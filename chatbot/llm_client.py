import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY missing in .env")
        self.client = Groq(api_key=self.api_key)

    def ask(self, messages: list, model: str = "llama-3.1-8b-instant"):
        try:
            # Ensure messages is always a list of dicts
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.2,
                max_tokens=700
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"LLM Error: {str(e)}"

# Singleton instance for app-wide use
llm = LLMClient()
