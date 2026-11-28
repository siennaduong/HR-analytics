"""Streamlit app to explore employee attrition interactively."""

import matplotlib.pyplot as plt
import streamlit as st

from hr_attrition.analysis import attrition_pivot, attrition_rate_by
from hr_attrition.cleaning import (
    add_age_group,
    drop_constant_columns,
    encode_attrition,
)
from hr_attrition.data_loader import load_data
from hr_attrition.stats_tests import (
    attrition_t_test,
    chi_square_test,
    income_statistics,
)
from hr_attrition.visualization import (
    plot_attrition_heatmap,
    plot_attrition_rate,
    plot_income_by_attrition,
)

FACTORS = [
    "OverTime",
    "Department",
    "AgeGroup",
    "MaritalStatus",
    "JobRole",
    "Gender",
]


@st.cache_data
def get_clean_data():
    """Load the employee data and apply the cleaning steps.

    Returns
    -------
    pandas.DataFrame
        The cleaned data, with AttritionFlag and AgeGroup columns.
    """
    df = drop_constant_columns(load_data())
    df = encode_attrition(df)
    return add_age_group(df)


def format_p_value(p_value):
    """Format a p-value the way reports usually show it.

    Parameters
    ----------
    p_value : float
        The p-value of a statistical test.

    Returns
    -------
    str
        "p < 0.001" for very small values, otherwise the value
        with three decimals.
    """
    if p_value < 0.001:
        return "p < 0.001"
    return f"p = {p_value:.3f}"


st.set_page_config(page_title="Attrition Explorer")

st.title("Employee Attrition Explorer")
st.write(
    "Explore which employee characteristics are associated with "
    "leaving the company (IBM HR dataset)."
)

df = get_clean_data()
overall_rate = df["AttritionFlag"].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Employees", len(df))
col2.metric("Leavers", int(df["AttritionFlag"].sum()))
col3.metric("Attrition rate", f"{overall_rate:.1%}")

# Section 1: one factor at a time, chosen in the sidebar.
factor = st.sidebar.selectbox("Choose a factor", FACTORS)

st.header(f"Attrition by {factor}")

summary = attrition_rate_by(df, factor)
fig = plot_attrition_rate(summary, factor, overall_rate)
st.pyplot(fig)
plt.close(fig)

result = chi_square_test(df, factor)
p_text = format_p_value(result["p_value"])
if result["significant"]:
    st.success(
        f"Significant association with attrition (chi-square test, {p_text})."
    )
else:
    st.info(
        "No significant association with attrition "
        f"(chi-square test, {p_text})."
    )

st.dataframe(summary, hide_index=True)

st.divider()

# Section 2: the two factors with the strongest combined effect.
st.header("Age group and overtime combined")
pivot = attrition_pivot(df, "AgeGroup", "OverTime")
fig = plot_attrition_heatmap(pivot)
st.pyplot(fig)
plt.close(fig)
st.write("Young employees who work overtime are the highest-risk group.")

st.divider()

# Section 3: monthly income.
st.header("Monthly income of stayers and leavers")
fig = plot_income_by_attrition(df)
st.pyplot(fig)
plt.close(fig)

st.dataframe(income_statistics(df).round(0), hide_index=True)

t_result = attrition_t_test(df)
t_p_text = format_p_value(t_result["p_value"])
st.write(f"Welch t-test on monthly income: {t_p_text}. Leavers earn less.")