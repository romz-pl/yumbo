import matplotlib.figure as matplotlib_figure
import matplotlib.ticker as matplotlib_ticker
import matplotlib.dates as matplotlib_dates
import pandas as pd
import streamlit as st
import time

import glb

#
# Tasks per day
#
def plot(expert_name):

    time_start = time.perf_counter()

    mm_hash = glb.math_model_hash("imgt")
    buf = imgt(expert_name, mm_hash)
    st.image(buf)

    time_end = time.perf_counter()
    st.session_state.stats["imgt:cnt"] += 1
    st.session_state.stats["imgt:ttime"] += time_end - time_start
    st.session_state.stats["imgt:nbytes"] += buf.getbuffer().nbytes


@st.cache_resource(max_entries=1000)
def imgt(expert_name, mm_hash):
    df = (st.session_state.amplsol[f"{expert_name}"] > 0).sum(axis=1)

    start = glb.imgt("Start")
    end = glb.imgt("End")

    # Calculate plot limits
    left = pd.Timestamp(start) - pd.Timedelta(days=1)
    right = pd.Timestamp(end) + pd.Timedelta(days=1)

    # Determine bar width
    width = 0.9 if df.index.size < 10 else 1.0

    # Create figure and axis
    fig = matplotlib_figure.Figure(figsize=(glb.imgt("Width"), glb.imgt("Height")), dpi=glb.imgt("Dpi"))
    ax = fig.subplots()

    # Configure plot properties
    ax.set_title("Tasks per day")
    ax.set_xlim([left, right])
    ax.yaxis.set_major_locator(matplotlib_ticker.MaxNLocator(nbins=6, min_n_ticks=1, integer=True))
    ax.xaxis.set_major_locator(matplotlib_dates.AutoDateLocator(minticks=3, maxticks=6, interval_multiples=True))
    ax.xaxis.set_major_formatter(matplotlib_dates.DateFormatter(glb.format()))
    ax.yaxis.grid(alpha=0.4)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", labelsize="x-small")
    ax.tick_params(axis="y", labelsize="x-small")

    # Add bars to the plot
    ax.bar(
        df.index,
        df.values,
        width,
        color=glb.imgt("Bar:color"),
        hatch=glb.imgt("Bar:hatch"),
        alpha=glb.imgt("Bar:alpha")
    )

    return glb.savefig(fig)
