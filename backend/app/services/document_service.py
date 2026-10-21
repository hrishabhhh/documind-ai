import pymupdf

class DocumentService:
    def extract_text(self,file_path: str):
        pages=[]

        with pymupdf.open(file_path) as document:
            for page_number, page in enumerate(document, start=1):
                text = page.get_text("text")

                if text.strip():
                    pages.append({
                        "page_number": page_number,
                        "text": text
                    })

        return pages
            
