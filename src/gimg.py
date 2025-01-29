import glb
import matplotlib
import streamlit as st
import time

#
# Task's Gantt Chart
#
def plot(df, work_done):
    time_start = time.perf_counter()

    mm_hash = glb.math_model_hash("gimg")
    buf = gimg(df, work_done, mm_hash)
    st.image(buf)

    time_end = time.perf_counter()
    st.session_state.glb["time:gimg:cnt"] += 1
    st.session_state.glb["time:gimg:val"] += time_end - time_start


@st.cache_resource
def gimg(df, work_done, mm_hash):


    # Create figure and axis
    fig = matplotlib.figure.Figure(figsize=(glb.gimg("Width"), glb.gimg("Height")), dpi=glb.gimg("Dpi"))
    ax = fig.subplots()
    ax.set_title("Task's Gantt Chart")

    # Plot Gantt bars
    rects = ax.barh(
        y=df["Name"],
        width=df["Days"] - 1,
        left=df["Start"],
        color=glb.gimg("Barh:color"),
        height=glb.gimg("Barh:height"),
        alpha=glb.gimg("Barh:alpha"),
    )

    # Add labels to the bars
    labels = [
        f"{round(done)} of {work}" for work, done in zip(df["Work"].to_numpy(), work_done.to_numpy())
    ]
    ax.bar_label(rects, labels=labels, size=6, label_type="center")

    # Configure x-axis
    ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(5, integer=True))
    ax.tick_params(axis="x", rotation=0, labelsize="x-small")
    ax.set_xlim(left=glb.today())

    # Configure y-axis
    ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(1))
    ax.tick_params(axis="y", rotation=0, labelsize="x-small")
    ax.yaxis.grid(alpha=0.5)
    ax.set_axisbelow(True)

    # Configure layout
    ax.set_ylim(bottom=-0.6)

    return glb.savefig(fig)


