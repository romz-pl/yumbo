import io
import streamlit as st
from matplotlib.figure import Figure
import matplotlib.ticker as tck
import matplotlib.artist
import numpy as np
import streamlit as st
import glb



def plot_summary():

    df = glb.data["tasks"]
    # Create figure and axis
    fig = Figure(figsize=(glb.gimg("Width"), glb.gimg("Height")))
    ax = fig.subplots()
    ax.set_title("Task's Gantt Chart")

    # Plot Gantt bars
    ax.barh(
        y=df["Name"],
        width=df["Days"] - 1,
        left=df["Start"],
        color=glb.gimg("Barh:color"),
        height=glb.gimg("Barh:height"),
        alpha=glb.gimg("Barh:alpha"),
    )

    # Configure x-axis
    ax.xaxis.set_major_locator(tck.MaxNLocator(5, integer=True))
    ax.tick_params(axis="x", rotation=0, labelsize="x-small")
    ax.set_xlim(left=np.datetime64(glb.today()))

    # Configure y-axis
    ax.yaxis.set_major_locator(tck.MaxNLocator(5, integer=True))
    ax.tick_params(axis="y", rotation=0, labelsize="x-small")
    ax.yaxis.grid(alpha=0.5)
    ax.set_axisbelow(True)

    # Configure layout
    ax.set_ylim(bottom=-0.6)
    fig.tight_layout()

    # Save the figure to a buffer and display
    with io.BytesIO() as buf:
        fig.savefig(buf, format="png", dpi=glb.gimg("Dpi"), pil_kwargs={"compress_level": 1})
        buf.seek(0)
        st.image(buf)


def plot(df, work_done):
    # Create figure and axis
    fig = Figure(figsize=(glb.gimg("Width"), glb.gimg("Height")))
    ax = fig.subplots()
    ax.set_title("Task's Gantt Chart")

    # Plot Gantt bars
    rects = ax.barh(
        y=df["Name"],
        width=df["Days"] - 1,
        left=df["Start"],
        color=glb.gimg("Barh:color"),
        height=glb.gimg("Barh:height"),
        alpha=glb.gimg("Barh:alpha"),
    )

    # Add labels to the bars
    labels = [
        f"{round(done)} of {work}" for work, done in zip(df["Work"].to_numpy(), work_done.to_numpy())
    ]
    ax.bar_label(rects, labels=labels, size=6, label_type="center")

    # Configure x-axis
    ax.xaxis.set_major_locator(tck.MaxNLocator(5, integer=True))
    ax.tick_params(axis="x", rotation=0, labelsize="x-small")
    ax.set_xlim(left=np.datetime64(glb.today()))

    # Configure y-axis
    ax.yaxis.set_major_locator(tck.MultipleLocator(1))
    ax.tick_params(axis="y", rotation=0, labelsize="x-small")
    ax.yaxis.grid(alpha=0.5)
    ax.set_axisbelow(True)

    # Configure layout
    ax.set_ylim(bottom=-0.6)
    fig.tight_layout()

    # Save the figure to a buffer and display
    with io.BytesIO() as buf:
        fig.savefig(buf, format="png", dpi=glb.gimg("Dpi"), pil_kwargs={"compress_level": 1})
        buf.seek(0)
        st.image(buf)

