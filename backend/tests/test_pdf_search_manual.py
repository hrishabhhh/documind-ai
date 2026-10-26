from app.services.ingestion_service import IngestionService
from app.services.search_service import SearchService

ingestion_service = IngestionService()
search_service = SearchService()

chunks = ingestion_service.ingest_document("data/sample.pdf")

search_service.load_chunks(chunks)

query = "What to do on thesday?"

results = search_service.search(query, top_k=3)

print(f"\nQuery: {query}")
print(f"Total Indexed Chunks: {len(chunks)}")

for index, result in enumerate(results, start=1):
    print(f"\nResult {index}")
    print(f"Page: {result['page_number']}")
    print(f"Similarity: {result['score']:.4f}")
    print(f"Text: {result['text'][:300]}")
    print(f"Chunk ID: {result['chunk_id']}" )

for chunk in chunks[22:25]:
    print(f"\nChunk ID: {chunk['chunk_id']}")
    print(f"Page: {chunk['page_number']}")
    print(f"Text: {chunk['text'][:250]}")
