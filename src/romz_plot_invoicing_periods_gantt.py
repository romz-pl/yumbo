import io
import streamlit as st
from matplotlib.figure import Figure
import matplotlib.ticker as tck


def plot(data):
    df = data["invoicing periods"]
    fig = Figure(figsize=(8, 4))
    ax = fig.subplots()
    rects = plt.barh(y=df["Name"], width=df["Days"], left=df["Start day"], height=1.0, color="tab:green", alpha=0.5)
    ax.bar_label(rects, label_type='center')
    ax.vlines(df["End day"], 0, df["Name"], linestyles='dashed', color="tab:green")
    ax.xaxis_date()
    ax.set_title("Invoicing periods Gantt chart")
    ax.yaxis.grid(True, alpha=0.5)
    ax.set_ylim(bottom=0)
    ax.set_xticks(df["End day"])
    ax.xaxis.set_minor_locator(tck.MultipleLocator(5))
    ax.tick_params(axis='y', labelsize='small')
    ax.tick_params(axis='x', rotation=90, labelsize='small')

    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, pil_kwargs={'compress_level': 1})
    st.image(buf)
    buf.close()
