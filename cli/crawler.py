import asyncio
from crawl4ai import AsyncWebCrawler
from pydantic import BaseModel
import typer
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from lib.clients import openai

app = typer.Typer()


async def _crawl_async(url: str):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)
        return result.markdown


@app.command(name="crawl")
def crawl_site(url: str = typer.Option(..., help="The URL to crawl")):
    result = asyncio.run(_crawl_async(url))
    print(result)


class JobPost(BaseModel):
    employer: str
    role: str
    salary: str


@app.command(name="job-post")
def crawl_job_post(url: str = typer.Option(..., help="The URL to crawl")):
    result = asyncio.run(_crawl_async(url))
    template = """Return the employer, role, and salary of the job post."""

    prompt = ChatPromptTemplate.from_messages([("system", template), ("human", "{result}")])
    llm = openai.openai_chat.with_structured_output(JobPost)

    chain = {"result": RunnablePassthrough()} | prompt | llm

    response = chain.invoke({"question": result})
    print(response)
