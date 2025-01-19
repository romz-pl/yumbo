import io
import streamlit as st
from matplotlib.figure import Figure
import matplotlib.ticker as tck


def plot(data):
    # Extract dataframe
    df = data["invoicing periods"]

    # Create figure and axis
    fig = Figure(figsize=(8, 4))
    ax = fig.subplots()

    # Plot horizontal bars
    rects = ax.barh(
        y=df["Name"],
        width=df["Days"],
        left=df["Start"],
        height=1.0,
        color="tab:green",
        alpha=0.5,
    )

    # Add labels to bars
    ax.bar_label(rects, label_type="center")

    # Add vertical lines for end days
    ax.vlines(
        df["End"],
        ymin=-0.5,
        ymax=len(df["Name"]) - 0.5,
        linestyles="dashed",
        color="tab:green",
    )

    # Format the x-axis
    ax.xaxis_date()
    ax.set_title("Invoicing Periods Gantt Chart")
    ax.set_xticks(df["End"])
    ax.xaxis.set_minor_locator(tck.MultipleLocator(5))
    ax.tick_params(axis="x", rotation=90, labelsize="small")

    # Format the y-axis
    ax.set_ylim(bottom=-0.5, top=len(df["Name"]) - 0.5)
    ax.yaxis.grid(True, alpha=0.5)
    ax.tick_params(axis="y", labelsize="small")

    # Adjust layout
    fig.tight_layout()

    # Save the figure to a buffer and display
    with io.BytesIO() as buf:
        fig.savefig(buf, format="png", dpi=150, pil_kwargs={"compress_level": 1})
        buf.seek(0)
        st.image(buf)

