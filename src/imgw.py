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

    yvalue = np.empty(period.shape[0])
    ylower = np.zeros(period.shape[0])
    yupper = np.zeros(period.shape[0])
    for idx, row in enumerate(period.itertuples(index=False)):
        x_task = pd.date_range(start=row.Start, end=row.End, freq="D").intersection(schedule.index)
        yvalue[idx] = schedule.loc[x_task].sum().sum()

        if (expert_name, row.Name) in pbsum.index:
            ylower[idx] = pbsum.loc[(expert_name, row.Name)]["Lower"]
            yupper[idx] = pbsum.loc[(expert_name, row.Name)]["Upper"]


    # Create the plot
    fig = matplotlib.figure.Figure(figsize=(glb.imgw("Width"), glb.imgw("Height")), dpi=glb.imgw("Dpi"))
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
    mask = np.array(yupper - ylower) != 0
    ax.errorbar(x=np.arange(period.shape[0])[mask],
                y=np.array(yvalue)[mask],
                yerr=[np.array(yvalue - ylower)[mask],
                      np.array(yupper - yvalue)[mask]],
                fmt="o",
                color="black",
                capsize=glb.imgw("Bar:capsize"),
                ecolor=glb.imgw("Bar:ecolor"),
                capthick=2)


    return glb.savefig(fig)





