import matplotlib.figure as matplotlib_figure
import matplotlib.ticker as matplotlib_ticker
import matplotlib.dates as matplotlib_dates
import pandas as pd
import streamlit as st
import time

import glb

#
# Tasks per day (Summary)
#
def plot(days_off):
    time_start = time.perf_counter()

    combi_hash = st.session_state.combi_hash
    buf = imgtsum(days_off, combi_hash)
    st.image(buf)

    time_end = time.perf_counter()
    st.session_state.stats["imgtsum:cnt"] += 1
    st.session_state.stats["imgtsum:ttime"] += time_end - time_start
    st.session_state.stats["imgtsum:nbytes"] += buf.getbuffer().nbytes


@st.cache_resource(max_entries=1000)
def imgtsum(days_off, combi_hash):

    start = glb.img("Start")
    end = glb.img("End")

    if days_off:
        # Summing over all the tasks.
        df = (st.session_state.schedule > 0).sum(axis=1)
    else:
        # Take only the days that are not public holidays.
        holiday = set(st.session_state.mprob["holiday"]["Date"])
        days = pd.bdate_range(start=start, end=end, freq='C', holidays=holiday)
        # Summing over all the tasks. Choose days that are not public holidays.
        df = (st.session_state.schedule.loc[days] > 0).sum(axis=1)

    # Create figure and axis
    fig = matplotlib_figure.Figure(
        figsize=(glb.img("Width"), glb.img("Height")),
        dpi=glb.img("Dpi")
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
