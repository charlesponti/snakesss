import os
import typer
from cli.crawlers.job_post import convert_text_to_job_post
from cli.crawlers.zillow import scrape_zillow
from cli.crawlers.utils import get_filename_from_url, scrape_website

app = typer.Typer()


@app.command(name="scrape")
def _scrape_website(url: str = typer.Option(..., help="The URL to scrape")):
    text = scrape_website(url)
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


@app.command(name="job-post")
def crawl_job_post(url: str = typer.Option(..., help="The URL to crawl")):
    result = _scrape_website(url)
    if not result:
        raise ValueError("No text found on the website")

    response = convert_text_to_job_post(result)

    output_path = os.path.join(os.getcwd(), f"{get_filename_from_url(url)}.json")
    with open(output_path, "w") as f:
        f.write(response.model_dump_json())


app.command(name="zillow")(scrape_zillow)

if __name__ == "__main__":
    app()
