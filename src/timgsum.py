import glb
import matplotlib
import pandas as pd
import streamlit as st
import time


#
# Tasks per day (Summary)
#
def plot():
    # # st.write(st.session_state.mprob["assign"][["Expert", "Task"]])


    # # sum_df = sum(st.session_state.amplsol[(f"{row.Expert}", f"{t}")] for row in st.session_state.mprob["assign"][["Expert", "Task"]])

    # sum_df = sum(
    #     st.session_state.amplsol[(f"{row.Expert}", f"{row.Task}")]
    #     for row in st.session_state.mprob["assign"].itertuples(index=False)
    # )
    # st.write(sum_df)


    # start = st.session_state.mprob["task"]["Start"].min()
    # end = st.session_state.mprob["task"]["End"].max()

    # days = pd.date_range(start=start, end=end, freq='D')

    # # Initialize result DataFrame
    # result = pd.DataFrame(0, index=days, columns=["X"])

    # # Iterate over rows in assign DataFrame
    # for row in st.session_state.mprob["assign"].itertuples(index=False):
    #     # Retrieve the solution DataFrame for the current expert and task
    #     amplsol_series = st.session_state.amplsol[(f"{row.Expert}", f"{row.Task}")]

    #     # # Align amplsol_series with the result DataFrame index and add
    #     #result["X"] = result["X"].add(amplsol_series.reindex(result.index, fill_value=0), fill_value=0)

    #     # Ensure amplsol_series is aligned with result.index
    #     amplsol_series = amplsol_series.reindex(result.index, fill_value=0)
    #     #st.write(amplsol_series, result["X"])
    #     #st.write(type(amplsol_series))

    #     # Add the aligned amplsol_series to result["X"]
    #     result["X"] = result["X"] + amplsol_series["X"]

    # st.write(result)



    time_start = time.perf_counter()

    mm_hash = glb.math_model_hash("timg")
    buf = timgsum( mm_hash)
    st.image(buf)

    time_end = time.perf_counter()
    st.session_state.glb["time:timgsum:cnt"] += 1
    st.session_state.glb["time:timgsum:ttime"] += time_end - time_start
    st.session_state.glb["time:timgsum:nbytes"] += buf.getbuffer().nbytes


@st.cache_resource(max_entries=1000)
def timgsum(mm_hash):

    df = (st.session_state.amplsol > 0).sum(axis=1)

    start = glb.timg("Start")
    end = glb.timg("End")

    # Generate the date range as string
    #days = pd.date_range(start=start, end=end, freq="D")

    # Count the number of tasks per day
    # tasks_per_day = (df[days] > 0).sum()
    #tasks_per_day = df

    # Calculate plot limits
    left = pd.Timestamp(start) - pd.Timedelta(days=1)
    right = pd.Timestamp(end) + pd.Timedelta(days=1)

    # Determine bar width
    width = 0.9 if df.index.size < 10 else 1.0

    # Create figure and axis
    fig = matplotlib.figure.Figure(figsize=(glb.timg("Width"), glb.timg("Height")), dpi=glb.timg("Dpi"))
    ax = fig.subplots()

    # Configure plot properties
    ax.set_title("Tasks per day")
    ax.set_xlim([left, right])
    ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(nbins=6, min_n_ticks=1, integer=True))
    ax.xaxis.set_major_locator(matplotlib.dates.AutoDateLocator(minticks=3, maxticks=6, interval_multiples=True))
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter(glb.format()))
    ax.yaxis.grid(alpha=0.4)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", labelsize="x-small")
    ax.tick_params(axis="y", labelsize="x-small")

    # Add bars to the plot
    ax.bar(
        df.index,
        df.values,
        width,
        color=glb.timg("Bar:color"),
        hatch=glb.timg("Bar:hatch"),
        alpha=glb.timg("Bar:alpha")
    )

    return glb.savefig(fig)
