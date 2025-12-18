from fastapi import FastAPI
from ai_service.rag_pipeline import run_rag

app = FastAPI()

@app.get("/ask")
def ask_ai(q: str):
    return {"response": run_rag(q)}

