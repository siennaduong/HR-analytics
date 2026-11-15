"""Load the IBM HR dataset safely and save result tables and figures to output folder."""

from pathlib import Path


import pandas as pd

# Go up two levels: data_loader.py -> hr_attrition/ -> HR-analytics/ (project root)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "WA_Fn-UseC_-HR-Employee-Attrition.csv"


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
    # TODO 1: convert file_path into a Path object
    #         (the caller might pass a plain string like "data/x.csv")
    file_path = Path(file_path)

    # TODO 2: if the file does not exist, raise FileNotFoundError
    #         with a message that includes the full path that was tried
    if not file_path.exists(): 
        raise FileNotFoundError(f"Data file not found: {file_path}")
    
    # TODO 3: read the CSV inside a try block
    #         - except pd.errors.EmptyDataError -> raise ValueError("...")
    #         - except pd.errors.ParserError    -> raise ValueError("...")

    # TODO 4: return the DataFrame

