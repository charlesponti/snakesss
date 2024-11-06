import os
from typing import Annotated, Optional

import typer
from huggingface_hub import snapshot_download

app = typer.Typer()


@app.command()
def download_flux(
    filepath: Annotated[
        Optional[str], typer.Argument(help="Directory to save the FLUX model (default: ./data/flux1-schnell)")
    ],
):
    """Download the FLUX.1-schnell model from Hugging Face Hub."""

    filepath = filepath or "./data/flux1-schnell"
    try:
        snapshot_download(repo_id="black-forest-labs/FLUX.1-schnell", local_dir=os.path.abspath(filepath))
        typer.echo(f"Successfully downloaded FLUX model to {filepath}")
    except Exception as e:
        typer.echo(f"Error downloading FLUX model: {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
