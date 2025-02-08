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
def plot(expert_name, days_off):

    time_start = time.perf_counter()

    combi_hash = st.session_state.combi_hash
    buf = imgt(expert_name, days_off, combi_hash)
    st.image(buf)

    time_end = time.perf_counter()
    st.session_state.stats["imgt:cnt"] += 1
    st.session_state.stats["imgt:ttime"] += time_end - time_start
    st.session_state.stats["imgt:nbytes"] += buf.getbuffer().nbytes


@st.cache_resource(max_entries=1000)
def imgt(expert_name, days_off, combi_hash):

    start = glb.img("Start")
    end = glb.img("End")

    # Summing over all the tasks.
    if days_off:
        df = (st.session_state.schedule[f"{expert_name}"].loc[start : end] > 0).sum(axis=1)
    else:
        # Take only the days that are not public holidays.
        holiday = set(st.session_state.mprob["holiday"]["Date"])
        days = pd.bdate_range(start=start, end=end, freq='C', holidays=holiday)
        df = (st.session_state.schedule[f"{expert_name}"].loc[days] > 0).sum(axis=1)

    # Create figure and axis
    fig = matplotlib_figure.Figure(
        figsize=(glb.img("Width"), glb.img("Height")),
        dpi=glb.img("Dpi"),
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
        color=glb.imgt("Bar:color"),
        alpha=glb.imgt("Bar:alpha"),
        hatch=glb.imgt("Bar:hatch"),
    )

    # Set the limits.
    ax.set_xlim([start, end])
    ax.set_ylim(bottom=0)

    # Set the ticks.
    ax.yaxis.set_major_locator(matplotlib_ticker.MaxNLocator(nbins=6, min_n_ticks=1, integer=True))
    ax.xaxis.set_major_locator(matplotlib_dates.AutoDateLocator(minticks=3, maxticks=6, interval_multiples=True))
    ax.xaxis.set_major_formatter(matplotlib_dates.DateFormatter(glb.format()))

    return glb.savefig(fig)
