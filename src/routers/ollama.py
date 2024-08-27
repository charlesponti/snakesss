import json
from typing import Annotated, Optional
from fastapi import APIRouter, Form
import requests
from lib.repositories.file_repository import FileRepository

file_repository = FileRepository()

ollama_router = APIRouter(
    prefix="/api/ollama",
    tags=["ollama"],
)


@ollama_router.post("/chat")
def chat(message: Annotated[str, Form()], model: Optional[str]):
    system_message = """
    You are an intelligent human being who is capable of conversing about any topic.
    """
    model = model if model else "llama3"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": message},
        ],
        "format": "json",
        "stream": False,
    }
    response = requests.post("http://localhost:11434/api/chat", json=payload)
    content = json.loads(response.json()["message"]["content"])
    return content
