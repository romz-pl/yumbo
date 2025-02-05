import matplotlib.figure as matplotlib_figure
import matplotlib.ticker as matplotlib_ticker
import streamlit as st
import time

import glb

#
# Task's Gantt Chart
#
def plot(expert_name, days_off):
    time_start = time.perf_counter()

    mm_hash = glb.math_model_hash("imgg")
    buf = imgg(expert_name, days_off, mm_hash)
    st.image(buf)

    time_end = time.perf_counter()
    st.session_state.stats["imgg:cnt"] += 1
    st.session_state.stats["imgg:ttime"] += time_end - time_start
    st.session_state.stats["imgg:nbytes"] += buf.getbuffer().nbytes


@st.cache_resource(max_entries=1000)
def imgg(expert_name, days_off, mm_hash):
    # Extract data from session state
    task = st.session_state.mprob["task"]
    assign = st.session_state.mprob["assign"]
    filter = assign.xs(expert_name, level="Elevel")["Task"]

    # Filter tasks for the expert
    expert_tasks = task.loc[filter]

    # Sum work done for the expert
    work_done = st.session_state.amplsol[expert_name].sum(axis=0)

    # Create the figure and axis
    fig = matplotlib_figure.Figure(
        figsize=(glb.imgg("Width"), glb.imgg("Height")),
        dpi=glb.imgg("Dpi")
    )
    ax = fig.subplots()
    ax.set_title("Task's Gantt Chart")

    # Plot Gantt bars
    rects = ax.barh(
        y=expert_tasks["Name"],
        width=expert_tasks["Days"] - 1,
        left=expert_tasks["Start"],
        color=glb.imgg("Barh:color"),
        height=glb.imgg("Barh:height"),
        alpha=glb.imgg("Barh:alpha"),
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
    ax.set_xlim(left=glb.today())

    # Configure y-axis
    ax.yaxis.set_major_locator(matplotlib_ticker.MultipleLocator(1))
    ax.tick_params(axis="y", rotation=0, labelsize="x-small")
    ax.yaxis.grid(alpha=0.5)
    ax.set_axisbelow(True)

    # Configure layout
    ax.set_ylim(bottom=-0.6)

    # Save the figure and return
    return glb.savefig(fig)

