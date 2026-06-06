from pathlib import Path

from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from azure_client import get_embeddings_model


DOCS_DIR = Path("../data/sample/policies")
CHROMA_DIR = "chroma_db"


def load_documents():
    documents = []

    for file_path in DOCS_DIR.glob("*.md"):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        documents.append(
            Document(
                page_content=content,
                metadata={"source": file_path.name}
            )
        )

    return documents


def build_vector_store():
    docs = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(docs)

    embeddings = get_embeddings_model()

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )

    print(f"Documents: {len(docs)}")
    print(f"Chunks: {len(chunks)}")
    print("Chroma vector store created successfully")


if __name__ == "__main__":
    build_vector_store()