"""Clean the raw data and prepare data for analysis."""


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