from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer




from src.routers.ai_router import ai_router
from src.routers.graphql import graphql_router
from src.routers.media_router import media_router
from src.routers.ollama import ollama_router

app = FastAPI()

# Allow CORS for all origins for simplicity
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Routers
app.include_router(ai_router)
app.include_router(graphql_router, prefix="/graphql")
app.include_router(media_router, prefix="/media")
app.include_router(ollama_router)

# Root
@app.get("/")
async def root():
    return {"message": "Hello World"}
