import streamlit as st


def show_solver_output():
    if st.session_state.glb["show_ampl_solver_log"]:
        st.subheader(f":green[Solver output at {st.session_state.glb['solver timestamp']}]", divider="blue")
        st.code(st.session_state.glb["solver output"])


def show_ampl_data_file():
    if st.session_state.glb["show_ampl_data_file"]:
        st.subheader(f":green[AMPL data file]", divider="blue")
        st.code(st.session_state.glb["ampl_data_file"])


def show():
    show_solver_output()
    show_ampl_data_file()

