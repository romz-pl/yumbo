import pandas as pd
import io
import streamlit as st
import matplotlib
from matplotlib.figure import Figure
import matplotlib.ticker as tck
import romz_datetime
import glb
import time

#
# Hours per day
#

def plot_df(df):
    start = glb.himg("Start")
    end = glb.himg("End")

    # Generate the date range as string
    days = pd.date_range(start=start, end=end, freq="D")

    # Sum the hours for each day
    hours_per_day = df[days].sum()

    # Calculate plot limits
    left = pd.Timestamp(start) - pd.Timedelta(days=1)
    right = pd.Timestamp(end) + pd.Timedelta(days=1)

    # Determine bar width
    width = 0.9 if days.size < 10 else 1.0

    # Create figure and axis
    fig = Figure(figsize=(glb.himg("Width"), glb.himg("Height")))
    ax = fig.subplots()

    # Configure plot properties
    ax.set_title("Hours per day")
    ax.set_xlim([left, right])
    ax.yaxis.set_major_locator(tck.MaxNLocator(nbins=6, min_n_ticks=1))
    ax.xaxis.set_major_locator(matplotlib.dates.AutoDateLocator(minticks=3, maxticks=6, interval_multiples=True))
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter(romz_datetime.format()))
    ax.yaxis.grid(alpha=0.4)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", labelsize="x-small")
    ax.tick_params(axis="y", labelsize="x-small")

    # Add bars to the plot
    ax.bar(
        days,
        hours_per_day,
        width,
        color=glb.himg("Bar:color"),
        hatch=glb.himg("Bar:hatch"),
        alpha=glb.himg("Bar:alpha")
    )

    # Finalize and save the plot
    fig.tight_layout()
    with io.BytesIO() as buf:
        fig.savefig(buf, format="png", dpi=glb.himg("Dpi"), pil_kwargs={"compress_level": 1})
        buf.seek(0)
        st.image(buf)


def plot(expert_name):
    time_start = time.perf_counter()

    plot_df(glb.data[f"schedule {expert_name}"])

    time_end = time.perf_counter()
    glb.data["time:himg:cnt"] += 1
    glb.data["time:himg:val"] += time_end - time_start


def plot_summary():
    dfs = (glb.data[f"schedule {e}"] for e in glb.data["experts"]["Name"])
    plot_df(sum(dfs))

