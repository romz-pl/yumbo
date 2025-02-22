import matplotlib.figure as matplotlib_figure
import matplotlib.ticker as matplotlib_ticker
import matplotlib.dates as matplotlib_dates
import pandas as pd
import streamlit as st
import time

import glb

def imgt_param(col):
    return st.session_state.mprob["imgt"].loc[0, col]

#
# Tasks per day
#
def plot(expert_name, days_off):
    time_start = time.perf_counter()

    buf = imgt(
        st.session_state.git_hash,
        st.session_state.schedule[expert_name],
        st.session_state.mprob["holiday"],
        days_off,
        glb.img("Start"),
        glb.img("End"),
        glb.img("Width"),
        glb.img("Height"),
        glb.img("Dpi"),
        imgt_param("Bar:color"),
        imgt_param("Bar:alpha"),
        imgt_param("Bar:hatch"),
    )
    st.image(buf)

    time_end = time.perf_counter()
    st.session_state.stats["imgt:cnt"] += 1
    st.session_state.stats["imgt:ttime"] += time_end - time_start
    st.session_state.stats["imgt:nbytes"] += buf.getbuffer().nbytes


@st.cache_resource(max_entries=1000)
def imgt(
        git_hash,
        schedule,
        holiday,
        days_off,
        start,
        end,
        width,
        height,
        dpi,
        bar_color,
        bar_alpha,
        bar_hatch,
    ):

    if days_off:
        # Summing over all the tasks.
        df = (schedule.loc[start : end] > 0).sum(axis=1)
    else:
        # Summing over all the tasks. Take only the days that are not public holidays.
        holiday = set(holiday["Date"])
        days = pd.bdate_range(start=start, end=end, freq='C', holidays=holiday)
        df = (schedule.loc[days] > 0).sum(axis=1)

    # Create figure and axis
    fig = matplotlib_figure.Figure(
        figsize=(width, height),
        dpi=dpi
    )
    ax = fig.subplots()

    # Configure plot properties
    ax.set_title("Tasks per day")
    ax.yaxis.grid(alpha=0.4)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", labelsize="x-small")
    ax.tick_params(axis="y", labelsize="x-small")

    ax.fill_between(
        x=df.index,
        y1=0,
        y2=df.values,
        step='mid',
        color=bar_color,
        alpha=bar_alpha,
        hatch=bar_hatch,
    )

    # Set the limits.
    ax.set_xlim([start, end])
    ax.set_ylim(bottom=0)

    # Set the ticks.
    ax.yaxis.set_major_locator(matplotlib_ticker.MaxNLocator(nbins=6, min_n_ticks=1, integer=True))
    ax.xaxis.set_major_locator(matplotlib_dates.AutoDateLocator(minticks=3, maxticks=6, interval_multiples=True))
    ax.xaxis.set_major_formatter(matplotlib_dates.DateFormatter(glb.format()))

    return glb.savefig(fig)
