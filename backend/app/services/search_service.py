import numpy as np

from app.services.embedding_service import EmbeddingService

class SearchService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.chunks = []
        self.chunk_embeddings = None

        # self.documents = [
        #     "FastAPI is a Python framework for building REST APIs.",
        #     "React is used to build interactive user interfaces.",
        #     "PostgreSQL is a relational database.",
        #     "Docker is used to containerize applications.",
        #     "Python is widely used for backend development."
        # ]
        # self.document_embeddings = np.array([
        #     self.embedding_service.generate_embedding(doc)
        #     for doc in self.documents
        # ])

    def load_chunks(self, chunks):
        self.chunks = chunks
        self.chunk_embeddings = np.array([
            chunk["embedding"]
            for chunk in chunks
        ])

    def search(self,query:str,top_k: int = 3):
        
        if not self.chunks:
            return[]

        query_embedding = np.array(
            self.embedding_service.generate_embedding(query)
        )

        scores = np.dot(
            self.chunk_embeddings,
            query_embedding
        )

        top_indices = np.argsort(scores)[::-1][:top_k]
        results = []

        for index in top_indices:
            chunk=self.chunks[index]
            results.append({
                "chunk_id": chunk["chunk_id"],
                "text": chunk["text"],
                "page_number": chunk["page_number"],
                "score": float(scores[index]),
                "section": chunk.get("section")
            })
            
        return results


    def expand_results(self, results, window: int = 1):
        expanded = []
        seen_ids = set()

        for result in results:
            chunk_id = result['chunk_id']
            source_page = result['page_number']

            start = max(0, chunk_id - window)
            end = min(len(self.chunks), chunk_id + window + 1)

            for index in range(start,end):
                chunk = self.chunks[index]

                if chunk['page_number'] != source_page:
                    continue
                if chunk['chunk_id'] in seen_ids:
                    continue

                seen_ids.add(chunk['chunk_id'])
                expanded.append(chunk)
        
        return sorted(expanded, key=lambda chunk: chunk['chunk_id'])

    def get_chunks_by_section(self, section: str):
        matching_chunks = []

        for chunk in self.chunks:
            if chunk.get("section") == section:
                matching_chunks.append(chunk)
        return matching_chunks
