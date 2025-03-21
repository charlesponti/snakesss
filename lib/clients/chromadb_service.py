import traceback

import chromadb
from chromadb.config import Settings
from langchain_chroma import Chroma

from conf import settings
from lib.clients.openai import openai_embeddings
from lib.logger import logger

chroma_client = None


if settings.ENVIRONMENT == "production" and not settings.CI:
    chroma_client = chromadb.HttpClient(
        host=settings.CHROMA_SERVER_HOST,
        settings=Settings(
            chroma_server_host=settings.CHROMA_SERVER_HOST,
            chroma_client_auth_provider=settings.CHROMA_SERVER_AUTH_PROVIDER,
            chroma_client_auth_credentials=settings.CHROMA_SERVER_AUTH_CREDENTIALS,
            chroma_auth_token_transport_header=settings.CHROMA_AUTH_TOKEN_TRANSPORT_HEADER,
        ),
    )
elif settings.ENVIRONMENT != "test" and not settings.CI and settings.CHROMA_SERVER_HTTP_PORT:
    chroma_client = chromadb.HttpClient(
        host=settings.CHROMA_SERVER_HOST,
        port=settings.CHROMA_SERVER_HTTP_PORT,
        settings=Settings(
            chroma_server_host=settings.CHROMA_SERVER_HOST,
            chroma_server_http_port=settings.CHROMA_SERVER_HTTP_PORT,
            chroma_client_auth_provider=settings.CHROMA_SERVER_AUTH_PROVIDER,
            chroma_client_auth_credentials=settings.CHROMA_SERVER_AUTH_CREDENTIALS,
            chroma_auth_token_transport_header=settings.CHROMA_AUTH_TOKEN_TRANSPORT_HEADER,
        ),
    )

if chroma_client:
    vector_store = Chroma(
        client=chroma_client,
        collection_name="focus",
        embedding_function=openai_embeddings,
    )
else:
    vector_store = Chroma(
        collection_name="focus",
        embedding_function=openai_embeddings,
        persist_directory=".chroma",
    )


def get_collection(name: str):
    if not chroma_client:
        return None

    return chroma_client.get_collection(name)


def clear_focus_items_from_vector_store():
    try:
        logger.info("Resetting Chroma vector store.")
        vector_store.reset_collection()
        logger.info("Reset Chroma vector store.")
    except Exception:
        traceback.print_exc()
        logger.error("Error resetting ChromaDB vector store")
