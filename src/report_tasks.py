import imge
import pandas as pd
import streamlit as st
import styled_table
import time


def experts_in_tasks_as_table(task, as_html):

    # Generate day labels based on the task start and end dates
    days = pd.date_range(start=task.Start, end=task.End, freq="D")

    # Sort experts by Name
    experts = st.session_state.mprob["expert"].sort_values("Name")

    # Build a dictionary with expert names as keys and their corresponding schedule series as values,
    # but only include experts that have the task column and a positive total for that task.
    data = dict()
    for expert in experts.itertuples(index=False):
        schedule = st.session_state.amplsol[expert.Name].loc[days]
        if task.Name in schedule.columns:
            expert_data = schedule[task.Name]
            if expert_data.sum() > 0:
                data[expert.Name] = expert_data


    # Create the DataFrame with the index already set to the string representation of `days`
    df = pd.DataFrame(data)
    styled_df = styled_table.create(df, days)

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

    for ii, col in enumerate(col_list, start=1):
        with col:
            chart_name = st.session_state.glb[f"report_task_column_{ii}"]
            # Call the corresponding function
            #st.write(chart_name)
            #st.write(chart_functions.get(chart_name))
            chart_functions.get(chart_name)(task)


def show_report():
    tasks = st.session_state.mprob["task"].sort_values(by="Name")
    report = st.session_state.glb["report:tasks"]

    if not report.loc[tasks["Name"], "Report"].any():
        return

    st.divider()

    st.header(":blue[Tasks]", divider="blue")
    for task in tasks.itertuples(index=False):
        if report.at[task.Name, "Report"]:
            st.subheader(f":green[{task.Name}]", divider="green")
            show_one_task(task)


def show():
    time_start = time.perf_counter()
    show_report()
    time_end = time.perf_counter()
    st.session_state.stats["report_tasks:ttime"] += time_end - time_start
