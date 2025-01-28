import datetime
import streamlit as st
import tempfile
import romz_excel


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

def prepare(uploaded_file):

    if 'key:uploaded_file' in st.session_state:
        new_input = ( st.session_state['key:uploaded_file'] != uploaded_file )
    else:
        new_input = True

    if new_input:
        with tempfile.NamedTemporaryFile(suffix=".xlsx") as f:
            f.write(uploaded_file.getvalue())
            f.flush()
            romz_excel.read(f.name)
        st.session_state['key:uploaded_file'] = uploaded_file

    return new_input


def tasks_for_expert(expert_name):
    tasks = st.session_state.glb["tasks"]
    links = st.session_state.glb["links"]

    # Filter the tasks related to the expert
    tasks_for_expert = links[links["Expert"] == expert_name]["Task"]

    # Use .isin() to filter tasks directly
    return tasks[tasks["Name"].isin(tasks_for_expert)]
