
from app.services.search_service import SearchService


search_service = SearchService()

query = "Which framework can I use to build backend APIs?"

results = search_service.search(query, top_k=3)

print(f"\nQuery: {query}")
print("\nTop 3 Relevant Documents:\n")

for index, result in enumerate(results, start=1):
    print(f"{index}. {result['document']}")
    print(f"   Similarity: {result['score']:.4f}\n")
