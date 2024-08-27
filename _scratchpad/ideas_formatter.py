import json
import os

import openai

import dotenv
dotenv.load_dotenv()

# Initialize OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to process content using OpenAI
def process_content(content):
    system_prompt = get_system_prompt()
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            { "content": system_prompt, "role": "system"},
            { "content": content, "role": "user" }
        ],
        max_tokens=500
    )
    return response.choices[0].message.content

# Function to parse the document
def parse_document(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    current_section = None
    current_subsection = None
    sections = {}

    for line in lines:
        line = line.strip()

        if line.startswith("## "):  # Main Section
            current_section = line[3:]
            if current_section not in sections:
                sections[current_section] = []
                current_subsection = None

        elif line.startswith("### "):  # Subsection
            current_subsection = line[4:]
            if current_subsection not in sections:
                sections[current_subsection] = []
            sections[current_subsection].append("")

        elif current_subsection:  # Content
            sections[current_subsection][-1] += line + "\n"

    return sections

def get_system_prompt() -> str:
    with open("src/prompts/writer.md", "r") as file:
        return file.read()

# Function to write processed content to files
def write_output(sections):
    for section, contents in sections.items():
        with open(f"{section}.txt", "a") as output_file:
            for content in contents:
                processed_content = process_content(content)
                if processed_content:
                    output_file.write(processed_content + "\n\n")

# Main execution
if __name__ == "__main__":
    input_file_path = "_scratchpad/_ideas.md"  # Change this to your input file path
    sections = parse_document(input_file_path)
    print(json.dumps(list(sections.keys()), indent=4))
    # write_output(sections)
