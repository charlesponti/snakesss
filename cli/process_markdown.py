import re
from sys import argv
import markdown
import json
import os
from pydantic import BaseModel
from bs4 import BeautifulSoup

core_elements = ["h1", "h2", "h3", "h4", "h5", "h6", "p", "ul", "ol", "li"]


class Note(BaseModel):
    file: str
    heading: str
    text: str
    tag: str | None = None
    date: str | None = None


def get_date(element: BeautifulSoup) -> str | None:
    full_date = re.search(r"\d{4}-\d{2}-\d{2}", element.get_text().strip())
    date = full_date.group(0) if full_date else None
    return date


def extract_data_from_html(html, filename):  # Updated function signature
    soup = BeautifulSoup(html, "html.parser")
    current_heading = None
    unique_headings = set()
    paragraphs = []
    bullet_points = []
    # Process known elements
    for element in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "ul", "ol"]):
        full_date = re.search(r"\d{4}-\d{2}-\d{2}", element.get_text().strip())
        date = full_date.group(0) if full_date else None
        tag = element.name
        if element.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            current_heading = element.get_text().strip()
            unique_headings.add(current_heading)
        elif element.name == "p":
            paragraphs.append(
                {
                    "file": filename,
                    "heading": current_heading,
                    "tag": tag,
                    "text": element.get_text().strip(),
                    "date": date,
                }
            )
        elif element.name in ["ul", "ol"]:
            for li in element.find_all("li"):
                bullet_points.append(
                    {
                        "file": filename,
                        "heading": current_heading,
                        "tag": tag,
                        "text": li.get_text().strip(),
                        "date": date,
                    }
                )
    # Capture extra elements not covered above
    others = []
    for element in soup.find_all(True):
        if element.name not in ["h1", "h2", "h3", "h4", "h5", "h6", "p", "ul", "ol", "li"]:
            text = element.get_text().strip()
            if text:
                others.append(
                    {"file": filename, "tag": element.name, "text": text, "date": get_date(element)}
                )
    return {
        "headings": list(unique_headings),
        "paragraphs": paragraphs,
        "bullet_points": bullet_points,
        "others": others,  # New field for extra elements
    }


def process_markdown_folder(folder_path):
    notes: list[Note] = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".md"):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, "r") as f:
                md_content = f.read()
                html = markdown.markdown(md_content)
                data_content = extract_data_from_html(html, filename)  # Updated call with filename

                for data in data_content["headings"]:
                    notes.append(Note(file=filename, heading=data, text="", tag="heading"))
                for data in data_content["paragraphs"]:
                    notes.append(
                        Note(
                            file=filename,
                            heading=data["heading"],
                            text=data["text"],
                            tag="paragraph",
                            date=data["date"],
                        )
                    )
                for data in data_content["bullet_points"]:
                    notes.append(
                        Note(file=filename, heading=data["heading"], text=data["text"], tag="bullet_point")
                    )
                for data in data_content["others"]:
                    notes.append(Note(file=filename, heading="", text=data["text"], tag=data["tag"]))

    with open("processed_data.json", "w") as outfile:
        json.dump(
            notes,
            outfile,
            indent=4,
        )


if __name__ == "__main__":
    process_markdown_folder(argv[1])
