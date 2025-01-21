import datetime
import streamlit as st
import tempfile
import romz_excel

data = dict()

def himg(col):
    return data["himg"].iloc[0][col]

def timg(col):
    return data["timg"].iloc[0][col]

def simg(col):
    return data["simg"].iloc[0][col]

def wimg(col):
    return data["wimg"].iloc[0][col]

def bimg(col):
    return data["bimg"].iloc[0][col]

def gimg(col):
    return data["gimg"].iloc[0][col]

def hours_per_day():
    return data["misc"].iloc[0]["Hours per day"]

def today():
    return (data["misc"].iloc[0]["Today"])
    # return data["misc"].at[0, "Today"]

def tomorrow():
    return (today() + datetime.timedelta(days=1))

def last_day():
    return max(data["tasks"]["End"].max(), data["invoicing periods"]["End"].max())

def prepare(uploaded_file):
    global data

    if 'key:uploaded_file' in st.session_state:
        new_input = ( st.session_state['key:uploaded_file'] != uploaded_file )
    else:
        new_input = True

    if new_input:
        with tempfile.NamedTemporaryFile(suffix=".xlsx") as f:
            f.write(uploaded_file.getvalue())
            f.flush()
            romz_excel.read(f.name)
        st.session_state['key:glb.data'] = data
        st.session_state['key:uploaded_file'] = uploaded_file
    else:
        data = st.session_state['key:glb.data']

    return new_input


def tasks_for_expert(expert_name):
    tasks = data["tasks"]
    links = data["links"]

    # Filter the tasks related to the expert
    tasks_for_expert = links[links["Expert"] == expert_name]["Task"]

    # Use .isin() to filter tasks directly
    return tasks[tasks["Name"].isin(tasks_for_expert)]
