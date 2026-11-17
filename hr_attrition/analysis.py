"""Aggregate employee data to compute attrition rates by group."""


def attrition_rate_by(df, column):
    """Compute the attrition rate for each group of a column.

    Parameters
    ----------
    df : pandas.DataFrame
        The cleaned employee data, with an AttritionFlag column.
    column : str
        Column to group by, for example "Department" or "OverTime".
    
    Returns
    -------
    pandas.DataFrame
        One row per group with the number of employees, the number who left and the 
        attrition rate, sorted from highest to lowest rate.
    
    Raises
    ------
    KeyError
        If 'column' is not a column of 'df'.
    """
    if column not in df.columns:
        raise KeyError(f"Column not found: {column}")

    summary = (
        df.groupby(column, as_index=False)
        .agg(
            employees=("AttritionFlag", "size"),
            leavers=("AttritionFlag", "sum"),
            attrition_rate=("AttritionFlag", "mean"),
        )
        .sort_values("attrition_rate", ascending=False)
    )
    return summary


def attrition_pivot(df, rows, columns):
    """Compute attrition rates for every combination of two columns.
    Parameters
    ----------
    df : pandas.DataFrame
        The cleaned employee data, with an AttritionFlag column.
    rows : str
        Columns whose groups become the rows, for example "Departments".
    columns : str
        Columns whose groups become the columns, for example "OverTime".

    Returns
    -------
    pandas.DataFrame
        Attrition rates with one row per group of 'rows' and one column
        per group of 'columns'.

    Raises
    ------
    KeyError
        If 'rows' or 'columns' is not a column of 'df'.
    """
    for name in (rows, columns):
        if name not in df.columns:
            raise KeyError(f"Column not found: {name}")
    return df.pivot_table(
        index=rows,
        columns=columns,
        values="AttritionFlag",
        aggfunc="mean",
    )