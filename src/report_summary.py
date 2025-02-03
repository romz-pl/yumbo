import imggsum
import imghsum
import imgtsum
import streamlit as st
import time


def show_report():
    if not st.session_state.glb["show_experts_summary"]:
        return

    st.divider()

    st.header(":blue[Experts summary]", divider="blue")
    col1, col2, col3 = st.columns(3)
    with col1:
        imggsum.plot()
    with col2:
        imgtsum.plot()
    with col3:
        imghsum.plot()


def show():
    time_start = time.perf_counter()
    show_report()
    time_end = time.perf_counter()
    st.session_state.stats["report_summary:ttime"] += time_end - time_start
