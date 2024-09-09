import json
import requests
from typing import Annotated

from fastapi import APIRouter, Form
from langchain.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough

from lib.clients.openai import openai_chat
from lib.file_service import FileRepository
from src.routers.user_intent.user_intent_models import (
    Intent,
    user_intent_examples
)
from src.routers.user_intent.user_intent_tools import (
    CreateTasksFunction,
    EditTaskFunction,
    SearchTasksFunction,
)

file_repository = FileRepository()

user_intent_router = APIRouter(
    prefix="/api/user_intent",
    tags=["llama"],
)

system_prompt = FileRepository.get_file_contents("src/routers/user_intent/user_intent_prompt.md")

openai_system_prompt = FileRepository.get_file_contents("src/routers/user_intent/user_intent_prompt_openai.md")

instruct_model = "lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"

lmstudio_url = "http://host.docker.internal:1234/v1/chat/completions"

@user_intent_router.post("/llama")
def chat(user_input: Annotated[str, Form()]):
    response = requests.post(
        url=lmstudio_url,
        json={
            "model": instruct_model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt + f"\n\n{user_input} <|eot_id|><|start_header_id|>assistant<|end_header_id|>"
                },
            ],
            "temperature": 0.7,
            "max_tokens": -1,
            "stream": False
        }
    )

    result = response.json()
    function_name = None
    error = None
    parsed = None
    values = None

    try:
        parsed = json.loads(result["choices"][0]["message"]["content"])
    except json.JSONDecodeError:
        parsed = None
        error = "Could not parse response"

    return {
        "error": error,
        "response": parsed,
        "function_name": function_name,
        "values": values,
        "usage": result["usage"]
    }


@user_intent_router.post("/openai")
def get_user_intent(user_input: Annotated[str, Form()]):
    openai_chat.bind_tools([
        CreateTasksFunction,
        SearchTasksFunction,
        EditTaskFunction,
    ])

    structured_llm = openai_chat.with_structured_output(Intent)

    # Define the prompt template
    chat_prompt = ChatPromptTemplate([
        ("system", openai_system_prompt),
        MessagesPlaceholder("examples", optional=False),
        ("human", "{user_input}")
    ])

    chain = (
        {"user_input": RunnablePassthrough()} |
        chat_prompt.partial(examples=user_intent_examples) |
        structured_llm
    )

    result = chain.invoke({"user_input": user_input})

    return result
