from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from routers import hollywood, ollama

app = FastAPI()

app.include_router(hollywood.router)
app.include_router(ollama.router)


@app.get("/")
async def index():
    return {"message": "Hello Smurf"}


# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app, port=5000, reload=True)
