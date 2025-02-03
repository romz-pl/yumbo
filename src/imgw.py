import glb
import matplotlib
import numpy as np
import pandas as pd
import streamlit as st
import time

#
# Invoicing Periods Workload
#
def plot(expert_name):
    time_start = time.perf_counter()

    mm_hash = glb.math_model_hash("imgw")
    buf = imgw(expert_name, mm_hash)
    st.image(buf)

    time_end = time.perf_counter()
    st.session_state.glb["time:imgw:cnt"] += 1
    st.session_state.glb["time:imgw:ttime"] += time_end - time_start
    st.session_state.glb["time:imgw:nbytes"] += buf.getbuffer().nbytes


@st.cache_resource(max_entries=1000)
def imgw(expert_name, mm_hash):
    period = st.session_state.mprob["period"]
    schedule = st.session_state.amplsol[f"{expert_name}"]
    pbsum = st.session_state.mprob["pbsum"]

    # Filter the bounds for the given expert
    bounds = pbsum[ pbsum["Expert"] == expert_name ]
    assert bounds["Lower"].dtype == bounds["Upper"].dtype
    dtype = bounds["Lower"].dtype

    if bounds.empty:
        st.write(":green[No limits have been set for the invoicing periods.]")
        return

    # Precompute invoicing period start and end as a dictionary for quick lookup
    period_dict = period.set_index("Name")[["Start", "End"]].to_dict("index")

    # Calculate workload for each period
    y = np.empty(bounds.shape[0], dtype=dtype)
    for idx, p in enumerate(bounds["Period"]):
        period_data = period_dict[p]
        start = pd.Timestamp(period_data["Start"])
        end = pd.Timestamp(period_data["End"])
        x_task = pd.date_range(start=start, end=end, freq="D").intersection(schedule.index)
        y[idx] = schedule.loc[x_task].sum().sum()

    ylower = bounds["Lower"].to_numpy(dtype=dtype)
    yupper = bounds["Upper"].to_numpy(dtype=dtype)
    yerr = np.array([y - ylower, yupper - y], dtype=dtype)

    # Create the plot
    fig = matplotlib.figure.Figure(figsize=(glb.imgw("Width"), glb.imgw("Height")), dpi=glb.imgw("Dpi"))
    ax = fig.subplots()
    ax.set_ylabel("Hours")
    ax.set_title("Invoicing Periods Workload")
    ax.bar(
        bounds["Period"],
        y,
        yerr=yerr,
        color=glb.imgw("Bar:color"),
        ecolor=glb.imgw("Bar:ecolor"),
        capsize=glb.imgw("Bar:capsize"),
    )
    ax.tick_params(axis="x", rotation=0, labelsize="x-small")
    ax.tick_params(axis="y", labelsize="x-small")

    return glb.savefig(fig)


