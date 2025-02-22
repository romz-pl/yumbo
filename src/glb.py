import hashlib
import io
import matplotlib.figure as matplotlib_figure
import matplotlib.ticker as matplotlib_ticker
import pandas as pd
import streamlit as st
import subprocess


def format():
    return "%Y-%m-%d"


def img(col):
    return st.session_state.mprob["img"].loc[0, col]

def imgh(col):
    return st.session_state.mprob["imgh"].loc[0, col]

def imgs(col):
    return st.session_state.mprob["imgs"].loc[0, col]

def imgt(col):
    return st.session_state.mprob["imgt"].loc[0, col]

def imgw(col):
    return st.session_state.mprob["imgw"].loc[0, col]

def hours_per_day():
    return st.session_state.mprob["misc"].loc[0, "Hours per day"]

def today():
    return (st.session_state.mprob["misc"].loc[0, "Today"])
    # return data["misc"].at[0, "Today"]

def tomorrow():
    return (today() + pd.Timedelta(1, unit="D"))

def last_day():
    return max(st.session_state.mprob["task"]["End"].max(), st.session_state.mprob["period"]["End"].max())


def get_ampl_model_name():
    return st.session_state.mprob["misc"].iloc[0]["AMPL model"]


def get_ampl_model_file():
    ampl_model = get_ampl_model_name()
    model_file = f"./res/{ampl_model}.ampl"
    return model_file


def is_ampl_model_ubday():
    model = get_ampl_model_name()
    return (model == "solid-ubday" or model == "solid-ubday-overflow")


def is_ampl_model_overflow():
    model = get_ampl_model_name()
    return (model == "solid-overflow" or model == "solid-ubday-overflow")


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


def calc_git_hash():
    return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()


def calc_mm_hash(img_name = None):
    keys = [
        "expert",
        "task",
        "assign",
        "xbday",
        "ubday",
        "ebday",
        "period",
        "pbsum",
        "holiday",
        "misc",
        "img",
    ]

    if img_name is not None:
        keys.append(img_name)


    # Use git_hash to reflect changes to the code.
    git_hash = calc_git_hash()

    # Build input_data by joining the string representations
    input_data = "".join(st.session_state.mprob[k].to_csv() for k in keys)

    # Combine the git hash and the input data, encode, and compute the hash
    combined = git_hash + input_data
    mm_hash = hashlib.blake2s(combined.encode('utf-8')).hexdigest()
    # st.write(mm_hash)

    return mm_hash


@st.cache_data
def convert_df_to_csv(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode("utf-8")
