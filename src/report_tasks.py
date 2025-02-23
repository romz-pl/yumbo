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
    df.name = task.Name
    styled_table.show(df, as_html)


def get_subheader(task_name):
    info = ""
    if glb.is_ampl_model_overflow():
        overflow_value = st.session_state.overflow.loc[task_name]
        if overflow_value > 0:
            info = f", :red[overflow {overflow_value:.2f} [h]]"

    return f":material/task: :green[{task_name}]{info}"


def show_report():
    show_tasks = st.session_state.show["tasks"]

    # Return if no tasks are selected
    if not show_tasks.any(axis=None):
        return

    st.divider()
    st.header(":material/receipt_long: :blue[Tasks]", divider="blue")
    tasks = st.session_state.mprob["task"]

    # Filter only rows with any True values
    active_tasks = show_tasks[show_tasks.any(axis=1)]

    days_off = st.session_state.show["days_off"]

    for task_name, row in active_tasks.iterrows():
        st.subheader(get_subheader(task_name), divider="green")
        task = tasks.loc[task_name]
        if row["Chart"]:
            imge.plot(task, days_off)
        if row["H:Table"]:
            experts_in_tasks_as_table(task, True)
        if row["S:Table"]:
            experts_in_tasks_as_table(task, False)


def show():
    time_start = time.perf_counter()
    show_report()
    time_end = time.perf_counter()
    st.session_state.stats["report_tasks:ttime"] += time_end - time_start
