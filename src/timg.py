import glb
import io
import matplotlib
import pandas as pd
import streamlit as st
import time

#
# Tasks per day
#
def plot_df(df):
    time_start = time.perf_counter()

    mm_hash = glb.math_model_hash("timg")
    buf = timg(df, mm_hash)
    st.image(buf)

    time_end = time.perf_counter()
    st.session_state.glb["time:timg:cnt"] += 1
    st.session_state.glb["time:timg:val"] += time_end - time_start


@st.cache_resource
def timg(df, mm_hash):
    start = glb.timg("Start")
    end = glb.timg("End")

    # Generate the date range as string
    days = pd.date_range(start=start, end=end, freq="D")

    # Count the number of tasks per day
    tasks_per_day = (df[days] > 0).sum()

    # Calculate plot limits
    left = pd.Timestamp(start) - pd.Timedelta(days=1)
    right = pd.Timestamp(end) + pd.Timedelta(days=1)

    # Determine bar width
    width = 0.9 if days.size < 10 else 1.0

    # Create figure and axis
    fig = matplotlib.figure.Figure(figsize=(glb.timg("Width"), glb.timg("Height")), dpi=glb.timg("Dpi"))
    ax = fig.subplots()

    # Configure plot properties
    ax.set_title("Tasks per day")
    ax.set_xlim([left, right])
    ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(nbins=6, min_n_ticks=1, integer=True))
    ax.xaxis.set_major_locator(matplotlib.dates.AutoDateLocator(minticks=3, maxticks=6, interval_multiples=True))
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter(glb.format()))
    ax.yaxis.grid(alpha=0.4)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", labelsize="x-small")
    ax.tick_params(axis="y", labelsize="x-small")

    # Add bars to the plot
    ax.bar(
        days,
        tasks_per_day,
        width,
        color=glb.timg("Bar:color"),
        hatch=glb.timg("Bar:hatch"),
        alpha=glb.timg("Bar:alpha")
    )

    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="WebP", pil_kwargs={"lossless":True, "quality":70, "method":3} )

    return buf


def plot(expert_name):
    plot_df(st.session_state.glb[f"schedule {expert_name}"])


def plot_summary():
    dfs = (st.session_state.glb[f"schedule {e}"] for e in st.session_state.glb["experts"]["Name"])
    plot_df(sum(dfs))

#
# Is this better, faster??
#
# def plot_summary():
#     # Combine all schedules into a single DataFrame using pd.concat
#     dfs = (st.session_state.glb[f"schedule {e}"] for e in st.session_state.glb["experts"]["Name"])
#     combined_df = pd.concat(dfs, ignore_index=True)
#     plot_df(combined_df)
