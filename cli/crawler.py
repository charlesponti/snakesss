import asyncio

import typer
from crawl4ai import AsyncWebCrawler
from crewai_tools import ScrapeWebsiteTool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from pydantic import BaseModel

from lib.clients import openai

app = typer.Typer()


def _scrape_website(url: str):
    tool = ScrapeWebsiteTool(website_url=url)
    text = tool.run()
    return text


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


@app.command(name="scrape")
def scrape_website(url: str = typer.Option(..., help="The URL to scrape")):
    text = _scrape_website(url)
    print(text)


class HomeDetails(BaseModel):
    address: str
    city: str
    state: str
    zip_code: str
    price: str


@app.command(name="zillow")
def scrape_zillow(url: str = typer.Option(..., help="The URL to scrape")):
    text = _scrape_website(url)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Return the address, city, state, zip code, and price of the home."),
            ("human", "{home_description}"),
        ]
    )
    llm = openai.openai_chat.with_structured_output(HomeDetails)
    chain = {"home_description": RunnablePassthrough()} | prompt | llm
    response = chain.invoke({"home_description": text})
    print(response)


# "https://www.zillow.com/homedetails/1520-Amalfi-Dr-Pacific-Palisades-CA-90272/20546426_zpid/"
