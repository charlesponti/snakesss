import dotenv
import typer

dotenv.load_dotenv()

from cli.calculations.rate_of_return import rate_of_return_app  # noqa: E402
from cli.notes.notes_cli import notes_app  # noqa: E402
from cli.user_story.user_story_generator import user_story_app  # noqa: E402

app = typer.Typer()
app.add_typer(notes_app)
app.add_typer(user_story_app)
app.add_typer(rate_of_return_app)

if __name__ == "__main__":
    app()
