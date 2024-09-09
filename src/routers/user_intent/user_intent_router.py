import json
from typing import Annotated

from fastapi import APIRouter, Form
from langchain.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough

from lib.clients.llama import lmstudio_chat
from lib.clients.openai import openai_chat
from lib.file_service import FileRepository

from src.routers.user_intent.user_intent_models import (
    Intent,
    get_user_intent_few_shot_examples,
    user_intent_examples,
)
from src.routers.user_intent.user_intent_tools import (
    CreateTasksFunction,
    EditTaskFunction,
    SearchTasksFunction,
)

file_repository = FileRepository()

user_intent_router = APIRouter(prefix="/api/user_intent")

system_prompt = FileRepository.get_file_contents("src/routers/user_intent/user_intent_prompt.md")

openai_system_prompt = FileRepository.get_file_contents(
    "src/routers/user_intent/user_intent_prompt_openai.md"
)

instruct_model = "lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"

lmstudio_url = "http://host.docker.internal:1234/v1/chat/completions"


@user_intent_router.post("/llama")
def chat(user_input: Annotated[str, Form()]):
    lmstudio_chat.bind_tools(
        [
            CreateTasksFunction,
            SearchTasksFunction,
            EditTaskFunction,
        ]
    )

    prompt = ChatPromptTemplate(
        [
            ("system", openai_system_prompt),
            FewShotChatMessagePromptTemplate(
                example_prompt=ChatPromptTemplate(
                    [
                        ("human", "{input}"),
                        ("ai", "{output}"),
                    ]
                ),
                examples=user_intent_examples,
            ),
            ("human", "{user_input}"),
        ]
    )

    chain = (
        {"user_input": RunnablePassthrough()} | prompt.partial(examples=user_intent_examples) | lmstudio_chat
    )

    result = chain.invoke({"user_input": user_input})

    function_name = None
    error = None
    parsed = None
    values = None

    if isinstance(result.content, str):
        try:
            parsed = json.loads(result.content)
        except Exception as e:
            print(json.dumps(result, indent=2), e)
            parsed = None
            error = "Could not parse response"
    else:
        parsed = result.content

    return {
        "error": error,
        "response": parsed,
        "function_name": function_name,
        "values": values,
        "usage": result.response_metadata["token_usage"],
    }


@user_intent_router.post("/openai")
def get_user_intent(user_input: Annotated[str, Form()]):
    openai_chat.bind_tools(
        [
            CreateTasksFunction,
            SearchTasksFunction,
            EditTaskFunction,
        ]
    )

    structured_llm = openai_chat.with_structured_output(Intent)

    # Define the prompt template
    chat_prompt = ChatPromptTemplate(
        [
            ("system", openai_system_prompt),
            MessagesPlaceholder("examples", optional=False),
            ("human", "{user_input}"),
        ]
    )

    chain = (
        {"user_input": RunnablePassthrough()}
        | chat_prompt.partial(examples=get_user_intent_few_shot_examples())
        | structured_llm
    )

    result = chain.invoke({"user_input": user_input})

    return result
