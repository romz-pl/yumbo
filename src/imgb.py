import matplotlib.figure as matplotlib_figure
import matplotlib.ticker as matplotlib_ticker
import pandas as pd
import streamlit as st
import time

import glb

def imgb_param(col):
    return st.session_state.mprob["imgb"].loc[0, col]


#
# Plot task with its XBDAY constrains
#
def plot(task, schedule, bounds):
    time_start = time.perf_counter()
    buf = imgb(
        st.session_state.git_hash,
        task,
        schedule,
        bounds,
        glb.img("Width"),
        glb.img("Height"),
        glb.img("Dpi"),
        imgb_param("Plot:format"),
        imgb_param("Plot:markeredgewidth"),
        imgb_param("Step:linewidth"),
        imgb_param("Fill:color"),
        imgb_param("Fill:hatch"),
        imgb_param("Fill:alpha"),
    )
    time_end = time.perf_counter()
    st.session_state.stats["imgb:cnt"] += 1
    st.session_state.stats["imgb:ttime"] += time_end - time_start
    st.session_state.stats["imgb:nbytes"] += buf.getbuffer().nbytes

    st.image(buf)


@st.cache_resource(max_entries=1000)
def imgb(
        git_hash,
        task,
        schedule,
        bounds,
        width,
        height,
        dpi,
        plot_format,
        plot_markeredgewidth,
        step_linewidth,
        fill_color,
        fill_hatch,
        fill_alpha,
    ):

    # Generate task-specific data
    x_task = pd.date_range(start=task.Start, end=task.End, freq="D")
    y_task = schedule.loc[x_task, task.Name]

    # Create figure and axis
    fig = matplotlib_figure.Figure(
        figsize=(width, height),
        dpi=dpi
    )

    ax = fig.subplots()

    # Plot task data
    ax.plot(
        x_task,
        y_task,
        plot_format + "-",
        drawstyle='steps-mid',
        markeredgewidth=plot_markeredgewidth,
        linewidth=step_linewidth,
        label=f"Task {task.Name}"
    )

    # Configure grid
    ax.yaxis.grid(alpha=0.5)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", labelsize="x-small")
    ax.tick_params(axis="y", labelsize="x-small")

    # Add task bounds
    for row in bounds.itertuples(index=False):
        bound_days = pd.date_range(start=row.Start, end=row.End, freq="D")

        delta = 0.1 if row.Lower == row.Upper else 0

        ax.fill_between(
            bound_days,
            row.Lower - delta,
            row.Upper + delta,
            color=fill_color,
            hatch=fill_hatch,
            alpha=fill_alpha
        )

    # Set the limits.
    ax.set_xlim([x_task[0], x_task[-1]])

    # Add legend and finalize layout
    ax.legend(loc="upper right")

    # Configure axis properties
    ax.xaxis.set_major_locator(matplotlib_ticker.MaxNLocator(5, integer=True))
    ax.xaxis.set_minor_locator(matplotlib_ticker.AutoMinorLocator())

    locator = glb.get_major_tick_locator(ax)
    ax.yaxis.set_major_locator(locator)

    return glb.savefig(fig)
