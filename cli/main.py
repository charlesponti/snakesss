import dotenv

dotenv.load_dotenv()

import sys
import typer

from cli.notes_etl import notes_app
from cli.user_story.user_story_generator import user_story_app
from lib.file_service import FileRepository
from lib.writing.utils import get_formatted_line, get_words, has_personal_pronouns

app = typer.Typer()
app.add_typer(notes_app)
app.add_typer(user_story_app)

@app.command()
def remove_duplicate_lines(
    file: str = typer.Argument(help="The file to remove duplicates from."),
):
    if len(file) < 2:
        print("Usage: python notes-analyzer.py --file <file>")
        sys.exit(1)

    with open(file, "r") as f:
        lines = f.readlines()
        print(f"Number of lines: {len(lines)}")
        self_referential_lines: set[str] = set()
        formatted_lines: set[str] = set()
        single_words: set[str] = set()

        for line in lines:
            formatted_line = get_formatted_line(line, lines)
            if formatted_line is None:
                continue
            if formatted_line not in formatted_lines and formatted_line not in self_referential_lines:
                words = get_words(formatted_line)
                if len(words) == 1:
                    single_words.add(formatted_line.replace("-", "").replace(" ", ""))
                elif has_personal_pronouns(words):
                    # Segment lines that have references to the writer.
                    self_referential_lines.add(formatted_line)
                else:
                    formatted_lines.add(formatted_line)

    with open(f"{file}-unduped.txt", "w") as f:
        print(f"Number of deduplicated lines: {len(formatted_lines)}")
        for line in formatted_lines:
            f.write(f"{line}\n")
        f.write("## Single words\n")
        for word in single_words:
            f.write(f"- {word}\n")

    with open(f"{file}-self-referential.txt", "w") as f:
        print(f"Number of self-referential lines: {len(self_referential_lines)}")
        for line in self_referential_lines:
            f.write(f"{line}\n")


@app.command()
def sort_file(file: str):
    sorted_lines: list[str] = []
    with open(file, "r") as f:
        lines = f.readlines()
        sorted_lines = [line for line in sorted(lines)]
    with open(f"{file}-sorted.txt", "w") as f:
        for line in sorted_lines:
            f.write(line)


@app.command()
def remove_duplicate_sections(file_path: str = typer.Option(help="The path to a text file.")):
    notes = FileRepository.get_file_contents(file_path)

    # Split file by "****"
    split_notes: list[str] = notes.split("****")
    print(f"Number of notes: {len(split_notes)}")

    # Remove duplicates
    notes = list(set(notes))
    print(f"Number of notes (without duplicates): {len(split_notes)}")

    # Write to file
    with open(f"{file_path}-unduped.txt", "w") as file:
        for note in notes:
            file.write(note)
            file.write("****")


if __name__ == "__main__":
    app()
