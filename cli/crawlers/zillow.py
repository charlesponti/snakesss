import os
import typer
from lib.costs import calculate_token_costs, token_costs_to_dataframe
from lib.scrapers import get_home_details_from_zillow
from cli.crawlers.utils import get_filename_from_url


zillow_app = typer.Typer()


@zillow_app.command(name="scrape")
def scrape_zillow(url: str = typer.Option(..., help="The URL to scrape")):
    # Get home details using the extracted scraper function
    result = get_home_details_from_zillow(url)

    # Calculate costs using the extracted cost calculator
    cost_info = calculate_token_costs(result["completion"].usage, input_price=0.0000025, output_price=0.00001)

    # Print cost information as a formatted table
    cost_table = token_costs_to_dataframe(cost_info)
    print(cost_table)

    # Save results to files
    url_filename = get_filename_from_url(url)
    filename = f"{url_filename}.json"
    markdown_filename = f"{url_filename}.md"

    with open(os.path.join(os.getcwd(), markdown_filename), "w") as f:
        f.write(result["text"])
        print(f"Home details saved to ./{markdown_filename}")

    with open(os.path.join(os.getcwd(), filename), "w") as f:
        f.write(result["details"].model_dump_json(indent=2))
        print(f"Home details saved to ./{filename}")


if __name__ == "__main__":
    zillow_app()
