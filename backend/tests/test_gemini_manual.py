import os 
from dotenv import load_dotenv
from google import genai
from app.services.gemini_service import GeminiService

# load_dotenv()

# api_key = os.getenv("GEMINI_API_KEY")

# if not api_key:
#     raise ValueError("GEMINI API key is missing")

# client = genai.Client(api_key=api_key)

# response = client.models.generate_content(
#     model="gemini-3.8-flash",
#     contents="Explain RAG in one sentence."
# )

# print(response.text)

service = GeminiService()

answer = service.generate_answer(
    "Explain semantic search in one sentence."
)

print(answer)

