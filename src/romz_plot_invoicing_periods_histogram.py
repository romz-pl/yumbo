import io
import streamlit as st
from matplotlib.figure import Figure
import matplotlib.ticker as tck
import pandas as pd

def plot(invper, schedule, bounds, dpi):
    if bounds.empty:
        st.write(":green[No limits have been set for the invoicing periods.]")
        return

    y = pd.Series(range(len(bounds.index)))
    for k in bounds.index:
        period_name = bounds.at[k, "Period"]
        start = invper[invper["Name"] == period_name]["Start day"].iat[0]
        end = invper[invper["Name"] == period_name]["End day"].iat[0]
        x_task = pd.date_range(start=start, end=end, freq="D").astype("str").intersection(schedule.columns)
        y[k] = schedule.loc[:, x_task].sum().sum()

    ylower = bounds["Lower"].to_numpy()
    yupper = bounds["Upper"].to_numpy()
    yerr = [[0],[0]]
    yerr[0] = y - ylower
    yerr[1] = yupper - y

    fig = Figure(figsize=(8, 4))
    ax = fig.subplots()
    ax.set_ylabel('Hours')
    ax.set_title('Invoicing periods workload')
    ax.bar(bounds["Period"], y, yerr=yerr, color='#7BC8F6', ecolor='tab:red', capsize=4)
    ax.tick_params(axis='x', rotation=0, labelsize='x-small')
    ax.tick_params(axis='y', labelsize='x-small')

    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=dpi, pil_kwargs={'compress_level': 1})
    st.image(buf)
    buf.close()
