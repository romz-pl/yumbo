import matplotlib.figure as matplotlib_figure
import matplotlib.ticker as matplotlib_ticker
import streamlit as st
import time

import glb

#
# Task's Gantt Chart (Summary)
#

def plot():
    time_start = time.perf_counter()

    mm_hash = glb.math_model_hash("imgg")
    buf = imggsum(mm_hash)
    st.image(buf)

    time_end = time.perf_counter()
    st.session_state.stats["imggsum:cnt"] += 1
    st.session_state.stats["imggsum:ttime"] += time_end - time_start
    st.session_state.stats["imggsum:nbytes"] += buf.getbuffer().nbytes


@st.cache_resource(max_entries=1000)
def imggsum(mm_hash):
    df = st.session_state.mprob["task"]

    # Create figure and axis
    fig = matplotlib_figure.Figure(
        figsize=(glb.imgg("Width"), glb.imgg("Height")),
        dpi=2 * glb.imgg("Dpi") # Double DPI for summary image.
    )
    ax = fig.subplots()
    ax.set_title("Task's Gantt Chart")

    # Plot Gantt bars
    ax.barh(
        y=df["Name"],
        width=df["Days"] - 1,
        left=df["Start"],
        color=glb.imgg("Barh:color"),
        height=glb.imgg("Barh:height"),
        alpha=glb.imgg("Barh:alpha"),
    )

    # Configure x-axis
    ax.xaxis.set_major_locator(matplotlib_ticker.MaxNLocator(5, integer=True))
    ax.tick_params(axis="x", rotation=0, labelsize="x-small")
    ax.set_xlim(left=glb.today())

    # Configure y-axis
    ax.yaxis.set_major_locator(matplotlib_ticker.MaxNLocator(5, integer=True))
    ax.tick_params(axis="y", rotation=0, labelsize="x-small")
    ax.yaxis.grid(alpha=0.5)
    ax.set_axisbelow(True)

    # Configure layout
    ax.set_ylim(bottom=-0.6)

    return glb.savefig(fig)
