import glb
import matplotlib
import pandas as pd
import streamlit as st
import time


#
# Hours per day
#
def plot(expert_name):
    df = st.session_state.glb[f"schedule {expert_name}"]

    time_start = time.perf_counter()

    mm_hash = glb.math_model_hash("himg")
    buf = himg(df, mm_hash)
    st.image(buf)

    time_end = time.perf_counter()
    st.session_state.glb["time:himg:cnt"] += 1
    st.session_state.glb["time:himg:ttime"] += time_end - time_start
    st.session_state.glb["time:himg:nbytes"] += buf.getbuffer().nbytes


@st.cache_resource(max_entries=1000)
def himg(df, mm_hash):
    start = glb.himg("Start")
    end = glb.himg("End")

    # Generate the date range as string
    days = pd.date_range(start=start, end=end, freq="D")

    # Sum the hours for each day
    hours_per_day = df[days].sum()

    # Calculate plot limits
    left = pd.Timestamp(start) - pd.Timedelta(days=1)
    right = pd.Timestamp(end) + pd.Timedelta(days=1)

    # Determine bar width
    width = 0.9 if days.size < 10 else 1.0

    # Create figure and axis
    fig = matplotlib.figure.Figure(figsize=(glb.himg("Width"), glb.himg("Height")), dpi=glb.himg("Dpi"))
    ax = fig.subplots()

    # Configure plot properties
    ax.set_title("Hours per day")
    ax.set_xlim([left, right])
    ax.yaxis.grid(alpha=0.4)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", labelsize="x-small")
    ax.tick_params(axis="y", labelsize="x-small")

    # Add bars to the plot
    ax.bar(
        days,
        hours_per_day,
        width,
        color=glb.himg("Bar:color"),
        hatch=glb.himg("Bar:hatch"),
        alpha=glb.himg("Bar:alpha")
    )

    step = glb.get_major_tick_step(ax)
    ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(step))
    ax.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%.2f'))

    ax.xaxis.set_major_locator(matplotlib.dates.AutoDateLocator(minticks=3, maxticks=6))
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter(glb.format()))

    return glb.savefig(fig)


