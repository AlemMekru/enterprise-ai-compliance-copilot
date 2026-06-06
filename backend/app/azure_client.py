import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings

load_dotenv(Path(__file__).parent.parent / ".env")


def get_embeddings_model():
    return AzureOpenAIEmbeddings(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
        openai_api_version="2024-02-01",
    )


def get_chat_model():
    return AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
        openai_api_version="2024-12-01-preview"
    )


if __name__ == "__main__":
    embeddings = get_embeddings_model()
    vector = embeddings.embed_query("What is compliance?")

    print("Embedding test successful")
    print(f"Vector length: {len(vector)}")

    llm = get_chat_model()
    response = llm.invoke("In one sentence, what is compliance?")

    print("Chat test successful")
    print(response.content)