import io
import streamlit as st
from matplotlib.figure import Figure
import matplotlib.ticker as tck
import pandas as pd


def plot(invper, schedule, bounds, dpi):
    if bounds.empty:
        st.write(":green[No limits have been set for the invoicing periods.]")
        return

    # Calculate workload for each period
    y = []
    for k in bounds.index:
        period_name = bounds.at[k, "Period"]
        period_data = invper[invper["Name"] == period_name]
        start, end = period_data["Start day"].iat[0], period_data["End day"].iat[0]
        x_task = pd.date_range(start=start, end=end, freq="D").astype("str").intersection(schedule.columns)
        y.append(schedule.loc[:, x_task].sum().sum())

    y = pd.Series(y)
    ylower = bounds["Lower"].to_numpy()
    yupper = bounds["Upper"].to_numpy()
    yerr = [y - ylower, yupper - y]

    # Create the plot
    fig = Figure(figsize=(8, 4))
    ax = fig.subplots()
    ax.set_ylabel("Hours")
    ax.set_title("Invoicing Periods Workload")
    ax.bar(
        bounds["Period"],
        y,
        yerr=yerr,
        color="#7BC8F6",
        ecolor="tab:red",
        capsize=4,
    )
    ax.tick_params(axis="x", rotation=0, labelsize="x-small")
    ax.tick_params(axis="y", labelsize="x-small")

    # Finalize and display the plot
    fig.tight_layout()
    with io.BytesIO() as buf:
        fig.savefig(buf, format="png", dpi=dpi, pil_kwargs={"compress_level": 1})
        buf.seek(0)
        st.image(buf)
