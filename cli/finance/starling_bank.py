import pandas as pd
import os

import typer

app = typer.Typer(name="starling-bank")


def convert_csvs_to_single(folder_path):
    """
    Converts multiple CSVs in a folder to a single CSV.

    Args:
        folder_path: Path to the folder containing the CSVs.

    Returns:
        None
    """

    all_data = []
    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            file_path = os.path.join(folder_path, file)
            df = pd.read_csv(file_path)

            # Convert 'Date' column to datetime and format as 'YYYY-MM-DD'
            try:
                df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")
                df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
            except ValueError as e:
                # The date format may already be 'YYYY-MM-DD' format
                if "doesn't match format" in str(e):
                    df["Date"] = pd.to_datetime(df["Date"], format="mixed")
                    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")

            # Filter rows with 'Opening Balance'
            opening_balance_row = df[df["Counter Party"] == "Opening Balance"].copy()
            opening_balance_row["Date"] = "1900-01-01"  # Set a placeholder date

            # Append to the list of dataframes
            all_data.append(opening_balance_row)
            all_data.append(df)

    # Concatenate all dataframes into a single dataframe
    final_df = pd.concat(all_data, ignore_index=True)

    # Sort by date
    final_df = final_df.sort_values(by="Date")

    # Save the final dataframe to a new CSV
    final_df.to_csv("combined_data.csv", index=False)


@app.command("merge-multiple", help="Merge multiple Starling Bank CSV Statements into a single CSV.")
def merge_multiple(folder_path: str = typer.Argument(..., help="Path to the folder containing the CSVs.")):
    convert_csvs_to_single(folder_path)
