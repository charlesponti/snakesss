# Read --file from command line and open file

import sys
import typer

app = typer.Typer()


@app.command()
def hello(name: str):
    typer.echo(f"Hello {name}")


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        typer.echo(f"Goodbye Ms. {name}. Have a good day.")
    else:
        typer.echo(f"Bye {name}!")


@app.command()
def add(x: int, y: int):
    typer.echo(f"{x} + {y} = {x + y}")


# This command will remove duplicate lines from a file.
# The first occurance of a line will be kept. Subsequent occurances will be removed.
# Usage: python notes-analyzer.py remove_duplicate_lines --file <file>
@app.command()
def remove_duplicate_lines(file: str):
    if len(file) < 2:
        print("Usage: python notes-analyzer.py --file <file>")
        sys.exit(1)

    with open(file, "r") as f:
        lines = f.readlines()
        print(f"Number of lines: {len(lines)}")
        list_set = []

        for line in lines:
            if line.startswith("#"):
                list_set.append(line)
            # Add empty lines that are not preceded by empty line
            if line.strip() == "" and not list_set[-1].strip() == "":
                list_set.append(line)
            elif line not in list_set:
                list_set.append(line)

        print(f"Number of lines (without duplicates): {len(list_set)}")

    with open(f"{file}-unduped.txt", "w") as f:
        for line in list_set:
            f.write(line)


@app.command()
def remove_duplicate_sections(file: str):
    if len(file) < 2:
        print("Usage: python notes-analyzer.py --file <file>")
        sys.exit(1)

    with open(file, "r") as f:
        notes = f.read()

        # Split file by "****"
        notes = notes.split("****")
        print(f"Number of notes: {len(notes)}")

        # Remove duplicates
        notes = list(set(notes))
        print(f"Number of notes (without duplicates): {len(notes)}")

        # Write to file
        with open(f"{file}-unduped.txt", "w") as f:
            for note in notes:
                f.write(note)
                f.write("****")


if __name__ == "__main__":
    app()
