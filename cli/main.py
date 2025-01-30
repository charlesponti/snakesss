import dotenv
import typer

dotenv.load_dotenv()

from cli.calculations import distance_matrix, fibonacci, rate_of_return  # noqa: E402
from cli.notes.notes_cli import notes_app  # noqa: E402
from cli.user_story.user_story_generator import user_story_app  # noqa: E402
from cli.crawler import app as crawler  # noqa: E402

app = typer.Typer()
app.add_typer(notes_app)
app.add_typer(user_story_app)
app.add_typer(crawler, name="crawler")

# Calculations
app.add_typer(rate_of_return.app)
app.add_typer(fibonacci.app, name="fibonacci")
app.add_typer(distance_matrix.app, name="fibonacci")

if __name__ == "__main__":
    app()
