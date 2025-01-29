import glb
import matplotlib
import numpy as np
import pandas as pd
import streamlit as st
import time

#
# Hours per day stacked
#
def plot(expert_name):
    time_start = time.perf_counter()

    mm_hash = glb.math_model_hash("simg")
    buf = simg(expert_name, mm_hash)
    st.image(buf)

    time_end = time.perf_counter()
    st.session_state.glb["time:simg:cnt"] += 1
    st.session_state.glb["time:simg:ttime"] += time_end - time_start
    st.session_state.glb["time:simg:nbytes"] += buf.getbuffer().nbytes




@st.cache_resource(max_entries=1000)
def simg(expert_name, mm_hash):
    start = glb.simg("Start")
    end = glb.simg("End")

    # Generate day labels and filter dataframe
    days = pd.date_range(start=start, end=end, freq="D")
    df = st.session_state.glb[f"schedule {expert_name}"][days]

    # Determine bar width
    width = 0.9 if days.size < 10 else 1.0

    # Define x-axis limits
    left = pd.Timestamp(start) - pd.Timedelta(days=1)
    right = pd.Timestamp(end) + pd.Timedelta(days=1)

    # Initialize figure and axis
    fig = matplotlib.figure.Figure(figsize=(glb.simg("Width"), glb.simg("Height")), dpi=glb.simg("Dpi"))
    ax = fig.subplots()
    ax.set_title("Hours per day stacked")
    ax.set_xlim([left, right])

    # Configure axis formatting and grid


    ax.yaxis.grid(alpha=0.4)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", labelsize="x-small")
    ax.tick_params(axis="y", labelsize="x-small")

    # Filter out zero-sum tasks efficiently
    mask = df.sum(axis=1) > 0
    filtered_df = df[mask]

    # Plot stacked bar chart
    bottom = np.zeros(days.shape[0])
    for task_name, task_data in filtered_df.iterrows():
        ax.bar(
            days,
            task_data,
            width,
            label=task_name,
            bottom=bottom,
            alpha=glb.simg("Bar:alpha"),
        )
        bottom = bottom + task_data

    locator = glb.get_major_tick_locator(ax)
    ax.yaxis.set_major_locator(locator)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%.2f'))

    ax.xaxis.set_major_locator(matplotlib.dates.AutoDateLocator(minticks=3, maxticks=6))
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter(glb.format()))

    # Add legend and adjust layout
    ax.legend(loc="upper right", fontsize="6")

    return glb.savefig(fig)



