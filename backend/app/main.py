from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(title="KrishiAI+ API")

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "KrishiAI+ Backend is healthy"}

@app.get("/")
def read_root():
    return {"message": "Welcome to KrishiAI+ API"}
