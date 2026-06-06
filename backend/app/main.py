from fastapi import FastAPI
from pydantic import BaseModel

from app.rag import ask_compliance_copilot


app = FastAPI(
    title="Enterprise AI Compliance Copilot",
    version="0.1.0"
)


class AskRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {
        "message": "Enterprise AI Compliance Copilot API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/ask")
def ask(request: AskRequest):
    result = ask_compliance_copilot(request.question)

    return {
        "question": request.question,
        "answer": result["answer"],
        "citations": result["citations"]
    }