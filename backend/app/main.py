from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from pathlib import Path
import shutil
from app.document_processor import ingest_file
from app.rag import ask_compliance_copilot

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

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

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    allowed_extensions = [".pdf", ".txt", ".md", ".docx"]

    suffix = Path(file.filename).suffix.lower()

    if suffix not in allowed_extensions:
        return {
            "success": False,
            "message": f"Unsupported file type: {suffix}"
        }

    destination = UPLOAD_DIR / file.filename

    with open(destination, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ingestion_result = ingest_file(destination)

    return {
        "success": True,
        "filename": file.filename,
        "path": str(destination),
        "chunks_created": ingestion_result["chunks_created"]
    }

@app.post("/ask")
def ask(request: AskRequest):
    result = ask_compliance_copilot(request.question)

    return {
        "question": request.question,
        "answer": result["answer"],
        "citations": result["citations"]
    }