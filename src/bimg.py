import glb
import matplotlib
import pandas as pd
import streamlit as st
import time


#
# Plot task with its constrains
#
def plot(task, schedule, bounds):
    time_start = time.perf_counter()

    mm_hash = glb.math_model_hash("bimg")
    buf = bimg(task, schedule, bounds, mm_hash)
    st.image(buf)

    time_end = time.perf_counter()
    st.session_state.glb["time:bimg:cnt"] += 1
    st.session_state.glb["time:bimg:ttime"] += time_end - time_start
    st.session_state.glb["time:bimg:nbytes"] += buf.getbuffer().nbytes


@st.cache_resource(max_entries=1000)
def bimg(task, schedule, bounds, mm_hash):
    # Generate task-specific data
    x_task = pd.date_range(start=task.Start, end=task.End, freq="D")
    y_task = schedule.loc[x_task, task.Name]

    # Create figure and axis
    fig = matplotlib.figure.Figure(figsize=(glb.bimg("Width"), glb.bimg("Height")), dpi=glb.bimg("Dpi"))
    ax = fig.subplots()

    # Plot task data
    ax.plot(x_task, y_task, glb.bimg("Plot:format"), markeredgewidth=glb.bimg("Plot:markeredgewidth"), label=f"Task {task.Name}")
    ax.step(x_task, y_task, linewidth=glb.bimg("Step:linewidth"), where="mid")

    # Configure grid
    ax.yaxis.grid(alpha=0.5)
    ax.set_axisbelow(True)
    ax.set_xlim([x_task[0], x_task[-1]])
    ax.tick_params(axis="x", labelsize="x-small")
    ax.tick_params(axis="y", labelsize="x-small")

    # Add task bounds
    for row in bounds.itertuples(index=False):
        bound_days = pd.date_range(start=row.Start, end=row.End, freq="D")

        delta = 0.1 if row.Lower == row.Upper else 0

        ax.fill_between(bound_days,
                        row.Lower - delta,
                        row.Upper + delta,
                        color=glb.bimg("Fill:color"),
                        hatch=glb.bimg("Fill:hatch"),
                        alpha=glb.bimg("Fill:alpha")
                        )

    # Add legend and finalize layout
    ax.legend(loc="upper right")

    # Configure axis properties
    ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(5, integer=True))
    ax.xaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator())

    locator = glb.get_major_tick_locator(ax)
    ax.yaxis.set_major_locator(locator)

    return glb.savefig(fig)
