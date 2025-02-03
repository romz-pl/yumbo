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

    # Get schedule for the expert
    schedule = st.session_state.amplsol[f"{expert_name}"].astype("float32")

    # Sum across columns for each date.
    sched_sum = schedule.sum(axis=1)

    # Compute the cumulative sum
    cum = sched_sum.cumsum()

    # Extract start and end dates for each period
    period = st.session_state.mprob["period"]
    starts = period["Start"].values
    ends = period["End"].values

    # Compute the sum for each period using cumulative sums.
    yvalue = cum[ends].values - cum[starts].values + sched_sum.loc[starts].values


    # Get bounds (Lower and Upper) for the given expert in one go
    # Construct a MultiIndex matching (expert_name, period["Name"]) for each period.
    multi_index = pd.MultiIndex.from_arrays(
            [np.repeat(expert_name, len(period)), period["Name"]],
            names=["Expert", "Name"]
        )

    # Reindex pbsum (which has a MultiIndex) to get the bounds for each period.
    # Missing keys will produce NaN; replace them with 0 (as in the original code).
    pbsum = st.session_state.mprob["pbsum"]
    bounds = pbsum.reindex(multi_index)
    ylower = bounds["Lower"].fillna(0).to_numpy()
    yupper = bounds["Upper"].fillna(0).to_numpy()

    # Create the plot
    fig = matplotlib.figure.Figure(
        figsize=(glb.imgw("Width"), glb.imgw("Height")),
        dpi=glb.imgw("Dpi")
    )

    ax = fig.subplots()
    ax.set_ylabel("Hours")
    ax.set_title("Invoicing Periods Workload")
    ax.bar(
        period["Name"],
        yvalue,
        color=glb.imgw("Bar:color"),
    )
    ax.tick_params(axis="x", rotation=0, labelsize="x-small")
    ax.tick_params(axis="y", labelsize="x-small")


    # Create mask for bars with errors
    mask = (yupper - ylower) != 0
    ax.errorbar(x=np.arange(period.shape[0])[mask],
                y=np.array(yvalue)[mask],
                yerr=[(yvalue - ylower)[mask],
                      (yupper - yvalue)[mask]],
                fmt="o",
                color="black",
                capsize=glb.imgw("Bar:capsize"),
                ecolor=glb.imgw("Bar:ecolor"),
                capthick=2)


    return glb.savefig(fig)





