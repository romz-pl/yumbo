import pandas as pd
import io
import streamlit as st
import matplotlib
from matplotlib.figure import Figure
import matplotlib.ticker as tck
import romz_datetime
import datetime
import glb
import time

#
# Tasks per day
#

def plot_df(df):


    start = glb.timg("Start")
    end = glb.timg("End")

    # Generate the date range as string
    days = pd.period_range(start=start, end=end, freq="D").astype(str)

    # Count the number of tasks per day
    tasks_per_day = (df[days] > 0).sum()

    # Calculate plot limits
    left = matplotlib.dates.date2num(start - datetime.timedelta(days=1))
    right = matplotlib.dates.date2num(end + datetime.timedelta(days=1))
    days = matplotlib.dates.datestr2num(days)

    # Determine bar width
    width = 0.9 if days.size < 10 else 1.0

    # Create figure and axis
    fig = Figure(figsize=(glb.timg("Width"), glb.timg("Height")))
    ax = fig.subplots()

    # Configure plot properties
    ax.set_title("Tasks per day")
    ax.set_xlim([left, right])
    ax.yaxis.set_major_locator(tck.MaxNLocator(nbins=6, min_n_ticks=1, integer=True))
    ax.xaxis.set_major_locator(matplotlib.dates.AutoDateLocator(minticks=3, maxticks=6, interval_multiples=True))
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter(romz_datetime.format()))
    ax.yaxis.grid(alpha=0.4)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", labelsize="x-small")
    ax.tick_params(axis="y", labelsize="x-small")

    # Add bars to the plot
    ax.bar(days, tasks_per_day, width, color=glb.timg("Bar:color"), hatch=glb.timg("Bar:hatch"), alpha=glb.timg("Bar:alpha"))

    # Finalize and save the plot
    fig.tight_layout()
    with io.BytesIO() as buf:
        fig.savefig(buf, format="png", dpi=glb.timg("Dpi"), pil_kwargs={"compress_level": 1})
        buf.seek(0)
        st.image(buf)


def plot(expert_name):
    time_start = time.perf_counter()

    plot_df(glb.data[f"schedule {expert_name}"])

    time_end = time.perf_counter()
    glb.data["time:timg:cnt"] += 1
    glb.data["time:timg:val"] += time_end - time_start


def plot_summary():
    dfs = (glb.data[f"schedule {e}"] for e in glb.data["experts"]["Name"])
    plot_df(sum(dfs))

#
# Is this better, faster??
#
# def plot_summary():
#     # Combine all schedules into a single DataFrame using pd.concat
#     dfs = (glb.data[f"schedule {e}"] for e in glb.data["experts"]["Name"])
#     combined_df = pd.concat(dfs, ignore_index=True)
#     plot_df(combined_df)
