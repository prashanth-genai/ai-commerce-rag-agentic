from fastapi import FastAPI
from agent_service.agent_graph import agent_executor

app = FastAPI()

@app.post("/chat")
def chat(payload: dict):
    return agent_executor.invoke(payload)

