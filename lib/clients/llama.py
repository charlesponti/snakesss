from langchain.pydantic_v1 import SecretStr
from langchain_openai import ChatOpenAI

lmstudio_chat = ChatOpenAI(
    model="mlx-community/llama-3.2-3b-instruct:3",
    temperature=0.5,
    base_url="http://host.docker.internal:1234/v1",
    api_key=SecretStr("lmstudio"),
)
