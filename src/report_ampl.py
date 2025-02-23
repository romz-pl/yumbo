import streamlit as st

import glb

def show_solver_log():
    st.subheader(f":green[Solver log]", divider="green")

    st.code(
        st.session_state.stats["solver_log"],
        line_numbers=True,
        height=500
    )


def show_ampl_data_file():
    st.subheader(":green[AMPL data file]", divider="green")

    data = st.session_state.mprob["ampl_data_file"]
    if len(data) < 10 * 1024:
        # The st.code widget is very slow for large files with syntax highliting!
        # What is a better syntax highlighting language for AMPL files?
        language="python"
    else:
        language=None

    st.code(body=data, language=language, line_numbers=True, height=500)



def show_ampl_model_file():
    st.subheader(":green[AMPL model file]", divider="green")

    model_file = glb.get_ampl_model_file()

    with open(model_file, "r") as f:
        buf = f.read()
    st.code(buf, line_numbers=True, height=500)


def show():
    solver_log = st.session_state.show["ampl_solver_log"]
    data_file = st.session_state.show["ampl_data_file"]
    model_file = st.session_state.show["ampl_model_file"]

    if not (solver_log or data_file or model_file):
        return

    st.divider()
    st.header(":material/calculate: :blue[AMPL]", divider="blue")

    if solver_log:
        show_solver_log()

    if data_file:
        show_ampl_data_file()

    if model_file:
        show_ampl_model_file()

