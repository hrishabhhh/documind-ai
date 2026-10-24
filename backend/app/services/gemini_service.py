import os
from dotenv import load_dotenv
from google import genai

class GeminiService:
    def __init__(self):
        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI API KEY is missing")

        self.client = genai.Client(api_key=api_key)
    
    def generate_answer(self, prompt: str):
        response = self.client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )
        
        return response.text