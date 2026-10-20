import numpy as np

from app.services.embedding_service import EmbeddingService

class SearchService:
    def __init__(self):
        self.embedding_service = EmbeddingService()

        self.documents = [
            "FastAPI is a Python framework for building REST APIs.",
            "React is used to build interactive user interfaces.",
            "PostgreSQL is a relational database.",
            "Docker is used to containerize applications.",
            "Python is widely used for backend development."
        ]

        self.document_embeddings = np.array([
            self.embedding_service.generate_embedding(doc)
            for doc in self.documents
        ])

    def search(self,query:str,top_k: int = 3):
        query_embedding = np.array(
            self.embedding_service.generate_embedding(query)
        )

        scores = np.dot(
            self.document_embeddings,
            query_embedding
        )

        top_indices = np.argsort(scores)[::-1][:top_k]
        results = []

        for index in top_indices:
            results.append({
                "document": self.documents[index],
                "score": float(scores[index])
            })
        return results