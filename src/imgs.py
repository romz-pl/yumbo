import matplotlib.figure as matplotlib_figure
import matplotlib.ticker as matplotlib_ticker
import matplotlib.dates as matplotlib_dates
import numpy as np
import pandas as pd
import streamlit as st
import time

import glb

#
# Hours per day stacked
#
def plot(expert_name):
    time_start = time.perf_counter()

    mm_hash = glb.math_model_hash("imgs")
    buf = imgs(expert_name, mm_hash)
    st.image(buf)

    time_end = time.perf_counter()
    st.session_state.stats["imgs:cnt"] += 1
    st.session_state.stats["imgs:ttime"] += time_end - time_start
    st.session_state.stats["imgs:nbytes"] += buf.getbuffer().nbytes


@st.cache_resource(max_entries=1000)
def imgs(expert_name, mm_hash):
    start = glb.imgs("Start")
    end = glb.imgs("End")

    # Generate day labels and filter dataframe
    days = pd.date_range(start=start, end=end, freq="D")
    df = st.session_state.amplsol[f"{expert_name}"].loc[days]

    # Determine bar width
    width = 0.9 if days.size < 10 else 1.0

    # Define x-axis limits
    left = pd.Timestamp(start) - pd.Timedelta(days=1)
    right = pd.Timestamp(end) + pd.Timedelta(days=1)

    # Initialize figure and axis
    fig = matplotlib_figure.Figure(figsize=(glb.imgs("Width"), glb.imgs("Height")), dpi=glb.imgs("Dpi"))
    ax = fig.subplots()
    ax.set_title("Hours per day stacked")
    ax.set_xlim([left, right])

    # Configure axis formatting and grid
    ax.yaxis.grid(alpha=0.4)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", labelsize="x-small")
    ax.tick_params(axis="y", labelsize="x-small")

    # Filter out zero-sum tasks efficiently
    df = df.loc[:, df.sum() > 0]

    # Plot stacked bar chart
    bottom = np.zeros(df.index.shape[0])
    for task_name in df.columns:
        task_data = df[task_name].values
        ax.bar(
            df.index,
            task_data,
            width,
            label=task_name,
            bottom=bottom,
            alpha=glb.imgs("Bar:alpha"),
        )
        bottom = bottom + task_data

    locator = glb.get_major_tick_locator(ax)
    ax.yaxis.set_major_locator(locator)

    ax.xaxis.set_major_locator(matplotlib_dates.AutoDateLocator(minticks=3, maxticks=6))
    ax.xaxis.set_major_formatter(matplotlib_dates.DateFormatter(glb.format()))

    # Add legend and adjust layout
    ax.legend(loc="upper right", fontsize="6")

    return glb.savefig(fig)
