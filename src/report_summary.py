import streamlit as st
import time

import glb
import imggsum
import imghsum
import imgtsum

def show_report():
    if not st.session_state.show["experts_summary"]:
        return

    st.divider()

    days_off = st.session_state.show["days_off"]
    st.header(":blue[Experts summary]", divider="blue")
    col1, col2, col3 = st.columns(3)
    with col1:
        imggsum.plot()
    with col2:
        imgtsum.plot(days_off)
    with col3:
        imghsum.plot(days_off)

    if glb.is_ampl_model_overflow():
        overflow = st.session_state.overflow
        if overflow.sum() > 0:
            st.subheader(":red[There are task overflows!]", divider="red")
            df = overflow[ overflow > 0]
            st.write(df)


def show():
    time_start = time.perf_counter()
    show_report()
    time_end = time.perf_counter()
    st.session_state.stats["report_summary:ttime"] += time_end - time_start
