from app.services.document_service import DocumentService

service = DocumentService()

text = "ABCDEFGHIJKLM"

chunks = service.chunk_text(
    text,
    chunk_size=5,
    overlap=2
)

for index, chunk in enumerate(chunks, start=1):
    print(f"Chunk {index}: {chunk}")