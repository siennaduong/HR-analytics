"""Streamlit app to explore employee attrition interactively."""

import matplotlib.pyplot as plt
import streamlit as st

from hr_attrition.analysis import attrition_rate_by
from hr_attrition.cleaning import (
    add_age_group,
    drop_constant_columns,
    encode_attrition,
)
from hr_attrition.data_loader import load_data
from hr_attrition.stats_tests import chi_square_test
from hr_attrition.visualization import plot_attrition_rate

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

factor = st.sidebar.selectbox("Choose a factor", FACTORS)

st.header(f"Attrition by {factor}")

summary = attrition_rate_by(df, factor)
fig = plot_attrition_rate(summary, factor, overall_rate)
st.pyplot(fig)
plt.close(fig)

result = chi_square_test(df, factor)
p_value = result["p_value"]
if result["significant"]:
    st.success(
        "Significant association with attrition "
        f"(chi-square test, p = {p_value:.2g})."
    )
else:
    st.info(
        "No significant association with attrition "
        f"(chi-square test, p = {p_value:.2g})."
    )

st.dataframe(summary, hide_index=True)