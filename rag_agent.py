import os
import langchain

from langchain.text_splitter import RecursiveCharacterTextSplitter

LANGCHAIN_TRACING_V2 = os.environ.get("LANGCHAIN_TRACING_V2", None)
LANGCHAIN_API_KEY = os.environ.get("LANGCHAIN_API_KEY", None)
LANGCHAIN_ENDPOINT = os.environ.get("LANGCHAIN_ENDPOINT", None)
