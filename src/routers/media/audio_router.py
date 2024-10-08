import io

from fastapi import APIRouter, UploadFile

from lib.ai_models import audio_models
from lib.clients.groq_service import groq_client
from lib.clients.openai import openai_client

from src.routers.media.vision_router import vision_router

audio_router = APIRouter()
audio_router.include_router(vision_router, prefix="/vision")


@audio_router.post("/audio/transcribe")
def transcribe_audio(
    audio_file: UploadFile,
    model: str = "openai",
):
    """
    Transcribes audio using either OpenAI's whisper or Groq's Whisper API.
    NOTE : OPenAI's transcription is faster as Groq uses whisper large v3 model which is not required at the moment
    """
    file = audio_file.file.read()
    buffer = io.BytesIO(file)
    buffer.name = "audio.m4a"

    if model == "groq":
        transcription = groq_client.audio.transcriptions.create(
            file=buffer,
            model=audio_models[model],
            prompt="",
            response_format="json",
            language="en",
            temperature=0.0,
        )

    elif model == "openai":
        transcription = openai_client.audio.transcriptions.create(model=audio_models[model], file=buffer)

    else:
        return {"error": "Choose an appropriate transcription model"}

    return {"result": transcription.text}
