import hashlib
import io
import matplotlib.figure as matplotlib_figure
import matplotlib.ticker as matplotlib_ticker
import pandas as pd
import streamlit as st


def format():
    return "%Y-%m-%d"



def imgb(col):
    return st.session_state.mprob["imgb"].iloc[0][col]

def imge(col):
    return st.session_state.mprob["imge"].iloc[0][col]

def imgg(col):
    return st.session_state.mprob["imgg"].iloc[0][col]

def imgh(col):
    return st.session_state.mprob["imgh"].iloc[0][col]

def imgs(col):
    return st.session_state.mprob["imgs"].iloc[0][col]

def imgt(col):
    return st.session_state.mprob["imgt"].iloc[0][col]

def imgw(col):
    return st.session_state.mprob["imgw"].iloc[0][col]





def hours_per_day():
    return st.session_state.mprob["misc"].iloc[0]["Hours per day"]

def today():
    return (st.session_state.mprob["misc"].iloc[0]["Today"])
    # return data["misc"].at[0, "Today"]

def tomorrow():
    return (today() + pd.Timedelta(1, unit="D"))

def last_day():
    return max(st.session_state.mprob["task"]["End"].max(), st.session_state.mprob["period"]["End"].max())


def math_model_hash(img):
    keys = [
        "expert",
        "task",
        "assign",
        "xbday",
        # "ubday",
        "ebday",
        "period",
        "pbsum",
        "holiday",
        "misc",
    ]

    if img != None:
        keys.append(img)

    # Create the input tuple
    input_data = tuple(st.session_state.mprob[k] for k in keys)

    buf = io.StringIO()
    buf.write(str(input_data))
    mm_hash = hashlib.blake2s(buf.getvalue().encode('utf-8')).hexdigest()
    buf.close()
    return mm_hash


def savefig(fig):
    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="WebP", pil_kwargs={"lossless":True, "quality":70, "method":3} )
    # fig.savefig(buf, format="png", pil_kwargs={"compress_level": 9})

    return buf



def get_major_tick_locator(ax):
    # Get the current y-axis limits
    y_min, y_max = ax.get_ylim()
    y_range = y_max - y_min

    # Determine locator based on the range
    if y_range <= 2:
        locator = matplotlib_ticker.MultipleLocator(0.25)
    elif y_range <= 5:
        locator = matplotlib_ticker.MultipleLocator(0.5)
    else:
        locator = matplotlib_ticker.MaxNLocator(steps=[1, 2, 5], integer=True)

    return locator
