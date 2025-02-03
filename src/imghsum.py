import matplotlib
import pandas as pd
import streamlit as st
import time

import glb

#
# Hours per day (Summary)
#
def plot():
    time_start = time.perf_counter()

    mm_hash = glb.math_model_hash("imgh")
    buf = imghsum(mm_hash)
    st.image(buf)

    time_end = time.perf_counter()
    st.session_state.stats["imghsum:cnt"] += 1
    st.session_state.stats["imghsum:ttime"] += time_end - time_start
    st.session_state.stats["imghsum:nbytes"] += buf.getbuffer().nbytes


@st.cache_resource(max_entries=1000)
def imghsum(mm_hash):
    df = st.session_state.amplsol.sum(axis=1)

    start = glb.imgh("Start")
    end = glb.imgh("End")

    # Calculate plot limits
    left = pd.Timestamp(start) - pd.Timedelta(days=1)
    right = pd.Timestamp(end) + pd.Timedelta(days=1)

    # Determine bar width
    width = 0.9 if df.index.size < 10 else 1.0

    # Create figure and axis
    fig = matplotlib.figure.Figure(figsize=(glb.imgh("Width"), glb.imgh("Height")), dpi=glb.imgh("Dpi"))
    ax = fig.subplots()

    # Configure plot properties
    ax.set_title("Hours per day")
    ax.set_xlim([left, right])

    ax.yaxis.grid(alpha=0.4)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", labelsize="x-small")
    ax.tick_params(axis="y", labelsize="x-small")

    # Add bars to the plot
    ax.bar(
        df.index,
        df.values,
        width,
        color=glb.imgh("Bar:color"),
        hatch=glb.imgh("Bar:hatch"),
        alpha=glb.imgh("Bar:alpha")
    )

    locator = glb.get_major_tick_locator(ax)
    ax.yaxis.set_major_locator(locator)

    ax.xaxis.set_major_locator(matplotlib.dates.AutoDateLocator(minticks=3, maxticks=6))
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter(glb.format()))

    return glb.savefig(fig)
