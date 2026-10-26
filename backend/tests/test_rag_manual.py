from app.services.ingestion_service import IngestionService
from app.services.search_service import SearchService
from app.services.gemini_service import GeminiService
from app.services.rag_service import RAGService

ingestion_service = IngestionService()
search_service = SearchService()
gemini_service = GeminiService()

chunks = ingestion_service.ingest_document("data/sample.pdf")
search_service.load_chunks(chunks)

rag_service = RAGService(search_service,gemini_service)
results = rag_service.ask("What should I do on Tuesday?")

print(results[:1000])

# print("Retrieved chunks:", len(results))
# print("Top page:", results[0]["page_number"])