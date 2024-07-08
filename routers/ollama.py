import json
from typing import Annotated, Optional
from fastapi import APIRouter, Form
import requests
from lib.repositories.file_repository import FileRepository

file_repository = FileRepository()

router = APIRouter(
    prefix="/api/ollama",
    tags=["ollama"],
)


@router.post("/candidate_email_parser")
def text_to_candidates(message: Annotated[str, Form()], model: Optional[str]):
    system_message = file_repository.get_file_contents(
        "lib/prompts/system_role_description.txt"
    )
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
