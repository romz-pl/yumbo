import matplotlib.figure as matplotlib_figure
import matplotlib.ticker as matplotlib_ticker
import matplotlib.dates as matplotlib_dates
import pandas as pd
import streamlit as st
import time

import glb

#
# Hours per day
#
def plot(expert_name, days_off):
    time_start = time.perf_counter()

    mm_hash = glb.math_model_hash("imgh")
    buf = imgh(expert_name, days_off, mm_hash)
    st.image(buf)

    time_end = time.perf_counter()
    st.session_state.stats["imgh:cnt"] += 1
    st.session_state.stats["imgh:ttime"] += time_end - time_start
    st.session_state.stats["imgh:nbytes"] += buf.getbuffer().nbytes


@st.cache_resource(max_entries=1000)
def imgh(expert_name, days_off, mm_hash):

    start = glb.imgh("Start")
    end = glb.imgh("End")

    # Summing over all the tasks.
    if days_off:
        df = st.session_state.amplsol[f"{expert_name}"].loc[start : end].sum(axis=1)
    else:
        # Take only the days that are not public holidays.
        holiday = set(st.session_state.mprob["holiday"]["Date"])
        days = pd.bdate_range(start=start, end=end, freq='C', holidays=holiday)
        df = st.session_state.amplsol[f"{expert_name}"].loc[days].sum(axis=1)


    # Create figure and axis.
    fig = matplotlib_figure.Figure(
        figsize=(glb.imgh("Width"), glb.imgh("Height")),
        dpi=glb.imgh("Dpi"),
    )
    ax = fig.subplots()

    # Configure plot properties.
    ax.set_title("Hours per day")
    ax.yaxis.grid(alpha=0.4)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", labelsize="x-small")
    ax.tick_params(axis="y", labelsize="x-small")

    ax.fill_between(
        x=df.index,
        y1=0,
        y2=df.values,
        step='mid',
        color=glb.imgh("Bar:color"),
        alpha=glb.imgh("Bar:alpha"),
        hatch=glb.imgh("Bar:hatch"),
    )

    # Set the limits.
    ax.set_xlim([start, end])
    ax.set_ylim(bottom=0)

    # Set the ticks.
    locator = glb.get_major_tick_locator(ax)
    ax.yaxis.set_major_locator(locator)
    ax.xaxis.set_major_locator(matplotlib_dates.AutoDateLocator(minticks=3, maxticks=6))
    ax.xaxis.set_major_formatter(matplotlib_dates.DateFormatter(glb.format()))

    return glb.savefig(fig)
