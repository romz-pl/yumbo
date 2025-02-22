import matplotlib.figure as matplotlib_figure
import matplotlib.ticker as matplotlib_ticker
import numpy as np
import pandas as pd
import streamlit as st
import time

import glb

def imgw_param(col):
    return st.session_state.mprob["imgw"].loc[0, col]

#
# Invoicing Periods Workload
#
def plot(expert_name, days_off):
    time_start = time.perf_counter()
    # Convertion from float16 to float32 is required!
    schedule = st.session_state.schedule[expert_name].astype("float32")
    buf = imgw(
        st.session_state.git_hash,
        expert_name,
        schedule,
        st.session_state.mprob["period"],
        st.session_state.mprob["pbsum"],
        days_off,
        glb.img("Width"),
        glb.img("Height"),
        glb.img("Dpi"),
        imgw_param("Bar:color"),
        imgw_param("Bar:capsize"),
        imgw_param("Bar:ecolor"),
    )
    time_end = time.perf_counter()
    st.session_state.stats["imgw:cnt"] += 1
    st.session_state.stats["imgw:ttime"] += time_end - time_start
    st.session_state.stats["imgw:nbytes"] += buf.getbuffer().nbytes

    st.image(buf)


@st.cache_resource(max_entries=1000)
def imgw(
        git_hash,
        expert_name,
        schedule,
        period,
        pbsum,
        days_off,
        width,
        height,
        dpi,
        bar_color,
        bar_capsize,
        bar_ecolor,
    ):

    # Sum across columns for each date and compute its cumulative sum.
    sched_sum = schedule.sum(axis=1)
    cum = sched_sum.cumsum()

    # Extract start and end dates for each period
    starts = period["Start"].to_numpy()
    ends = period["End"].to_numpy()

    # Compute the sum for each period using cumulative sums.
    # Note: cum[ends] and cum[starts] use the index labels from 'starts' and 'ends'
    yvalue = (
        cum[ends].to_numpy() -
        cum[starts].to_numpy() +
        sched_sum.loc[starts].to_numpy()
    )

    # Build a MultiIndex to extract the bounds for the given expert and period names.
    period_names = period["Name"]
    multi_index = pd.MultiIndex.from_arrays(
        [np.repeat(expert_name, len(period_names)), period_names],
        names=["Expert", "Name"]
    )

    # Reindex pbsum with fill_value=0
    bounds = pbsum.reindex(multi_index, fill_value=0)
    ylower = bounds["Lower"].to_numpy()
    yupper = bounds["Upper"].to_numpy()

    # Create the plot
    fig = matplotlib_figure.Figure(
        figsize=(width, height),
        dpi=dpi
    )

    ax = fig.subplots()
    ax.set_ylabel("Hours")
    ax.set_title("Invoicing Periods Workload")
    ax.yaxis.grid(alpha=0.4)
    rects = ax.bar(
        period["Name"],
        yvalue,
        color=bar_color,
    )
    ax.tick_params(axis="x", rotation=0, labelsize="x-small")
    ax.tick_params(axis="y", labelsize="x-small")


    # Create mask for bars with errors
    mask = (yupper - ylower) != 0
    # Create error bars
    ax.errorbar(x=np.arange(period.shape[0])[mask],
                y=np.array(yvalue)[mask],
                yerr=[(yvalue - ylower)[mask],
                      (yupper - yvalue)[mask]],
                fmt="o",
                color="black",
                capsize=bar_capsize,
                ecolor=bar_ecolor,
                capthick=2)

    # Generate labels for the bars
    labels = [
        "{:.0f}".format(v)
        for v in yvalue
    ]

    ax.bar_label(rects, labels=labels, size=8, label_type="edge")

    return glb.savefig(fig)
