import os
from dotenv import load_dotenv
from langchain_openai import AzureOpenAIEmbeddings

load_dotenv()

def get_embeddings_model():
    return AzureOpenAIEmbeddings(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
        openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    )


if __name__ == "__main__":
    embeddings = get_embeddings_model()

    text = "Employees must not store customer SIN numbers in unauthorized systems."
    vector = embeddings.embed_query(text)

    print("Embedding generated successfully")
    print(f"Vector length: {len(vector)}")
    print(f"First 5 values: {vector[:5]}")