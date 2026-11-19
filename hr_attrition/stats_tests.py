"""Compute descriptive statistics and run hypothesis tests on attrition."""

import numpy as np
import pandas as pd


def income_statistics(df, group_column="Attrition"):
    """Describe monthly income for each group of a column using NumPy.

    Parameters
    ----------
    df : pandas.DataFrame
        The employee data, with a MonthlyIncome column.
    group_column : str, optional
        Column that defines the groups. Defaults to "Attrition".
    
    Returns
    -------
    pandas.DataFrame
        One row per group with the number of employees, mean, sample
        standard deviation, 25th percentile, median and 75th percentile 
        of monthly income.
    
    Raises
    ------
    KeyError
        If ``group_column`` is not a column of ``df``.
    """
    if group_column not in df.columns:
        raise KeyError(f"Column not found: {group_column}")

    rows = []
    for group, group_df in df.groupby(group_column):
        income = group_df["MonthlyIncome"].to_numpy()
        p25, p50, p75 = np.percentile(income, [25, 50, 75])
        rows.append(
            {
                group_column: group,
                "employees": income.size,
                "mean": np.mean(income),
                "std": np.std(income, ddof=1),
                "p25": p25,
                "median": p50,
                "p75": p75,
            }
        )
    return pd.DataFrame(rows)