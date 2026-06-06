from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

DOCS_DIR = Path("../data/sample/policies")


def load_documents():
    documents = []

    for file_path in DOCS_DIR.glob("*.md"):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        documents.append({
            "source": file_path.name,
            "content": content
        })

    return documents


def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = []

    for doc in documents:
        split_texts = splitter.split_text(doc["content"])

        for index, text in enumerate(split_texts):
            chunks.append({
                "source": doc["source"],
                "chunk_index": index,
                "content": text
            })

    return chunks


if __name__ == "__main__":
    docs = load_documents()
    chunks = chunk_documents(docs)

    print(f"Loaded {len(docs)} documents")
    print(f"Created {len(chunks)} chunks")

    for chunk in chunks:
        print("-" * 50)
        print(f"Source: {chunk['source']}")
        print(f"Chunk: {chunk['chunk_index']}")
        print(chunk["content"][:300])