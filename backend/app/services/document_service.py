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
            
    def chunk_text(self, text:str, chunk_size: int = 500, overlap: int = 100):
        if chunk_size <=0 or overlap < 0 or overlap >= chunk_size:
            raise ValueError("Invalid chunk size or overlap")

        chunks = []
        step = chunk_size - overlap

        for start in range(0, len(text), step):
            chunk = text[start:start + chunk_size]

            if chunk.strip():
                chunks.append(chunk)
            
            if start + chunk_size >= len(text):
                break

        return chunks

    def process_document(self, file_path:str):
        pages = self.extract_text(file_path)
        page_sections = self.detect_sections(pages)
      
        all_chunks = []

        for page in pages:
            chunks = self.chunk_text(page["text"])
            section = page_sections.get(page["page_number"])
            for index, chunk in enumerate(chunks):
                all_chunks.append({
                    "chunk_id": len(all_chunks),
                    "page_number": page["page_number"],
                    "chunk_index": index,
                    "section": section,
                    "text": chunk
                })
                
        return all_chunks

    def detect_sections(self, pages):

        days = ['monday','tuesday','wednesday','thursday','friday','saturday']

        page_sections = {}

        for page in pages:
            lines = page["text"].splitlines()

            if not lines:
                continue
            heading = lines[0].strip().lower()

            parts = heading.split(" /", 1)
            day = parts[0]

            if len(parts) == 2 and day in days:
                page_sections[page['page_number']] = day

            # for day in days:
            #     matching_pages = find_document(service, day)

            #     for page in matching_pages:
            #         page_sections[page['page_number']] = day

        return page_sections


        