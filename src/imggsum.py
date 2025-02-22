import matplotlib.figure as matplotlib_figure
import matplotlib.ticker as matplotlib_ticker
import streamlit as st
import time

import glb

def imggsum_param(col):
    # Yes, "imgg" is used, and not "imggsum"!
    # Summary figures have the same colors as non-summary ones.
    return st.session_state.mprob["imgg"].loc[0, col]

#
# Task's Gantt Chart (Summary)
#

def plot(days_off):
    time_start = time.perf_counter()
    buf = imggsum(
        st.session_state.git_hash,
        st.session_state.mprob["task"],
        glb.today(),
        glb.img("Width"),
        glb.img("Height"),
        glb.img("Dpi"),
        imggsum_param("Barh:color"),
        imggsum_param("Barh:height"),
        imggsum_param("Barh:alpha"),
    )
    time_end = time.perf_counter()
    st.session_state.stats["imggsum:cnt"] += 1
    st.session_state.stats["imggsum:ttime"] += time_end - time_start
    st.session_state.stats["imggsum:nbytes"] += buf.getbuffer().nbytes

    st.image(buf)


@st.cache_resource(max_entries=1000)
def imggsum(
        git_hash,
        df,
        today,
        width,
        height,
        dpi,
        barh_color,
        barh_height,
        barh_alpha,
        ):

    # Create figure and axis
    fig = matplotlib_figure.Figure(
        figsize=(width, height),
        dpi=dpi
    )
    ax = fig.subplots()
    ax.set_title("Task's Gantt Chart")

    # Plot Gantt bars
    ax.barh(
        y=df["Name"],
        width=df["Days"] - 1,
        left=df["Start"],
        color=barh_color,
        height=barh_height,
        alpha=barh_alpha,
    )

    # Configure x-axis
    ax.xaxis.set_major_locator(matplotlib_ticker.MaxNLocator(5, integer=True))
    ax.tick_params(axis="x", rotation=0, labelsize="x-small")
    ax.set_xlim(left=today)

    # Configure y-axis
    ax.yaxis.set_major_locator(matplotlib_ticker.MaxNLocator(5, integer=True))
    ax.tick_params(axis="y", rotation=0, labelsize="x-small")
    ax.yaxis.grid(alpha=0.5)
    ax.set_axisbelow(True)

    # Configure layout
    ax.set_ylim(bottom=-0.6)

    return glb.savefig(fig)
