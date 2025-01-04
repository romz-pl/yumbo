import io
import streamlit as st
from matplotlib.figure import Figure
import matplotlib.ticker as tck
import romz_datetime
import pandas as pd


def plot(task, schedule, bounds, dpi):
    # Generate task-specific data
    x_task = pd.date_range(start=task["Start day"], end=task["End day"], freq="D")
    y_task = schedule.loc[task["Name"], x_task.strftime(romz_datetime.format())]

    # Create figure and axis
    fig = Figure(figsize=(8, 4))
    ax = fig.subplots()

    # Plot task data
    ax.plot(x_task, y_task, "o", markeredgewidth=1.5, label=f"Task {task['Name']}")
    ax.step(x_task, y_task, linewidth=0.5, where="mid")

    # Configure grid and axis properties
    ax.xaxis.set_major_locator(tck.MaxNLocator(5, integer=True))
    ax.xaxis.set_minor_locator(tck.AutoMinorLocator())
    ax.yaxis.set_major_locator(tck.MultipleLocator(1))
    ax.yaxis.grid(alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_xlim([x_task[0], x_task[-1]])
    ax.set_ylim([-0.2, 8])
    ax.tick_params(axis="x", labelsize="x-small")
    ax.tick_params(axis="y", labelsize="x-small")

    # Add task bounds
    for _, row in bounds.iterrows():
        bound_days = pd.date_range(start=row["Start day"], end=row["End day"], freq="D")
        lower, upper = int(row["Lower"]), int(row["Upper"])
        if lower == upper:
            lower -= 0.5
            upper += 0.5
        ax.fill_between(bound_days, lower, upper, hatch="/", alpha=0.2, color="#90EE90")

    # Add legend and finalize layout
    ax.legend(loc="upper right")
    fig.tight_layout()

    # Save and display the plot
    with io.BytesIO() as buf:
        fig.savefig(buf, format="png", dpi=dpi, pil_kwargs={"compress_level": 1})
        buf.seek(0)
        st.image(buf)
