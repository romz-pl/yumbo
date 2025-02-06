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



def show_commitment_per_task(expert_name):
    # Cache frequently used session state objects
    mprob = st.session_state.mprob
    amplsol = st.session_state.amplsol

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

    # Iterate over each task row (as a namedtuple) and plot the commitment
    for idx, task_row in enumerate(expert_tasks.itertuples(index=False)):
        # Look up bounds for the task from the precomputed groups dictionary.
        bounds = xbday_groups.get(task_row.Name, pd.DataFrame())
        # Plot in the appropriate column
        with cols[idx % 3]:
            imgb.plot(task_row, schedule, bounds)


def show_schedule_as_table(expert_name):
    # Retrieve data from session state
    task = st.session_state.mprob["task"]
    assign = st.session_state.mprob["assign"]

    # Filter tasks for the specified expert
    filter = assign.xs(expert_name, level="Elevel")["Task"]
    expert_tasks = task.loc[filter]

    # Calculate the date range
    start_date, end_date = expert_tasks["Start"].min(), expert_tasks["End"].max()
    days = pd.date_range(start=start_date, end=end_date, freq='D')

    # Retrieve and format the relevant schedule data
    df = st.session_state.amplsol[expert_name].loc[start_date:end_date, expert_tasks["Name"]]

    styled_df = styled_table.create(df, days)

    # Render the styled dataframe as HTML
    st.markdown(styled_df.to_html(), unsafe_allow_html=True)

    # Optionally display the dataframe as a Streamlit table
    if st.checkbox(f"Show schedule as simple table", value=False, key=f"checkbox_html_table_{expert_name}"):
        st.dataframe(styled_df, use_container_width=False)


def show_one_expert(expert_name):
    report_column_no = st.session_state.glb["report_expert_column_no"]
    col_list = st.columns(report_column_no)

    # Define the mapping of chart names to functions
    chart_functions = {
        "Task's Gantt chart": imgg.plot,
        "Tasks per day": imgt.plot,
        "Hours per day": imgh.plot,
        "Hours per day stacked": imgs.plot,
        "Invoice period workload": imgw.plot
    }

    days_off = st.session_state.show["days_off"]
    for ii, col in enumerate(col_list, start=1):
        with col:
            chart_name = st.session_state.glb[f"report_expert_column_{ii}"]
            # Call the corresponding function
            chart_functions.get(chart_name)(expert_name, days_off)

def show_report():
    report = st.session_state.show["experts"]

    # If all values are False
    if (~report[["Charts", "Table", "Commitment"]]).all().all():
        return

    # Filter experts with any active field
    experts = st.session_state.mprob["expert"].sort_values(by="Name")

    active_experts = experts[
        experts["Name"].apply(
            lambda name: any(report.at[name, col] for col in ["Charts", "Table", "Commitment"])
        )
    ]

    if active_experts.empty:
        return


    st.divider()

    st.header(":blue[Experts]", divider="blue")
    for expert in active_experts.itertuples(index=False):
        bCharts = report.at[expert.Name, "Charts"]
        bTable = report.at[expert.Name, "Table"]
        bCommitment = report.at[expert.Name, "Commitment"]

        if bCharts or bTable or bCommitment:
            st.subheader(f":green[{expert.Name}, {expert.Comment}]", divider="green")

            if bCharts:
                show_one_expert(expert.Name)

            if bTable:
                show_schedule_as_table(expert.Name)

            if bCommitment:
                show_commitment_per_task(expert.Name)


def show():
    time_start = time.perf_counter()
    show_report()
    time_end = time.perf_counter()
    st.session_state.stats["report_experts:ttime"] += time_end - time_start
