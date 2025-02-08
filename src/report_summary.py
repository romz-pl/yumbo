import streamlit as st
import time

import glb
import imggsum
import imghsum
import imgtsum

def show_report():
    show = st.session_state.show

    # Extract relevant values from the session state
    b_list = [
        show["summary_tasks_gantt_chart"],
        show["summary_tasks_per_day"],
        show["summary_hours_per_day"],
    ]

    func_list = [imggsum.plot, imgtsum.plot, imghsum.plot]

    # Return early if no charts are to be shown
    if not any(b_list):
        return

    st.divider()

    days_off = show["days_off"]
    st.header(":blue[Summary]", divider="blue")

    if show["summary_charts_in_one_column"]:
        # Loop through and plot charts in one column
        for func, show_chart in zip(func_list, b_list):
            if show_chart:
                func(days_off)
    else:
        # Create columns only for the charts that need to be shown
        col_list = st.columns(sum(b_list))
        col_index = 0

        for func, show_chart in zip(func_list, b_list):
            if show_chart:
                with col_list[col_index]:
                    func(days_off)
                col_index += 1


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
