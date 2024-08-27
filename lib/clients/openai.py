from os import getenv
from openai import OpenAI

OPENAI_API_KEY = getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set")

client = OpenAI(api_key=OPENAI_API_KEY)


def get_openai_embedding(text):
    response = client.embeddings.create(
        model="text-similarity-embeddings-v1", input=text
    )

    embeddings = response.data[0].embedding

    return embeddings


async def get_openai_chat_completion(system_message, user_message):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
    )

    return response.choices[0].message.content
