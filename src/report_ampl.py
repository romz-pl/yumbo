import streamlit as st

import glb

def show_solver_log():
    solver_timestamp = st.session_state.stats["solver_timestamp"]
    st.subheader(f":green[Solver output at {solver_timestamp}]", divider="green")
    st.code(st.session_state.stats["solver_log"])


def show_ampl_data_file():
    st.subheader(":green[AMPL data file]", divider="green")

    data = st.session_state.mprob["ampl_data_file"]
    if len(data) < 10 * 1024:
        # st.code is very slow for large files!!
        # What is better syntax for AML data files?
        language="python"
    else:
        language=None

    st.code(body=data, language=language, line_numbers=True, height=500)



def show_ampl_model_file():
    st.subheader(":green[AMPL model file]", divider="green")

    model_file = glb.get_ampl_model_file()

    with open(model_file, "r") as f:
        buf = f.read()
    st.code(buf)


def show():
    solver_log = st.session_state.show["ampl_solver_log"]
    data_file = st.session_state.show["ampl_data_file"]
    model_file = st.session_state.show["ampl_model_file"]

    if not (solver_log or data_file or model_file):
        return

    st.divider()
    st.header(":blue[AMPL]", divider="blue")

    if solver_log:
        show_solver_log()

    if data_file:
        show_ampl_data_file()

    if model_file:
        show_ampl_model_file()

