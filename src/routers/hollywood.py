import json
from typing import Annotated
from lib.clients.openai import openai_client
from lib.file_service import FileRepository
from fastapi import APIRouter, Form

router = APIRouter(
    prefix="/api/hollywood",
    tags=["hollywood"],
)

file_repository = FileRepository()


@router.post("/candidate_email_parser")
async def candidate_email_parser(message: Annotated[str, Form()]):
    system_message = file_repository.get_file_contents(
        "./lib/prompts/candidate_email_parser.txt"
    )
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        # model="gpt-4o",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": message},
        ],
        temperature=0.0,
        response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content

    if not content:
        return ""

    try:
        content = json.loads(content)
    except json.JSONDecodeError as e:
        return {"error": "Invalid JSON", "content": content}

    if content:
        candidates = content.get("candidates")
        candidates_len = len(candidates)

        if not candidates:
            return {"error": "No candidates found"}

        return {"count": candidates_len, "candidates": candidates}
