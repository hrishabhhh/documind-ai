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

        all_chunks = []

        for page in pages:
            chunks = self.chunk_text(page["text"])

            for index, chunk in enumerate(chunks):
                all_chunks.append({
                    "chunk_id": len(all_chunks),
                    "page_number": page["page_number"],
                    "chunk_index": index,
                    "text": chunk
                })
                
        return all_chunks