"""Create charts showing how employee attributes relate to attrition."""

import matplotlib.pyplot as plt
import seaborn as sns

# Colours: blue for the main series, orange for the contrasting group.
BLUE = "#2a78d6"
ORANGE = "#eb6834"
GREY = "#52514e"


def plot_attrition_rate(summary, column, overall_rate=None):
    """Draw a horizontal bar chart of the attrition rate by group.

    Parameters
    ----------
    summary : pandas.DataFrame
        Output of ``attrition_rate_by``, with ``column`` and an
        attrition_rate column.
    column : str
        Name of the grouping column, used for the labels.
    overall_rate : float, optional
        Company-wide attrition rate, drawn as a dashed reference line.

    Returns
    -------
    matplotlib.figure.Figure
        The chart.
    """
    data = summary.sort_values("attrition_rate")
    labels = data[column].astype(str)
    rates = data["attrition_rate"] * 100

    fig, ax = plt.subplots(figsize=(8, 0.6 * len(data) + 1.5))
    bars = ax.barh(labels, rates, color=BLUE, height=0.6)
    ax.bar_label(bars, fmt="%.1f%%", padding=4)

    if overall_rate is not None:
        ax.axvline(
            overall_rate * 100,
            color=GREY,
            linestyle="--",
            linewidth=1,
            label=f"Company average ({overall_rate:.1%})",
        )
        ax.legend(loc="lower right", frameon=False)

    ax.set_title(f"Attrition rate by {column}")
    ax.set_xlabel("Attrition rate (%)")
    ax.set_ylabel(column)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    return fig


def plot_attrition_heatmap(pivot):
    """Draw a heatmap of attrition rates for two combined factors.

    Parameters
    ----------
    pivot : pandas.DataFrame
        Output of ``attrition_pivot``: attrition rates with one factor
        as rows and the other as columns.

    Returns
    -------
    matplotlib.figure.Figure
        The chart.
    """
    fig, ax = plt.subplots(figsize=(6, 0.6 * len(pivot) + 2))
    sns.heatmap(
        pivot * 100,
        annot=True,
        fmt=".1f",
        cmap="Blues",
        linewidths=2,
        linecolor="white",
        cbar_kws={"label": "Attrition rate (%)"},
        ax=ax,
    )
    ax.set_title(
        f"Attrition rate (%) by {pivot.index.name} and {pivot.columns.name}"
    )
    ax.set_xlabel(pivot.columns.name)
    ax.set_ylabel(pivot.index.name)
    fig.tight_layout()
    return fig


def plot_income_by_attrition(df):
    """Draw box plots of monthly income for stayers and leavers.

    Parameters
    ----------
    df : pandas.DataFrame
        The employee data, with Attrition and MonthlyIncome columns.

    Returns
    -------
    matplotlib.figure.Figure
        The chart.
    """
    stayers = df.loc[df["Attrition"] == "No", "MonthlyIncome"]
    leavers = df.loc[df["Attrition"] == "Yes", "MonthlyIncome"]

    fig, ax = plt.subplots(figsize=(6, 5))
    boxes = ax.boxplot(
        [stayers, leavers],
        tick_labels=["No", "Yes"],
        patch_artist=True,
        widths=0.5,
        medianprops={"color": "black"},
    )
    for box, colour in zip(boxes["boxes"], [BLUE, ORANGE]):
        box.set_facecolor(colour)

    ax.set_title("Monthly income of stayers and leavers")
    ax.set_xlabel("Left the company")
    ax.set_ylabel("Monthly income")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    return fig