import numpy as np
from scipy.spatial import distance_matrix
import pandas as pd
import json
from pathlib import Path
from typing import List, Tuple, Literal


def parse_coordinates(coord_str: str) -> Tuple[float, float]:
    """Parse coordinate string in format 'x,y'"""
    x, y = map(float, coord_str.split(","))
    return (x, y)


def calculate_distance_matrix(coordinates: np.ndarray, metric: str = "euclidean") -> np.ndarray:
    """Calculate distance matrix using specified metric"""
    p_value = {"manhattan": 1, "euclidean": 2, "chebyshev": np.inf}.get(metric, 2)

    return distance_matrix(coordinates, coordinates, p=p_value)


def calculate(
    coordinates: List[str], input_file: Path, metric: str, output_format: Literal["text", "csv", "json"]
):
    """
    Calculate distances between coordinates using various metrics

    Args:
        coordinates (List[str]): List of coordinates in format 'x,y'. Example: 0,0 1,1 2,1
        input_file (Path): Path to a file containing coordinates (one pair per line: x,y).
        metric (str): Distance metric to use (manhattan, euclidean, or chebyshev).
        output_format (str): Output format (text, csv, or json).

    Raises:
        Exception: If no coordinates or input file is provided.
        typer.Exit: If there is an error reading the input file.

    Returns:
        str: The distance matrix in the specified output format.

    """
    if not coordinates and not input_file:
        raise Exception("Please provide coordinates or an input file")

    # Get coordinates from file or arguments
    if input_file:
        try:
            with open(input_file) as f:
                coordinates = [line.strip() for line in f if line.strip()]
        except Exception as e:
            raise Exception(f"Error reading file: {e}")

    try:
        # Convert coordinates to numpy array
        coord_array = np.array([parse_coordinates(c) for c in coordinates])

        # Calculate distance matrix
        result = calculate_distance_matrix(coord_array, metric)

        # Format output
        if output_format == "text":
            return result
        elif output_format == "csv":
            df = pd.DataFrame(result)
            return df.to_csv(index=False)
        else:
            return json.dumps({"metric": metric, "matrix": result.tolist()}, indent=2)

    except Exception as e:
        return {"error": f"Error calculating distances: {e}"}
