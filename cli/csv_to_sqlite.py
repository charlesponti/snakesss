import os
import pandas
import sqlite3
from typer import Typer, Argument


app = Typer(name="csv-to-sqlite")


@app.command(name="csv-to-sqlite")
def csv_to_sqlite(path: str = Argument(..., help="Path to the CSV file")):
    """
    Convert a CSV file to a SQLite database
    """

    """
    The user may provide a path relative to where the script is run
    If the path does not begin with `/`, the path starts with `.`, or does not start with either
    assume it is relative.
    """
    if (
        not path.startswith("/")
        or path.startswith(".")
        or (not path.startswith("/") and not path.startswith("."))
    ):
        path = os.path.join(os.getcwd(), path)

    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    # with open(path, "r") as csv_file:
    #     csv_reader = csv.reader(csv_file)

    # Connect to SQLite database and create table. Drop table if it already exists.
    conn = sqlite3.connect(os.path.join(os.getcwd(), "data.db"))
    # conn.execute("DROP TABLE IF EXISTS data")
    # conn.execute(f"CREATE TABLE data ({', '.join(headers)})")
    # conn.commit()

    df = pandas.read_csv(path)
    df.to_sql("data", conn, index=False, if_exists="replace")
    conn.close()
