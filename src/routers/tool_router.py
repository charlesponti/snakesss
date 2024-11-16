from typing import Annotated
from fastapi import APIRouter, Form
from langchain.pydantic_v1 import BaseModel
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

from lib.clients.openai import openai_chat
from lib.file_service import FileRepository

tool_router = APIRouter(prefix="/tools")


class WriterRewritten(BaseModel):
    message: str


@tool_router.post("/writer")
def writer_tool(message: Annotated[str, Form(...)]):
    structured_llm = openai_chat.with_structured_output(WriterRewritten)

    prompt = PromptTemplate(
        template=FileRepository.get_file_contents("prompts/writer.md"),
        partial_variables={"schema": WriterRewritten.schema_json()},
        input_variables=["user_input"],
    )

    chain = {"user_input": RunnablePassthrough()} | prompt | structured_llm
    response = chain.invoke({"user_input": message})

    return {"content": response}
