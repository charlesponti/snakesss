from typing import Annotated

from fastapi import APIRouter, Form
from fastapi.responses import StreamingResponse
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from lib.clients.llama import lmstudio_chat
from lib.clients.openai import openai_async_client
from lib.logger import logger

chat_router = APIRouter()


@chat_router.post("/chat/openai")
async def chat(message: str = Form(...)):
    response = await openai_async_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}],
        stream=False,
    )
    return {"text": response.choices[0].message.content}


@chat_router.post("/chat/openai/stream")
async def stream_chat(message: str = Form(...)):
    async def generate():
        stream = await openai_async_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}],
            stream=True,
        )
        async for chunk in stream:
            content = chunk.choices[0].delta.content
            if content is not None:
                logger.info(f" -- CHUNK -- {content} ")
                yield content

    return StreamingResponse(generate(), media_type="text/event-stream")


@chat_router.post("/chat/llama")
def chat_llama(message: Annotated[str, Form()]):
    prompt = ChatPromptTemplate(
        [("system", "You are a super intelligent personal assistant"), ("human", "{message}")]
    )
    chain = {"message": RunnablePassthrough()} | prompt | lmstudio_chat
    response = chain.invoke({"message": message})
    return response
