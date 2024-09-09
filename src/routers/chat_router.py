import json
from typing import Annotated

from fastapi import APIRouter, Form
from fastapi.responses import StreamingResponse
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_core.runnables import RunnablePassthrough

from lib.clients.llama import llama_chat, lmstudio_chat
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


chunk_system_prompt = """
You are an expert at taking a long text and splitting it into smaller chunks.
You are especially good at identifying grouping chunks that are related to each other, such as if the user says
"I want to buy groceries, finish a report by tomorrow, and check my email for updates." you should split it into
three chunks: "I want to buy groceries", "finish a report by tomorrow", and "check my email for updates."

You are also capable of identifying chunks that are unrelated to each other, such as if the user says "I want to
buy groceries and check my email for updates." you should split it into two chunks: "I want to buy groceries" and
"check my email for updates."

## Rules:
- You must group chunks that are related to each other.
- You must not group chunks that are not related to each other.
- You must respond in valid JSON format.
- You MUST NOT include any explanation or context in your response.
- You MUST NOT include any additional information in your response.
- You MUST NOT include any additional fields in your response.
- You MUST NOT include any additional formatting, such as line breaks or indentation or Markdown.
- Remove any references to the user, such as "I", "you", etc.
- The chunks must be in the same order as the user said them.
- The chunks should use decisive language, such as "Go to the grocery store" instead of "I have to go to the grocery store."
- Do not summarize the user's message. Include all the information the user said in the chunks.
"""

chunk_examples = [
    {
        "input": "I have to go to the grocery store and buy milk, email my boss, and check my email for updates.",
        "output": json.dumps(
            {
                "chunks": [
                    {"text": "Go to the grocery store and buy milk"},
                    {"text": "Email boss"},
                    {"text": "Check email for updates."},
                ]
            }
        ),
    },
    {
        "input": "I have to pick up my kids from school and go to the park.",
        "output": json.dumps({"chunks": [{"text": "Pick up kids from school"}, {"text": "Go to the park."}]}),
    },
]


@chat_router.post("/chat/llama/chunk")
def chat_llama_chunk(message: Annotated[str, Form()]):
    chunk_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{input}"),
            ("ai", "{output}"),
        ]
    )
    prompt = ChatPromptTemplate(
        [
            ("system", chunk_system_prompt),
            FewShotChatMessagePromptTemplate(
                example_prompt=chunk_prompt,
                examples=chunk_examples,
            ),
            ("human", "{message}"),
        ]
    )
    chain = {"message": RunnablePassthrough()} | prompt | lmstudio_chat
    response = chain.invoke({"message": message})
    try:
        if isinstance(response.content, str):
            json_response = json.loads(response.content)
            return json_response
        else:
            return response.content
    except json.JSONDecodeError:
        return response.content


@chat_router.post("/chat/llama")
def chat_llama(message: Annotated[str, Form()]):
    prompt = ChatPromptTemplate(
        [("system", "You are a super intelligent personal assistant"), ("human", "{message}")]
    )
    chain = {"message": RunnablePassthrough()} | prompt | llama_chat
    response = chain.invoke({"message": message})
    return response
