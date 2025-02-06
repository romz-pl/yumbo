import streamlit as st
import time

import imggsum
import imghsum
import imgtsum

def show_report():
    if not st.session_state.show["experts_summary"]:
        return

    st.divider()

    days_off = st.session_state.glb["days_off"]
    st.header(":blue[Experts summary]", divider="blue")
    col1, col2, col3 = st.columns(3)
    with col1:
        imggsum.plot()
    with col2:
        imgtsum.plot(days_off)
    with col3:
        imghsum.plot(days_off)


def show():
    time_start = time.perf_counter()
    show_report()
    time_end = time.perf_counter()
    st.session_state.stats["report_summary:ttime"] += time_end - time_start
