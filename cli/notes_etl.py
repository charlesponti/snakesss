"""
!TODO Analyze documents and apply tags
!TODO Analyze documents line-by-line
!TODO Fix base-level grammar and spelling mistakes
"""

from datetime import datetime
import json
import os
from time import time_ns
from typing import Dict, List

import openai
import typer

from lib.clients.openai import get_openai_chat_completion
from lib.file_service import FileRepository


# Initialize OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

notes_app = typer.Typer(name="notes")


def get_document_sections(file_lines: List[str]):
    current_section = None
    current_subsection = None
    current_subsection_depth = 0
    sections: Dict[str, list[str]] = {}

    for line in file_lines:
        line = line.strip()
        if len(line) == 0:
            continue

        if line.startswith("# "):
            current_section = line[2:]
            if current_section not in sections:
                sections[current_section] = []
                current_subsection = None

        elif line.startswith("## "):
            section_name = line[3:]
            if current_section and current_subsection_depth == 0:
                current_subsection_depth = 1
                sections[current_section].append(line)
                current_subsection = section_name
            else:
                sections[section_name] = []
                current_subsection = None

        elif line.startswith("### "):
            section_name = line[4:]
            if current_subsection and current_subsection_depth == 1:
                sections[current_subsection].append(line)
                current_subsection = section_name
                current_subsection_depth = 2
            else:
                sections[section_name] = []
                current_subsection = None

    return sections


# Function to write processed content to files
async def write_output(sections):
    for section, contents in sections.items():
        with open(f"{section}.txt", "a") as output_file:
            for content in contents:
                processed_content = await get_openai_chat_completion(
                    system_message=FileRepository.get_file_contents("src/prompts/writer.md"),
                    user_message=content,
                )
                if processed_content:
                    output_file.write(processed_content + "\n\n")


@notes_app.command(name="line-items")
def get_line_items(file_path: str = typer.Argument(..., help="Path to the file to be parsed")):
    lines, seconds_taken = FileRepository.get_file_line_items(file_path=file_path)

    print("Time taken to process file in seconds:", seconds_taken)
    return len(lines)


@notes_app.command(name="get_file_section_names")
def get_file_section_names(file_path: str = typer.Argument(..., help="Path to the file to be parsed")):
    file_lines = FileRepository.get_file_lines(file_path=file_path)
    sections = get_document_sections(file_lines)
    section_names = sorted((list(sections.keys())))
    print(json.dumps(section_names, indent=4))


@notes_app.command(name="get_file_sections")
def get_file_sections(file_path: str = typer.Argument(..., help="Path to the file to be parsed")):
    file_lines = FileRepository.get_file_lines(file_path=file_path)
    sections = get_document_sections(file_lines)
    # section_names = sorted((list(sections.keys())))
    print(json.dumps(sections, indent=4))
    # print(json.dumps(sections[section_names[10]], indent=4))
    # write_output(sections)
