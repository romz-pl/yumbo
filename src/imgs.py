import matplotlib.figure as matplotlib_figure
import matplotlib.ticker as matplotlib_ticker
import matplotlib.dates as matplotlib_dates
import numpy as np
import pandas as pd
import streamlit as st
import time

import glb

def imgs_param(col):
    return st.session_state.mprob["imgs"].loc[0, col]

#
# Hours per day stacked
#
def plot(expert_name, days_off):
    time_start = time.perf_counter()

    buf = imgs(
        st.session_state.git_hash,
        st.session_state.schedule[expert_name],
        days_off,
        glb.img("Start"),
        glb.img("End"),
        glb.img("Width"),
        glb.img("Height"),
        glb.img("Dpi"),
        imgs_param("Bar:alpha")
    )
    st.image(buf)

    time_end = time.perf_counter()
    st.session_state.stats["imgs:cnt"] += 1
    st.session_state.stats["imgs:ttime"] += time_end - time_start
    st.session_state.stats["imgs:nbytes"] += buf.getbuffer().nbytes


@st.cache_resource(max_entries=1000)
def imgs(
        git_hash,
        schedule,
        days_off,
        start,
        end,
        width,
        height,
        dpi,
        bar_alpha,
    ):

    if days_off:
        # Filter dataframe.
        df = schedule.loc[start : end]
    else:
        # Take only the days that are not public holidays.
        holiday = set(st.session_state.mprob["holiday"]["Date"])
        days = pd.bdate_range(start=start, end=end, freq='C', holidays=holiday)
        df = schedule.loc[days]

    # Initialize figure and axis
    fig = matplotlib_figure.Figure(
        figsize=(width, height),
        dpi=dpi
    )

    ax = fig.subplots()
    ax.set_title("Hours per day stacked")

    # Configure axis formatting and grid
    ax.yaxis.grid(alpha=0.4)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", labelsize="x-small")
    ax.tick_params(axis="y", labelsize="x-small")

    # Filter out zero-sum tasks efficiently
    df = df.loc[:, df.sum() > 0]

    # Plot stacked chart
    bottom = np.zeros(df.index.shape[0])
    for task_name in df.columns:
        task_data = df[task_name].values
        ax.fill_between(
            x=df.index,
            y1=bottom,
            y2=task_data + bottom,
            label=task_name,
            step='mid',
            alpha=bar_alpha,
        )
        bottom = bottom + task_data

    # Set the limits.
    ax.set_xlim([start, end])
    ax.set_ylim(bottom=0)

    locator = glb.get_major_tick_locator(ax)
    ax.yaxis.set_major_locator(locator)

    ax.xaxis.set_major_locator(matplotlib_dates.AutoDateLocator(minticks=3, maxticks=6))
    ax.xaxis.set_major_formatter(matplotlib_dates.DateFormatter(glb.format()))

    # Add legend and adjust layout
    ax.legend(loc="upper right", fontsize="6")

    return glb.savefig(fig)
