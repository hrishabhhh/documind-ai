from app.services.document_service import DocumentService

service = DocumentService()

pages = service.extract_text("data/sample.pdf")

print("Total pages with text: ", len(pages))\

for page in pages:
    print("\nPage:", page["page_number"])
    print("Text:",page['text'][:300])