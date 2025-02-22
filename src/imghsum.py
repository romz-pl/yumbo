import matplotlib.figure as matplotlib_figure
import matplotlib.ticker as matplotlib_ticker
import matplotlib.dates as matplotlib_dates
import numpy as np
import pandas as pd
import streamlit as st
import time

import glb

def imghsum_param(col):
    # Yes, "imgh" is used, and not "imghsum"!
    # Summary figures have the same colors as non-summary ones.
    return st.session_state.mprob["imgh"].loc[0, col]

#
# Hours per day (Summary)
#
def plot(days_off):
    time_start = time.perf_counter()

    buf = imghsum(
        st.session_state.git_hash,
        st.session_state.schedule,
        st.session_state.mprob["holiday"],
        days_off,
        glb.img("Start"),
        glb.img("End"),
        glb.img("Width"),
        glb.img("Height"),
        glb.img("Dpi"),
        imghsum_param("Bar:color"),
        imghsum_param("Bar:alpha"),
        imghsum_param("Bar:hatch"),
    )
    st.image(buf)

    time_end = time.perf_counter()
    st.session_state.stats["imghsum:cnt"] += 1
    st.session_state.stats["imghsum:ttime"] += time_end - time_start
    st.session_state.stats["imghsum:nbytes"] += buf.getbuffer().nbytes


@st.cache_resource(max_entries=1000)
def imghsum(
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
        df = schedule.sum(axis=1)
    else:
        # Take only the days that are not public holidays.
        holiday = set(holiday["Date"])
        days = pd.bdate_range(start=start, end=end, freq='C', holidays=holiday)
        # Summing over all the tasks. Choose days that are not public holidays.
        df = schedule.loc[days].sum(axis=1)


    # Create figure and axis.
    fig = matplotlib_figure.Figure(
        figsize=(width, height),
        dpi=dpi
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
        color=bar_color,
        alpha=bar_alpha,
        hatch=bar_hatch,
    )

    idx_size = df.index.shape[0]
    if idx_size > 21 :
        window_size = [7, 15, 21]
        window_color = ["#333333", "#AAAAAA", "#DD0000"]

        for ws, wc in zip(window_size, window_color):
            conv = np.convolve(df.values, np.ones(ws)/ws, mode='valid')
            shift = int(ws/2) # See the documentation of the [np.convolve] function.
            ax.plot(
                df.index[shift : idx_size - shift],
                conv,
                'o-',
                linewidth=1,
                markersize=1,
                color=wc,
                label=f"window size {ws}",
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
