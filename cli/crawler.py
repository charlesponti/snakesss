import os
import typer
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from pydantic import BaseModel
from crewai_tools import ScrapeWebsiteTool
from lib.clients.ollama import llama

app = typer.Typer()


def _scrape_website(url: str):
    tool = ScrapeWebsiteTool(website_url=url)
    text = tool.run()
    return text


@app.command(name="scrape")
def scrape_website(url: str = typer.Option(..., help="The URL to scrape")):
    text = _scrape_website(url)
    url_parts = url.split("/")

    if url_parts[0].rfind("http") != -1:
        domain = url_parts[2]
    else:
        domain = url_parts[0]

    last_index = len(url_parts) - 1
    route = ""
    while route == "":
        route = url_parts[last_index]
        last_index -= 1

    output_path = os.path.join(os.getcwd(), f"{domain} - {route}.md")

    with open(output_path, "w") as f:
        f.write(str(text))


class JobPost(BaseModel):
    company: str
    status: str
    role: str
    salary: str


def get_ollama_client():
    return Ollama(model="llama3.2")


def _get_filename_from_url(url: str):
    url_parts = url.split("/")

    if url_parts[0].rfind("http") != -1:
        domain = url_parts[2]
    else:
        domain = url_parts[0]
    domain = ".".join(domain.split(".")[:-1])

    last_index = len(url_parts) - 1
    route = ""
    while route == "":
        route = url_parts[last_index]
        last_index -= 1

    # Remove query parameters
    route = route.split("?")[0]

    return f"{domain} - {route}"


@app.command(name="job-post")
def crawl_job_post(url: str = typer.Option(..., help="The URL to crawl")):
    result = _scrape_website(url)
    template = """Return the employer, role, and salary of the job post."""

    prompt = ChatPromptTemplate.from_messages([("system", template), ("human", "{result}")])
    llm = llama.with_structured_output(JobPost)

    chain = {"result": RunnablePassthrough()} | prompt | llm

    chain_response = chain.invoke({"question": result})
    response = JobPost.model_validate(chain_response)

    output_path = os.path.join(os.getcwd(), f"{_get_filename_from_url(url)}.json")
    with open(output_path, "w") as f:
        f.write(response.model_dump_json())


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
    llm = get_ollama_client().with_structured_output(HomeDetails)
    chain = {"home_description": RunnablePassthrough()} | prompt | llm
    response = chain.invoke({"home_description": text})
    print(response)


# "https://www.zillow.com/homedetails/1520-Amalfi-Dr-Pacific-Palisades-CA-90272/20546426_zpid/"

if __name__ == "__main__":
    app()
