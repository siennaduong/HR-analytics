"""Clean the raw data and prepare data for analysis."""

import pandas as pd

# Age bands: (17,29] means 18 to 29 and so on.
AGE_BINS = [17, 29, 39, 49, 60]
AGE_LABELS = ["18-29", "30-39", "40-49", "50-60"]

def count_missing_values(df):
    """Count the missing values in each column.
    
    Parameters
    ----------
    df: pandas.DataFrame
        The employee data.

    Returns
    -------
    pandas.Series
        Number of missing values per column, only for the columns that have
        at least one. Empty if the data has no missing value
    """
    missing = df.isna().sum()
    return missing[missing > 0]


def drop_constant_columns(df):
    """Remove columns that hold the same value for every employee.

    Such columns (EmployeeCount, Over18 and StandardHours in the IBM data)
    carry no information for the analysis.
    
    Parameters
    ----------
    df : pandas.DataFrame
        The employee data.
        
    Returns
    -------
    pandas.DataFrame
        A copy of the data without the constant columns.
    """
    unique_counts = df.nunique()
    constant_columns = unique_counts[unique_counts == 1].index
    return df.drop(columns=constant_columns)

def encode_attrition(df):
    """Add an AttritionFlag column where "Yes" becomes 1 and "No" becomes 0.
    
    The mean of this column is the attrition rate.
    
    Parameters
    ----------
    df : pandas.DataFrame
        The employee data, with an Attrition column of "Yes"/"No" values.
        
    Returns
    -------
    pandas.DataFrame
        A copy of the data with the new AttritionFlag column.
        
    Raises
    ------
    ValueError
        If Attrition holds a value other than "Yes" or "No".
    """
    df = df.copy()
    df["AttritionFlag"] = df["Attrition"].map({"Yes": 1, "No": 0})
    if df["AttritionFlag"].isna().any():
        raise ValueError("Attrition must contain only 'Yes' or 'No'.")
    return df


def add_age_group(df):
    """Add an AgeGroup column that places each employee in an age band.

    Parameters
    ----------
    df: pandas.DataFrame
        The employee data, with an Age column.

    Returns
    -------
    pandas.DataFrame
        A copy of the data with the new AgeGroup column.
    """
    df = df.copy()
    df["AgeGroup"] = pd.cut(df["Age"], bins=AGE_BINS, labels=AGE_LABELS)
    return df