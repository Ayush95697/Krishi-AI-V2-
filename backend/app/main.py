from fastapi import FastAPI

app = FastAPI(title="KrishiAI+ API")

@app.get("/")
def read_root():
    return {"message": "Welcome to KrishiAI+ API"}
