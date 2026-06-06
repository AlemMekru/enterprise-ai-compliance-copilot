from langchain_chroma import Chroma

from azure_client import get_chat_model, get_embeddings_model


def get_relevant_docs(question):
    embeddings = get_embeddings_model()

    vector_store = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )

    return vector_store.similarity_search(question, k=3)


def ask_compliance_copilot(question):
    docs = get_relevant_docs(question)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
You are an Enterprise AI Compliance Copilot.

Answer the user's question using ONLY the provided context.

If the answer cannot be found in the context, say:
"I could not find that information in the provided compliance documents."

Context:
{context}

Question:
{question}
"""

    llm = get_chat_model()

    response = llm.invoke(prompt)

    citations = [
        doc.metadata.get("source")
        for doc in docs
    ]

    return {
        "answer": response.content,
        "citations": list(set(citations))
    }


if __name__ == "__main__":
    result = ask_compliance_copilot(
        "Can employees store customer SIN numbers in any system?"
    )

    print("\nANSWER\n")
    print(result["answer"])

    print("\nCITATIONS\n")
    print(result["citations"])