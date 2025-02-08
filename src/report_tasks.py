import pandas as pd
import streamlit as st
import styled_table
import time

import glb
import imge


def experts_in_tasks_as_table(task, as_html):

    # Generate day labels based on the task start and end dates
    days = pd.date_range(start=task.Start, end=task.End, freq="D")

    # Sort experts by Name
    experts = st.session_state.mprob["expert"].sort_values("Name")

    # Build a dictionary with expert names as keys and their corresponding schedule series as values,
    # but only include experts that have the task column and a positive total for that task.
    data = dict()
    for expert in experts.itertuples(index=False):
        schedule = st.session_state.schedule[expert.Name].loc[days]
        if task.Name in schedule.columns:
            expert_data = schedule[task.Name]
            if expert_data.sum() > 0:
                data[expert.Name] = expert_data


    # Create the DataFrame with the index already set to the string representation of `days`
    df = pd.DataFrame(data)
    styled_df = styled_table.create(df, days, as_html)

    # Render the styled DataFrame
    if as_html:
        st.markdown(styled_df.to_html(), unsafe_allow_html=True)
    else:
        st.dataframe(styled_df)


def experts_in_tasks_as_table_html(task):
    experts_in_tasks_as_table(task, True)


def experts_in_tasks_as_table_simple(task):
    experts_in_tasks_as_table(task, False)


def show_one_task(task):
    column_no = st.session_state.glb["report_task_column_no"]
    col_list = st.columns(column_no)

    chart_functions = {
        "Experts per day stacked": imge.plot,
        "HTML table": experts_in_tasks_as_table_html,
        "Simple table": experts_in_tasks_as_table_simple,
    }

    days_off = st.session_state.show["days_off"]
    for ii, col in enumerate(col_list, start=1):
        with col:
            chart_name = st.session_state.glb[f"report_task_column_{ii}"]
            # Call the corresponding function
            chart_functions.get(chart_name)(task, days_off)


def show_report():
    show_tasks = st.session_state.show["tasks"]

    # Return if no tasks are selected
    if not show_tasks.any(axis=None):
        return

    st.divider()
    st.header(":blue[Tasks]", divider="blue")
    tasks = st.session_state.mprob["task"]

    # Filter only rows with True value
    selected_tasks = show_tasks[show_tasks["Report"]]

    # Batch process selected tasks  
    if glb.is_ampl_model_overflow():
        overflow = st.session_state.overflow
        for task_id in selected_tasks.index:
            v = overflow.loc[task_id]
            info = f", :red[overflow {v:.2f} [h]]" if v > 0 else ""
            st.subheader(f":green[{task_id}]{info}", divider="green")
            show_one_task(tasks.loc[task_id])
    else:
        for task_id in selected_tasks.index:
            st.subheader(f":green[{task_id}]", divider="green")
            show_one_task(tasks.loc[task_id])


def show():
    time_start = time.perf_counter()
    show_report()
    time_end = time.perf_counter()
    st.session_state.stats["report_tasks:ttime"] += time_end - time_start
