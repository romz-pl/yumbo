import io
import streamlit as st
import matplotlib
from matplotlib.figure import Figure
import matplotlib.ticker as tck
import pandas as pd
import numpy as np
import romz_datetime
import datetime

def plot(df, start_day, end_day, width, dpi):
    if end_day < start_day:
        end_day = start_day

    days = pd.date_range(start=start_day, end=end_day, freq="D").astype("str")
    df = df[days]
    bottom = np.zeros(romz_datetime.length(start_day, end_day))

    left = start_day- datetime.timedelta(days=1)
    left = matplotlib.dates.date2num(left)

    right = end_day + datetime.timedelta(days=1)
    right = matplotlib.dates.date2num(right)

    days = matplotlib.dates.datestr2num(days)

    fig = Figure(figsize=(8, 4))
    ax = fig.subplots()
    ax.set_title('Hours per day stacked')
    ax.set_xlim([left, right])

    ax.yaxis.set_major_locator(tck.MultipleLocator(1))
    #ax.xaxis.set_major_locator(tck.MaxNLocator(nbins=6, min_n_ticks=1, integer=True))
    #ax.xaxis.set_minor_locator(tck.AutoMinorLocator())
    ax.xaxis.set_major_locator(matplotlib.dates.AutoDateLocator(tz=None, minticks=3, maxticks=6, interval_multiples=True))
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter(romz_datetime.format()))
    ax.yaxis.grid(alpha=0.4)
    ax.set_axisbelow(True)
    ax.tick_params(axis='x', labelsize='x-small')
    ax.tick_params(axis='y', labelsize='x-small')

    for idx in df.index:
        task = df.loc[idx]
        if task.sum() > 0:
            ax.bar(days, task, width, label="{name}".format(name=task.name), bottom=bottom, alpha=0.6)
            bottom += task

    ax.legend(loc="upper right", fontsize="6")
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=dpi, pil_kwargs={'compress_level': 1})
    st.image(buf)
    buf.close()

