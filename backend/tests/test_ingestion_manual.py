from app.services.ingestion_service import IngestionService

service = IngestionService()

results = service.ingest_document("data/sample.pdf")

print("Total chunks:", len(results))

for chunk in  results[:3]:
    print("\nPage:", chunk["page_number"])
    print("Chunk:", chunk["chunk_index"])
    print("Text:", chunk["text"][:100])
    print("Embedding dimensions:", len(chunk["embedding"]))