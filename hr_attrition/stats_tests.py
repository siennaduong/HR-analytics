"""Compute descriptive statistics and run hypothesis tests on attrition."""

import numpy as np
import pandas as pd
from scipy import stats

# Significance level used by all hypothesis tests.
ALPHA = 0.05


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


def chi_square_test(df, column, alpha=ALPHA):
    """Test whether attrition is dependent of a categorical column.

    Uses the chi-square test of independence on the contingency table
    of ``column`` againts Attrition.

    Parameters
    ----------
    df : pandas.DataFrame
        The employee data, with an Attrition column.
    column : str
        Categorical column to test, for example "OverTime".
    alpha : float, optional
        Significance level. Defaults to 0.05.

    Returns
    -------
    dict
        The column name, the chi-square statistic, the degree of freedom,
        the p-value and whether the result is significant at ``alpha``.
    
    Raises
    ------
    KeyError
        If ``column`` is not a column of ``df``.
    """
    if column not in df.columns:
        raise KeyError(f"Column not found: {column}")

    table = pd.crosstab(df[column], df["Attrition"])
    result = stats.chi2_contingency(table)
    return {
        "column": column,
        "chi2": float(result.statistic),
        "dof": int(result.dof),
        "p_value": float(result.pvalue),
        "significant": bool(result.pvalue < alpha),
    }

def attrition_t_test(df, column="MonthlyIncome", alpha=ALPHA):
    """Compare the mean of a numeric column between leavers and stayers.

    Uses Welch's t-test, which does not assume equal variances.

    Parameters
    ----------
    df : pandas.DataFrame
        The employee data, with an Attrition column.
    column : str, optional
        Numeric column to compare. Defaults to "MonthlyIncome".
    alpha : float, optional
        Significance level. Defaults to 0.05.

    Returns
    -------
    dict
        The column name, the mean for leavers and for stayers, the t
        statistic, the p-value and whether the result is significant.

    Raises
    ------
    KeyError
        If ``column`` is not a column of ``df``.
    """
    if column not in df.columns:
        raise KeyError(f"Column not found: {column}")

    leavers = df.loc[df["Attrition"] == "Yes", column].to_numpy()
    stayers = df.loc[df["Attrition"] == "No", column].to_numpy()
    result = stats.ttest_ind(leavers, stayers, equal_var=False)
    return {
        "column": column,
        "mean_leavers": float(np.mean(leavers)),
        "mean_stayers": float(np.mean(stayers)),
        "t_statistic": float(result.statistic),
        "p_value": float(result.pvalue),
        "significant": bool(result.pvalue < alpha),
    }