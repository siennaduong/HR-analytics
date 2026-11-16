"""Load the IBM HR dataset safely and save result tables and figures to output folder."""

from pathlib import Path


import pandas as pd

# Go up two levels: data_loader.py -> hr_attrition/ -> HR-analytics/ (project root)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "WA_Fn-UseC_-HR-Employee-Attrition.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs"


def load_data(file_path=DEFAULT_DATA_PATH):
    """Load the IBM HR Employee Attrition CSV file into a DataFrame.

    Parameters
    ----------
    file_path : str or pathlib.Path, optional
        Location of the CSV file. Defaults to the copy in the data/ folder.

    Returns
    -------
    pandas.DataFrame
        One row per employee and one column per attribute.

    Raises
    ------
    FileNotFoundError
        If no file exists at ``file_path``.
    ValueError
        If the file is empty or cannot be parsed as CSV.
    """
    # Accept both str and Path input.
    file_path = Path(file_path)

    # Fail early with a clear message if the file is missing.
    if not file_path.exists(): 
        raise FileNotFoundError(f"Data file not found: {file_path}")
    
    # Turn pandas reading errors into clear ValueErrors.
    try:
        df = pd.read_csv(file_path)
    except pd.errors.EmptyDataError:
        raise ValueError(f"File is empty: {file_path}")
    except pd.errors.ParserError:
        raise ValueError(f"Incorrect file format: {file_path}")

    return df


def save_table(table, file_name, output_dir=OUTPUT_DIR):
    """Save a DataFrame as a CSV file in the output folder.

    Parameters
    ----------
    table : pandas.DataFrame
        The table to save.
    file_name : str
        Name of the CSV file, for example "attrition_by_department.csv".
    output_dir : str or pathlib.Path, optional
        Folder where the file is written. Defaults to the outputs/ folder.

    Returns
    -------
    pathlib.Path
        Full path of the saved file.
    """
    # Accept both str and Path input.
    output_dir = Path(output_dir)

    # Create the folder if it does not exist yet.
    output_dir.mkdir(parents=True, exist_ok=True)

    # Build the full path, write the table, and return where it was saved.
    file_path = output_dir / file_name
    table.to_csv(file_path, index=False)
    return file_path