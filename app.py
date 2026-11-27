"""Streamlit app to explore employee attrition interactively."""

import streamlit as st

from hr_attrition.cleaning import (
    add_age_group,
    drop_constant_columns,
    encode_attrition,
)
from hr_attrition.data_loader import load_data


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