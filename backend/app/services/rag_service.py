from app.services.search_service import SearchService
from app.services.gemini_service import GeminiService

class RAGService:
    def __init__(self, search_service: SearchService, gemini_service: GeminiService):
        self.search_service = search_service
        self.gemini_service = gemini_service

    def ask(self,question: str):
        result = self.search_service.search(query= question, top_k=3)
        return result
