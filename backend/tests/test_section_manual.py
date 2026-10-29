from app.services.document_service import DocumentService

service = DocumentService()

# pages = service.extract_text("data/sample.pdf")
# for page in pages:
#     if page["page_number"] in [6,7]:
#         print(f"\n{'n' * 40}")
#         print(f"PAGE {page['page_number']}")
#         print(f"{'=' * 40}")
#         print(page["text"][:700])

# def find_document(service, day):
#         pages = service.extract_text("data/sample.pdf")

#         matching_pages = []

#         for page in pages: 
#             lines = page["text"].splitlines()
           
#             if not lines:
#                 continue
#             heading = lines[0].strip().lower()

#             if heading.startswith(f"{day} /"):
#                 matching_pages.append(page)

#         return matching_pages

# matching_pages = find_document(service, "wednesday")

# for page in matching_pages:
#     print(f"Page: {page['page_number']}")

#     lines = page["text"].splitlines()
#     print(lines[:5])

pages = service.extract_text("data/sample.pdf")

page_sections = service.detect_sections(pages)

print(page_sections)
