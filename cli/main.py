import dotenv
import typer

dotenv.load_dotenv()

from cli.calculations import distance_matrix, fibonacci, rate_of_return  # noqa: E402

from cli.notes.notes_cli import notes_app  # noqa: E402
from cli.user_story.user_story_generator import user_story_app  # noqa: E402

from cli.crawlers.main import app as crawler  # noqa: E402
import cli.nexus as nexus  # noqa: E402

app = typer.Typer()
app.add_typer(notes_app, name="notes")
app.add_typer(user_story_app, name="user-story")
app.add_typer(crawler, name="crawler")
app.add_typer(rate_of_return.app)
app.add_typer(fibonacci.app, name="blarb")
app.add_typer(distance_matrix.app, name="distance-matrix")
app.add_typer(nexus.app, name="nexus")


@app.command()
def main():
    """Main CLI entrypoint."""
    typer.echo("Welcome to snakesss!")


if __name__ == "__main__":
    print("Running main")
    app()
