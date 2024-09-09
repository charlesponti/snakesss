from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

llama_chat = ChatOllama(
    model="llama3.1",
    temperature=0,
    base_url="http://host.docker.internal:11434",
)

lmstudio_chat = ChatOpenAI(
    temperature=0.5,
    base_url="http://host.docker.internal:1234/v1",
    api_key="lmstudio"
)
