from typer import Typer

from cli.finance.starling_bank import app as starling_bank_app

app = Typer()

app.add_typer(starling_bank_app, name="starling-bank")

if __name__ == "__main__":
    app()
