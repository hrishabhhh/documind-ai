from app.services.ingestion_service import IngestionService
from app.services.search_service import SearchService

ingestion_service = IngestionService()
search_service = SearchService()

chunks = ingestion_service.ingest_document("data/sample.pdf")

search_service.load_chunks(chunks)

query = "What to do on thesday?"

results = search_service.search(query, top_k=3)

# print(f"\nQuery: {query}")
# print(f"Total Indexed Chunks: {len(chunks)}")

# for index, result in enumerate(results, start=1):
#     print(f"\nResult {index}")
#     print(f"Page: {result['page_number']}")
#     print(f"Similarity: {result['score']:.4f}")
#     print(f"Text: {result['text'][:300]}")
#     print(f"Chunk ID: {result['chunk_id']}" )

# for chunk in chunks[22:25]:
#     print(f"\nChunk ID: {chunk['chunk_id']}")
#     print(f"Page: {chunk['page_number']}")
#     print(f"Text: {chunk['text'][:250]}")

print("\nOriginal search results:")

for result in results:
    print(
        f"Chunk {result['chunk_id']} | "
        f"Page {result['page_number']}"
    )

expanded = search_service.expand_results(results, window=1)

print("\nExpanded results count:", len(expanded))

for chunk in expanded:
    print(
        f"Chunk {chunk['chunk_id']} | "
        f"Page {chunk['page_number']}"
    )