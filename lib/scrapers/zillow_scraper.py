from typing import List, Optional
from pydantic import BaseModel
from lib.clients.openai import openai_client
from cli.crawlers.utils import scrape_website


class HomeDetails(BaseModel):
    address: str
    city: str
    state: str
    zip_code: str
    price: str
    bedrooms: float
    bathrooms: float
    square_footage: int
    lot_size: str
    year_built: int
    home_type: str
    days_on_market: int
    description: str
    amenities: list[str]
    school_rating: str
    neighborhood: str
    monthly_payment_estimate: str
    property_tax: str
    hoa_fee: Optional[str] = None
    fees: Optional[List[str]] = None


def get_home_details_from_zillow(url: str):
    """Extract home details from a Zillow listing URL"""
    text = scrape_website(url)

    completion = openai_client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Return details of the home listing with as many of these fields as you can find and determine based on the provided text and schema.",
            },
            {"role": "user", "content": text},
        ],
        response_format=HomeDetails,
    )

    response = completion.choices[0].message.parsed
    if not response:
        raise ValueError("Could not parse home details")

    return {"text": text, "details": response, "completion": completion}
