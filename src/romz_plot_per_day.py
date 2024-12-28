import io
import streamlit as st
import matplotlib
from matplotlib.figure import Figure
import matplotlib.ticker as tck
import romz_datetime
import datetime

def plot(df, days, data, title, color, hatch, dpi):
    left = romz_datetime.from_string(days[0]) - datetime.timedelta(days=1)
    left = matplotlib.dates.date2num(left)

    right = romz_datetime.from_string(days[-1]) + datetime.timedelta(days=1)
    right = matplotlib.dates.date2num(right)

    days = matplotlib.dates.datestr2num(days)

    width = 1.0
    if days.size < 10:
        width = 0.9

    fig = Figure(figsize=(8, 4))
    ax = fig.subplots()
    ax.set_title(title)
    ax.set_xlim([left, right])

    ax.yaxis.set_major_locator(tck.MaxNLocator(nbins=6, min_n_ticks=1, integer=True))
    ax.xaxis.set_major_locator(matplotlib.dates.AutoDateLocator(tz=None, minticks=3, maxticks=6, interval_multiples=True))
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter(romz_datetime.format()))
    ax.yaxis.grid(alpha=0.4)
    ax.set_axisbelow(True)
    ax.tick_params(axis='x', labelsize='x-small')
    ax.tick_params(axis='y', labelsize='x-small')
    ax.bar(days, data, width, color=color, hatch=hatch, alpha=0.3)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=dpi, pil_kwargs={'compress_level': 1})
    st.image(buf)
    buf.close()
