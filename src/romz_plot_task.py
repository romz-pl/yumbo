import io
import streamlit as st
from matplotlib.figure import Figure
import matplotlib.ticker as tck
import pandas as pd


def plot(task, schedule, bounds, dpi):
    x_task = pd.date_range(start=task["Start day"], end=task["End day"], freq="D")
    y_task = schedule.loc[task["Name"], x_task.astype("str")]

    fig = Figure(figsize=(8, 4))
    ax = fig.subplots()
    ax.plot(x_task, y_task, 'o', markeredgewidth=1.5)
    ax.xaxis.set_major_locator(tck.MaxNLocator(5, integer=True))
    ax.xaxis.set_minor_locator(tck.AutoMinorLocator())
    ax.step(x_task, y_task, linewidth=0.5, where='mid')
    ax.legend(['Task {id}'.format(id=task["Name"])], loc="upper right")
    ax.yaxis.grid(alpha=0.5)
    ax.set_axisbelow(True)
    ax.yaxis.set_major_locator(tck.MultipleLocator(1))
    ax.set_ylim([-0.2, 8])

    for idx in bounds.index:
        start = bounds.at[idx,"Start day"]
        end = bounds.at[idx,"End day"]
        bound_days = pd.date_range(start=start, end=end, freq="D")
        lower = bounds.at[idx,"Lower"].astype(int)
        upper = bounds.at[idx,"Upper"].astype(int)
        if lower == upper:
            lower -= 0.5
            upper += 0.5
        ax.fill_between(bound_days, lower, upper, hatch='/', alpha=0.2, color='#90EE90')

    ax.set_xlim([x_task[0], x_task[-1]])
    ax.tick_params(axis='x', labelsize='x-small')
    ax.tick_params(axis='y', labelsize='x-small')
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=dpi, pil_kwargs={'compress_level': 1})
    st.image(buf)
    buf.close()
