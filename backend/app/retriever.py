from langchain_chroma import Chroma

from azure_client import get_embeddings_model


def get_retriever():
    embeddings = get_embeddings_model()

    vector_store = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )

    return vector_store.as_retriever(search_kwargs={"k": 3})


if __name__ == "__main__":
    retriever = get_retriever()

    question = "Can employees store customer SIN numbers in any system?"

    docs = retriever.invoke(question)

    print(f"Retrieved {len(docs)} documents")

    for i, doc in enumerate(docs):
        print("\n" + "=" * 60)
        print(f"Result {i + 1}")
        print(f"Source: {doc.metadata.get('source')}")
        print(doc.page_content[:500])