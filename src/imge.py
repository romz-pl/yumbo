import matplotlib.figure as matplotlib_figure
import matplotlib.ticker as matplotlib_ticker
import matplotlib.dates as matplotlib_dates
import numpy as np
import pandas as pd
import streamlit as st
import time

import glb

#
# Experts per day stacked
#
def plot(task, days_off):
    time_start = time.perf_counter()

    mm_hash = glb.math_model_hash(True)
    buf = imge(task, days_off, mm_hash)
    st.image(buf)

    time_end = time.perf_counter()
    st.session_state.stats["imge:cnt"] += 1
    st.session_state.stats["imge:ttime"] += time_end - time_start
    st.session_state.stats["imge:nbytes"] += buf.getbuffer().nbytes


@st.cache_resource(max_entries=1000)
def imge(task, days_off, mm_hash):

    start = task.Start
    end = task.End

    # Summing over all the experts.
    if days_off:
        df = st.session_state.amplsol.xs(task.Name, level="Task", axis=1, drop_level=False).loc[start : end]
    else:
        # Take only the days that are not public holidays.
        holiday = set(st.session_state.mprob["holiday"]["Date"])
        days = pd.bdate_range(start=start, end=end, freq='C', holidays=holiday)
        df = st.session_state.amplsol.xs(task.Name, level="Task", axis=1, drop_level=False).loc[days]

    # Initialize figure and axis
    fig = matplotlib_figure.Figure(
        figsize=(glb.img("Width"), glb.img("Height")),
        dpi=glb.img("Dpi")
    )
    ax = fig.subplots()
    ax.set_title("Experts per day stacked")

    # Configure axis formatting and grid
    ax.yaxis.grid(alpha=0.4)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", labelsize="x-small")
    ax.tick_params(axis="y", labelsize="x-small")

    # Plot stacked chart
    bottom = np.zeros(df.shape[0])
    for et in df.columns:
        col = df[et]
        if col.sum() > 0:
            ax.fill_between(
                x=df.index,
                y1=bottom,
                y2=col.values + bottom,
                label=et[0],
                step='mid',
                alpha=glb.imge("Bar:alpha"),
            )
            bottom = bottom + col.values

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
