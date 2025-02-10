import streamlit as st
import time

import glb
import imggsum
import imghsum
import imgtsum
import styled_table


def show_charts():
    show = st.session_state.show

    b_list = [
        show["summary_tasks_gantt_chart"],
        show["summary_tasks_per_day"],
        show["summary_hours_per_day"],
    ]

    if not any(b_list):
        return

    days_off = show["days_off"]
    func_list = [imggsum.plot, imgtsum.plot, imghsum.plot]

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


def show_overflow():
    task_overflows = st.session_state.show["summary_task_overflows"]

    if glb.is_ampl_model_overflow() and task_overflows:
        overflow = st.session_state.overflow
        if overflow.sum() > 0:
            st.subheader(":red[There are task overflows!]", divider="red")
            df = overflow[ overflow > 0]
            st.write(df)
        else:
            st.subheader(":green[There in no overflows]", divider="green")


def show_full_schedule(as_html):
    if not st.session_state.show["summary_full_schedule"]:
        return

    st.subheader(":green[Full schedule]", divider="green")

    df = st.session_state.schedule
    styled_df = styled_table.create(df, as_html)

    if as_html:
        # Render the styled dataframe as HTML
        st.markdown(styled_df.to_html(), unsafe_allow_html=True)
    else:
        # Optionally display the dataframe as a Streamlit table
        st.dataframe(styled_df, use_container_width=False)

def show_report():
    show = st.session_state.show

    # Extract relevant values from the session state
    b_list = [
        show["summary_tasks_gantt_chart"],
        show["summary_tasks_per_day"],
        show["summary_hours_per_day"],
        show["summary_task_overflows"],
        show["summary_full_schedule"],
    ]

    # Return early if no charts are to be shown
    if not any(b_list):
        return

    st.divider()
    st.header(":blue[Summary]", divider="blue")

    show_charts()
    show_overflow()
    show_full_schedule(False)


def show():
    time_start = time.perf_counter()
    show_report()
    time_end = time.perf_counter()
    st.session_state.stats["report_summary:ttime"] += time_end - time_start
