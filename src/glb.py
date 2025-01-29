import datetime
import hashlib
import io
import pickle
import streamlit as st


def format():
    return "%Y-%m-%d"

def himg(col):
    return st.session_state.glb["himg"].iloc[0][col]

def timg(col):
    return st.session_state.glb["timg"].iloc[0][col]

def simg(col):
    return st.session_state.glb["simg"].iloc[0][col]

def wimg(col):
    return st.session_state.glb["wimg"].iloc[0][col]

def bimg(col):
    return st.session_state.glb["bimg"].iloc[0][col]

def gimg(col):
    return st.session_state.glb["gimg"].iloc[0][col]

def hours_per_day():
    return st.session_state.glb["misc"].iloc[0]["Hours per day"]

def today():
    return (st.session_state.glb["misc"].iloc[0]["Today"])
    # return data["misc"].at[0, "Today"]

def tomorrow():
    return (today() + datetime.timedelta(days=1))

def last_day():
    return max(st.session_state.glb["tasks"]["End"].max(), st.session_state.glb["invoicing periods"]["End"].max())


def math_model_hash(img):
    data = st.session_state.glb

    keys = [
        "experts",
        "tasks",
        "links",
        "xbday",
        "xbsum",
        "ubday",
        "ubsum",
        "expert bounds",
        "invoicing periods",
        "invoicing periods bounds",
        "public holidays",
        "misc",
        img,
    ]

    # Create the input tuple
    input_data = tuple(data[k] for k in keys)

    # Serialize and hash the input data
    pickled = pickle.dumps(input_data)
    return hashlib.blake2s(pickled).hexdigest()


def savefig(fig):
    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="WebP", pil_kwargs={"lossless":True, "quality":70, "method":3} )
    # fig.savefig(buf, format="png", pil_kwargs={"compress_level": 9})

    return buf
