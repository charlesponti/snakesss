from crewai_tools import ScrapeWebsiteTool


def scrape_website(url: str):
    tool = ScrapeWebsiteTool(website_url=url)
    text = tool.run()
    return text


def get_filename_from_url(url: str):
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
