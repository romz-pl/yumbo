import matplotlib.figure as matplotlib_figure
import matplotlib.ticker as matplotlib_ticker
import pandas as pd
import streamlit as st
import time

import glb
import imgb
import imgg
import imgh
import imgs
import imgt
import imgw
import styled_table



def show_xbday_per_task(expert_name):
    # Cache frequently used session state objects
    mprob = st.session_state.mprob
    amplsol = st.session_state.schedule

    # Filter tasks for the expert using a cross-section on the assignment DataFrame
    filter = mprob["assign"].xs(expert_name, level="Elevel")["Task"]
    expert_tasks = mprob["task"].loc[filter]

    # Get the expert's schedule
    schedule = amplsol[expert_name]

    # Get the 'xbday' DataFrame for the expert and precompute groups by 'Task'
    xbday = mprob["xbday"][mprob["xbday"]["Expert"] == expert_name]
    xbday_groups = {group_name: group_df for group_name, group_df in xbday.groupby('Task')}

    # Create 3 columns for layout
    cols = st.columns(3)

    # Iterate over each task row (as a namedtuple) and plot the xbday
    for idx, task_row in enumerate(expert_tasks.itertuples(index=False)):
        # Look up bounds for the task from the precomputed groups dictionary.
        bounds = xbday_groups.get(task_row.Name, pd.DataFrame())
        # Plot in the appropriate column
        with cols[idx % 3]:
            imgb.plot(task_row, schedule, bounds)



def show_schedule_as_table(expert_name, as_html):
    # Retrieve data from session state
    task = st.session_state.mprob["task"]
    assign = st.session_state.mprob["assign"]

    # Filter tasks for the specified expert
    filter = assign.xs(expert_name, level="Elevel")["Task"]
    expert_tasks = task.loc[filter]

    # Calculate the date range
    start_date, end_date = expert_tasks["Start"].min(), expert_tasks["End"].max()

    # Retrieve and format the relevant schedule data
    df = st.session_state.schedule[expert_name].loc[start_date:end_date, expert_tasks["Name"]]
    df.name = expert_name

    styled_table.show(df, as_html)


def show_one_expert(expert_name):
    # Mapping of chart names to their respective plotting functions
    chart_functions = {
        "Task's Gantt chart": imgg.plot,
        "Tasks per day": imgt.plot,
        "Hours per day": imgh.plot,
        "Hours per day stacked": imgs.plot,
        "Invoice period workload": imgw.plot,
    }

    days_off = st.session_state.show["days_off"]
    report_column_no = st.session_state.show["expert_column_no"]

    # Retrieve the column chart names in advance
    column_chart_names = [
        st.session_state.show[f"expert_column_{ii}"]
        for ii in range(1, report_column_no + 1)
    ]

    if st.session_state.show["expert_charts_in_one_column"]:
        # Render charts in rows
        for chart_name in column_chart_names:
            if chart_name in chart_functions:
                chart_functions[chart_name](expert_name, days_off)
    else:
        # Render charts in columns
        col_list = st.columns(report_column_no)
        for col, chart_name in zip(col_list, column_chart_names):
            with col:
                if chart_name in chart_functions:
                    chart_functions[chart_name](expert_name, days_off)


def show_report():
    show_experts = st.session_state.show["experts"]

    # Return if no experts are selected
    if not show_experts.any(axis=None):
        return

    st.divider()
    st.header(":material/person: :blue[Experts]", divider="blue")
    experts = st.session_state.mprob["expert"]

    # Filter only rows with any True values
    active_experts = show_experts[show_experts.any(axis=1)]

    for expert_name, row in active_experts.iterrows():
        st.subheader(
            f":green[{expert_name}, {experts.loc[expert_name, 'Comment']}]",
            divider="green"
        )

        if row["Chart"]:
            show_one_expert(expert_name)
        if row["H:Table"]:
            show_schedule_as_table(expert_name, True)
        if row["S:Table"]:
            show_schedule_as_table(expert_name, False)
        if row["xbday"]:
            show_xbday_per_task(expert_name)


def show():
    time_start = time.perf_counter()
    show_report()
    time_end = time.perf_counter()
    st.session_state.stats["report_experts:ttime"] += time_end - time_start
