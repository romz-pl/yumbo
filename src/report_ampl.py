import streamlit as st


def show_solver_output():
    st.subheader(f":green[Solver output at {st.session_state.glb['solver timestamp']}]", divider="green")
    st.code(st.session_state.glb["solver output"])


def show_ampl_data_file():
    st.subheader(f":green[AMPL data file]", divider="green")
    st.code(st.session_state.glb["ampl_data_file"])


def show():
    solver_log = st.session_state.glb["show_ampl_solver_log"]
    data_file = st.session_state.glb["show_ampl_data_file"]

    if not (solver_log or data_file):
        return

    st.divider()
    st.header(":blue[AMPL]", divider="blue")

    if solver_log:
        show_solver_output()

    if data_file:
        show_ampl_data_file()

