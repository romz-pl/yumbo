import glb
import io
import matplotlib
import streamlit as st
import time


#
# Task's Gantt Chart (Summary)
#

def plot():
    time_start = time.perf_counter()

    mm_hash = glb.math_model_hash("gimg")
    buf = gimgsum(mm_hash)
    st.image(buf)

    time_end = time.perf_counter()
    st.session_state.glb["time:gimgsum:cnt"] += 1
    st.session_state.glb["time:gimgsum:val"] += time_end - time_start


@st.cache_resource
def gimgsum(mm_hash):
    df = st.session_state.glb["tasks"]
    # Create figure and axis
    fig = matplotlib.figure.Figure(figsize=(glb.gimg("Width"), glb.gimg("Height")), dpi=glb.gimg("Dpi"))
    ax = fig.subplots()
    ax.set_title("Task's Gantt Chart")

    # Plot Gantt bars
    ax.barh(
        y=df["Name"],
        width=df["Days"] - 1,
        left=df["Start"],
        color=glb.gimg("Barh:color"),
        height=glb.gimg("Barh:height"),
        alpha=glb.gimg("Barh:alpha"),
    )

    # Configure x-axis
    ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(5, integer=True))
    ax.tick_params(axis="x", rotation=0, labelsize="x-small")
    ax.set_xlim(left=glb.today())

    # Configure y-axis
    ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(5, integer=True))
    ax.tick_params(axis="y", rotation=0, labelsize="x-small")
    ax.yaxis.grid(alpha=0.5)
    ax.set_axisbelow(True)

    # Configure layout
    ax.set_ylim(bottom=-0.6)

    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="WebP", pil_kwargs={"lossless":True, "quality":70, "method":3} )

    return buf
