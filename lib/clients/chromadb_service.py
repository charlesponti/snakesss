import os

import chromadb
from chromadb.api.models.Collection import Collection
from langchain_chroma import Chroma

from lib.clients.openai import openai_embedding_model

try:
    chroma_client = chromadb.HttpClient(
        host=os.getenv("CHROMA_HOST"),
        port=os.getenv("CHROMA_PORT")
    )
except Exception as e:
    print(f"Error connecting to chromadb: {e}")
    chroma_client = None


def get_image_collection() -> Collection | None:
    if chroma_client is None:
        return None
    return chroma_client.get_or_create_collection("images")

# Initialize ChromaDB
vector_db = Chroma(
    embedding_function=openai_embedding_model,
    persist_directory="./chroma_db",
    client=chroma_client
)
