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

def plot(expert_name):
    start = glb.simg("Start")
    end = glb.simg("End")

    # Generate day labels and filter dataframe
    days = pd.date_range(start=start, end=end, freq="D")
    day_labels = matplotlib.dates.date2num(days)
    df = glb.data[f"schedule {expert_name}"][days.astype("str")]

    # Determine bar width
    width = 0.9 if days.size < 10 else 1.0

    # Define x-axis limits
    left = matplotlib.dates.date2num(start - datetime.timedelta(days=1))
    right = matplotlib.dates.date2num(end + datetime.timedelta(days=1))

    # Initialize figure and axis
    fig = Figure(figsize=(glb.simg("Width"), glb.simg("Height")))
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

    # Filter out zero-sum tasks efficiently
    mask = df.sum(axis=1) > 0
    filtered_df = df[mask]

    # Plot stacked bar chart
    bottom = np.zeros(len(days))
    for task_name, task_data in filtered_df.iterrows():
        ax.bar(
            day_labels,
            task_data,
            width,
            label=task_name,
            bottom=bottom,
            alpha=glb.simg("Bar:alpha"),
        )
        bottom = bottom + task_data

    # Add legend and adjust layout
    ax.legend(loc="upper right", fontsize="6")
    fig.tight_layout()

    # Save the figure to a buffer
    with io.BytesIO() as buf:
        fig.savefig(buf, format="png", dpi=glb.simg("Dpi"), pil_kwargs={"compress_level": 1})
        buf.seek(0)
        st.image(buf)


