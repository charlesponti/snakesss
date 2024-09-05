import os
from typing import Annotated, Optional

from openai import AsyncOpenAI, OpenAI
from langchain_openai import ChatOpenAI
from pydantic import StringConstraints
from pydantic.v1.types import SecretStr

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", None)

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set")


openai_client = OpenAI(api_key=OPENAI_API_KEY)
openai_async_client = AsyncOpenAI(api_key=OPENAI_API_KEY)
openai_chat = ChatOpenAI(model="gpt-4o", api_key=SecretStr(OPENAI_API_KEY))


def get_openai_embedding(text):
    response = openai_client.embeddings.create(model="text-similarity-embeddings-v1", input=text)

    embeddings = response.data[0].embedding

    return embeddings


async def get_openai_chat_completion(
    system_message,
    user_message,
    model: Annotated[Optional[str], StringConstraints(pattern=r"^gpt-*$")] = None,
):
    response = openai_client.chat.completions.create(
        model=model or "gpt-4o",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
    )

    return response.choices[0].message.content
