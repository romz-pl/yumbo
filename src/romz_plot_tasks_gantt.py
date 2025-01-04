import io
import streamlit as st
from matplotlib.figure import Figure
import matplotlib.ticker as tck
import matplotlib.artist


def plot_summary(df, dpi):
    fig = Figure(figsize=(8, 4))
    ax = fig.subplots()
    ax.set_title("Task's Gantt chart")

    rects = ax.barh(y=df["Name"], width=df["Days"]-1, left=df["Start day"], color='tab:orange', height=0.9, alpha=0.6)

    # ax.bar_label(rects, labels=df["Name"], size=6, label_type='center')

    ax.xaxis.set_major_locator(tck.MaxNLocator(5, integer=True))
    ax.yaxis.set_major_locator(tck.MaxNLocator(5, integer=True))
    # ax.set_xticks(df["End day"])
    # ax.xaxis.set_minor_locator(tck.AutoMinorLocator())
    ax.tick_params(axis='x', rotation=0, labelsize='x-small')
    ax.tick_params(axis='y', rotation=0, labelsize='x-small')
    ax.yaxis.grid()
    ax.set_axisbelow(True)
    ax.set_ylim(bottom=-0.6)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=dpi, pil_kwargs={'compress_level': 1})
    st.image(buf)
    buf.close()


def plot(df, work_done, dpi):
    fig = Figure(figsize=(8, 4))
    ax = fig.subplots()
    ax.set_title("Task's Gantt chart")

    rects = ax.barh(y=df["Name"], width=df["Days"]-1, left=df["Start day"], color='tab:orange', height=0.9, alpha=0.6)

    ll = ["%d of %d" % (d, w) for w, d in zip(df["Work"].to_numpy(), work_done.to_numpy()) ]
    ax.bar_label(rects, labels=ll, size=6, label_type='center')
    # ax.vlines(df["End day"], -0.6, df["Name"], linestyles='dashed', color="tab:orange")

    ax.xaxis.set_major_locator(tck.MaxNLocator(5, integer=True))
    ax.yaxis.set_major_locator(tck.MultipleLocator(1))
    # ax.xaxis.set_minor_locator(tck.AutoMinorLocator())
    # ax.set_xticks(df["End day"])
    ax.tick_params(axis='x', rotation=0, labelsize='x-small')
    ax.tick_params(axis='y', rotation=0, labelsize='x-small')
    # matplotlib.artist.setp(ax.get_yticklabels(), rotation=20, ha='center', rotation_mode='anchor')
    ax.yaxis.grid()
    ax.set_axisbelow(True)
    ax.set_ylim(bottom=-0.6)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=dpi, pil_kwargs={'compress_level': 1})
    st.image(buf)
    buf.close()
