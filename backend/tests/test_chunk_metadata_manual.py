from app.services.document_service import DocumentService

service = DocumentService()

chunks = service.process_document("data/sample.pdf")

for chunk in chunks:

    if chunk["section"] == "tuesday":
        print(
            f"ID: {chunk['chunk_id']} | "
            f"Page: {chunk['page_number']} |"
            f"index {chunk['chunk_index']}"
        )