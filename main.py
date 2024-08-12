from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from routers import ollama, media

app = FastAPI()

app.include_router(ollama.router)
app.include_router(media.vision_router)


@app.get("/")
async def index():
    return {"message": "Hello Smurf"}
