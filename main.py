from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from routers import ollama

app = FastAPI()

app.include_router(ollama.router)


@app.get("/")
async def index():
    return {"message": "Hello Smurf"}
