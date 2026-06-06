from pathlib import Path

from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from app.azure_client import get_embeddings_model
from app.document_analyzer import analyze_document

CHROMA_DIR = "chroma_db"


def extract_text(file_path: Path) -> str:
    suffix = file_path.suffix.lower()

    if suffix in [".txt", ".md"]:
        return file_path.read_text(encoding="utf-8")

    if suffix == ".pdf":
        reader = PdfReader(str(file_path))
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return text

    raise ValueError(f"Unsupported file type: {suffix}")


def ingest_file(file_path: Path):
    text = extract_text(file_path)
    analysis = analyze_document(text)

    document = Document(
        page_content=text,
        metadata={"source": file_path.name}
    )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents([document])

    embeddings = get_embeddings_model()

    vector_store = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )

    vector_store.add_documents(chunks)

    return {
        "filename": file_path.name,
        "chunks_created": len(chunks),
        "analysis": analysis
    }