from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from src.routers.chat_router import chat_router
from src.routers.graphql import graphql_router
from src.routers.media.audio_router import audio_router
from src.routers.user_intent import UserIntentRouter

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
app.include_router(chat_router)
app.include_router(graphql_router, prefix="/graphql")
app.include_router(audio_router, prefix="/media")
app.include_router(UserIntentRouter)


# Root
@app.get("/info")
async def root():
    return {"message": "🐍🐍🐍"}
