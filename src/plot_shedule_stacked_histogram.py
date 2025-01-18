import io
import streamlit as st
import matplotlib
from matplotlib.figure import Figure
import matplotlib.ticker as tck
import pandas as pd
import numpy as np
import romz_datetime
import datetime
import glb

def plot(df, start_day, end_day, width):
    if end_day < start_day:
        end_day = start_day

    # Generate day labels and filter dataframe
    days = pd.date_range(start=start_day, end=end_day, freq="D")
    day_labels = matplotlib.dates.date2num(days)
    df = df[days.astype("str")]

    # Define x-axis limits
    left = matplotlib.dates.date2num(start_day - datetime.timedelta(days=1))
    right = matplotlib.dates.date2num(end_day + datetime.timedelta(days=1))

    # Initialize figure and axis
    fig = Figure(figsize=(8, 4))
    ax = fig.subplots()
    ax.set_title("Hours per day stacked")
    ax.set_xlim([left, right])

    # Configure axis formatting and grid
    ax.yaxis.set_major_locator(tck.MultipleLocator(1))
    ax.xaxis.set_major_locator(
        matplotlib.dates.AutoDateLocator(
            tz=None, minticks=3, maxticks=6, interval_multiples=True
        )
    )
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter(romz_datetime.format()))
    ax.yaxis.grid(alpha=0.4)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", labelsize="x-small")
    ax.tick_params(axis="y", labelsize="x-small")

    # Plot stacked bar chart
    bottom = np.zeros(len(days))
    for idx, task in df.iterrows():
        if task.sum() > 0:
            ax.bar(
                day_labels,
                task,
                width,
                label=task.name,
                bottom=bottom,
                alpha=0.6,
            )
            bottom += task

    # Add legend and adjust layout
    ax.legend(loc="upper right", fontsize="6")
    fig.tight_layout()

    # Save the figure to a buffer
    with io.BytesIO() as buf:
        fig.savefig(buf, format="png", dpi=glb.dpi(), pil_kwargs={"compress_level": 1})
        buf.seek(0)
        st.image(buf)


