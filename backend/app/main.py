from fastapi import FastAPI

app = FastAPI(
    title="DocuMind AI",
    description="Production-style RAG application",
    version="0.1.0"
)


@app.get("/")
def root():
    return {"message": "DocuMind AI API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}