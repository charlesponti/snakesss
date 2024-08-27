import base64
import io
import requests

from fastapi import APIRouter, UploadFile

from lib.clients.openai import OPENAI_API_KEY
from src.services.images import ImageResolver

vision_router = APIRouter()


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


@vision_router.post("/images/embedding")
def image_embedding(image_file: UploadFile):
    """
    Extracts image embeddings using OpenAI's CLIP model
    """
    file = image_file.file.read()
    buffer = io.BytesIO(file)
    buffer.name = "image.jpg"

    embedding = ImageResolver.image_to_embedding(image_bytes=buffer)
    return {"embedding": embedding}

@vision_router.post("/vision")
async def vision(image: UploadFile):
    # Path to your image
    image_path = "path_to_your_image.jpg"

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What’s in this image?"},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        "max_tokens": 300,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )

    return response.json()
