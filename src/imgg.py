import matplotlib.figure as matplotlib_figure
import matplotlib.ticker as matplotlib_ticker
import streamlit as st
import time

import glb

def imgg_param(col):
    return st.session_state.mprob["imgg"].loc[0, col]

#
# Task's Gantt Chart
#
def plot(expert_name, days_off):
    time_start = time.perf_counter()
    buf = imgg(
        st.session_state.git_hash,
        st.session_state.mprob["task"],
        st.session_state.mprob["assign"],
        st.session_state.schedule[expert_name],
        expert_name,
        days_off,
        glb.today(),
        glb.img("Width"),
        glb.img("Height"),
        glb.img("Dpi"),
        imgg_param("Barh:color"),
        imgg_param("Barh:height"),
        imgg_param("Barh:alpha"),
    )
    time_end = time.perf_counter()
    st.session_state.stats["imgg:cnt"] += 1
    st.session_state.stats["imgg:ttime"] += time_end - time_start
    st.session_state.stats["imgg:nbytes"] += buf.getbuffer().nbytes

    st.image(buf)


@st.cache_resource(max_entries=1000)
def imgg(
        git_hash,
        task,
        assign,
        schedule,
        expert_name,
        days_off,
        today,
        width,
        height,
        dpi,
        barh_color,
        barh_height,
        barh_alpha,
    ):

    # Extract data from session state
    filter = assign.xs(expert_name, level="Elevel")["Task"]

    # Filter tasks for the expert
    expert_tasks = task.loc[filter]

    # Sum work done for the expert
    work_done = schedule.sum(axis=0)

    # Create the figure and axis
    fig = matplotlib_figure.Figure(
        figsize=(width, height),
        dpi=dpi
    )
    ax = fig.subplots()
    ax.set_title("Task's Gantt Chart")

    # Plot Gantt bars
    rects = ax.barh(
        y=expert_tasks["Name"],
        width=expert_tasks["Days"] - 1,
        left=expert_tasks["Start"],
        color=barh_color,
        height=barh_height,
        alpha=barh_alpha,
    )

    # Generate labels for the bars
    labels = [
        f"{work_done[idx]} of {task.loc[idx, 'Work']}"
        for idx in work_done.index
    ]

    ax.bar_label(rects, labels=labels, size=6, label_type="center")

    # Configure x-axis
    ax.xaxis.set_major_locator(matplotlib_ticker.MaxNLocator(5, integer=True))
    ax.tick_params(axis="x", rotation=0, labelsize="x-small")
    ax.set_xlim(left=today)

    # Configure y-axis
    ax.yaxis.set_major_locator(matplotlib_ticker.MultipleLocator(1))
    ax.tick_params(axis="y", rotation=0, labelsize="x-small")
    ax.yaxis.grid(alpha=0.5)
    ax.set_axisbelow(True)

    # Configure layout
    ax.set_ylim(bottom=-0.6)

    # Save the figure and return
    return glb.savefig(fig)

