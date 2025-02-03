import glb
import matplotlib
import numpy as np
import pandas as pd
import streamlit as st
import time

#
# Experts per day stacked
#
def plot(task):
    time_start = time.perf_counter()

    mm_hash = glb.math_model_hash("imge")
    buf = imge(task, mm_hash)
    st.image(buf)

    time_end = time.perf_counter()
    st.session_state.glb["time:imge:cnt"] += 1
    st.session_state.glb["time:imge:ttime"] += time_end - time_start
    st.session_state.glb["time:imge:nbytes"] += buf.getbuffer().nbytes


@st.cache_resource(max_entries=1000)
def imge(task, mm_hash):

    # Generate day labels and filter dataframe
    days = pd.date_range(start=task.Start, end=task.End, freq="D")

    # Determine bar width
    width = 0.9 if days.size < 10 else 1.0

    # Define x-axis limits
    left = pd.Timestamp(task.Start) - pd.Timedelta(days=1)
    right = pd.Timestamp(task.End) + pd.Timedelta(days=1)

    # Initialize figure and axis
    fig = matplotlib.figure.Figure(
        figsize=(glb.imge("Width"), glb.imge("Height")),
        dpi=glb.imge("Dpi")
    )
    ax = fig.subplots()
    ax.set_title("Experts per day stacked")
    ax.set_xlim(left, right)

    # Configure axis formatting and grid
    ax.yaxis.grid(alpha=0.4)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", labelsize="x-small")
    ax.tick_params(axis="y", labelsize="x-small")

    expert_schedules = st.session_state.amplsol.xs(
        task.Name, level="Task", axis=1, drop_level=False
    ).loc[days]

    # Plot stacked bar chart
    bottom = np.zeros(days.shape[0])
    for et in expert_schedules.columns:
        col = expert_schedules[et]
        if col.sum() > 0:
            ax.bar(
                days,
                col.values,
                width,
                label=et[0],
                bottom=bottom,
                alpha=glb.imge("Bar:alpha"),
            )
            bottom += col.values

    locator = glb.get_major_tick_locator(ax)
    ax.yaxis.set_major_locator(locator)

    ax.xaxis.set_major_locator(matplotlib.dates.AutoDateLocator(minticks=3, maxticks=6))
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter(glb.format()))

    # Add legend and adjust layout
    ax.legend(loc="upper right", fontsize="6")

    return glb.savefig(fig)
