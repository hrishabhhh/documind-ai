from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService


class IngestionService:
    def __init__(self):
        self.document_service = DocumentService()
        self.embedding_service = EmbeddingService()
    
    def ingest_document(self, file_path: str):
        chunks = self.document_service.process_document(file_path)

        for chunk in chunks:
            chunk["embedding"] = self.embedding_service.generate_embedding(
                chunk["text"]
            )
        return chunks