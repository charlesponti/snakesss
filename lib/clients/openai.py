from os import getenv
from openai import OpenAI

OPENAI_API_KEY = getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set")

client = OpenAI(api_key=OPENAI_API_KEY)


def get_open_api_embedding(text):
    response = client.embeddings.create(
        model="text-similarity-embeddings-v1", input=text
    )

    embeddings = response.data[0].embedding

    return embeddings
