import io
import streamlit as st
from matplotlib.figure import Figure
import matplotlib.ticker as tck
import romz_datetime
import pandas as pd
import glb

def bimg(col):
    return glb.data["bimg"].iloc[0][col]

def plot(task, schedule, bounds):
    # Generate task-specific data
    x_task = pd.date_range(start=task.Start, end=task.End, freq="D")
    y_task = schedule.loc[task.Name, x_task.strftime(romz_datetime.format())]

    # Create figure and axis
    fig = Figure(figsize=(bimg("Width"), bimg("Height")))
    ax = fig.subplots()

    # Plot task data
    ax.plot(x_task, y_task, bimg("Plot:format"), markeredgewidth=bimg("Plot:markeredgewidth"), label=f"Task {task.Name}")
    ax.step(x_task, y_task, linewidth=bimg("Step:linewidth"), where="mid")

    # Configure grid and axis properties
    ax.xaxis.set_major_locator(tck.MaxNLocator(5, integer=True))
    ax.xaxis.set_minor_locator(tck.AutoMinorLocator())
    ax.yaxis.set_major_locator(tck.MaxNLocator(5))
    ax.yaxis.grid(alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_xlim([x_task[0], x_task[-1]])
    ax.tick_params(axis="x", labelsize="x-small")
    ax.tick_params(axis="y", labelsize="x-small")

    # Add task bounds
    for _, row in bounds.iterrows():
        bound_days = pd.date_range(start=row["Start"], end=row["End"], freq="D")
        lower, upper = row["Lower"], row["Upper"]
        if lower == upper:
            lower -= 0.5
            upper += 0.5
        ax.fill_between(bound_days, lower, upper, color=bimg("Fill:color"), hatch=bimg("Fill:hatch"), alpha=bimg("Fill:alpha"))

    # Add legend and finalize layout
    ax.legend(loc="upper right")
    fig.tight_layout()

    # Save and display the plot
    with io.BytesIO() as buf:
        fig.savefig(buf, format="png", dpi=bimg("Dpi"), pil_kwargs={"compress_level": 1})
        buf.seek(0)
        st.image(buf)
