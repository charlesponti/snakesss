import io

from fastapi import APIRouter, UploadFile

from lib.clients.openai import openai_client

from src.routers.media.vision_router import vision_router

audio_router = APIRouter()
audio_router.include_router(vision_router, prefix="/vision")


@audio_router.post("/audio/transcribe")
def transcribe_audio(
    audio_file: UploadFile,
):
    """Transcribes audio using OpenAI's Whisper API."""

    file = audio_file.file.read()
    buffer = io.BytesIO(file)
    buffer.name = "audio.m4a"

    transcription = openai_client.audio.transcriptions.create(model="whisper-1", file=buffer)

    return {"result": transcription.text}
