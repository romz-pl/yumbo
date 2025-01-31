import bimg
import datetime
import eimg
import gimg
import gimgsum
import glb
import himg
import himgsum
import numpy as np
import os
import pandas as pd
import romz_ampl
import sbar
import simg
import streamlit as st
import timg
import timgsum
import wimg



def tasks_for_expert(expert_name):
    tasks = st.session_state.mprob["tasks"]
    links = st.session_state.mprob["links"]

    # Filter the tasks related to the expert
    filter = links[links["Expert"] == expert_name]["Task"]

    # Use .isin() to filter tasks directly
    return tasks[tasks["Name"].isin(filter)]


def show_tasks_gantt_chart(expert_name):
    tasks = tasks_for_expert(expert_name)
    work_done = st.session_state.glb[f"schedule {expert_name}"].loc[tasks["Name"]].sum(axis=1)
    gimg.plot(tasks, work_done)


def highlight_rows(row):
    if row['Weekdays'] in ['Saturday', 'Sunday']:
        return ['background-color: rgba(144,238,144, 0.2)'] * len(row)
    else:
        return [''] * len(row)


def show_schedule_as_table(expert_name):
    tasks = tasks_for_expert(expert_name)
    start_date = tasks["Start"].min()
    end_date = tasks["End"].max()

    # Retrieve the relevant schedule data
    days = pd.date_range(start=start_date, end=end_date, freq='D')
    df = st.session_state.glb[f"schedule {expert_name}"].loc[tasks["Name"], start_date:end_date]
    df = df.replace(0, '')
    df = df.transpose()
    df.index = days.astype("str")
    # df.index.name = "Date"

    df.insert(0, "Weekdays", days.day_name())

    # Style definitions
    row_hover = {'selector': 'tr:hover', 'props': [('background-color', '#555555')]}
    cell_format = {'selector': 'td', 'props': 'text-align: right;'}
    headers = {'selector': 'th:not(.index_name)', 'props': 'background-color: #000066; color: white;'}

    styled_df = df.style \
                  .format(precision=2) \
                  .apply(highlight_rows, axis=1) \
                  .set_table_styles([row_hover, cell_format, headers], overwrite=True) \
                  .map(lambda v: 'color:LightBlue', subset=['Weekdays'])

    st.markdown(styled_df.to_html(), unsafe_allow_html=True)

    if st.checkbox("Show schedule as Streamlit table", value=False, key=f"checkbox_html_table_{expert_name}") :
        st.dataframe(styled_df, use_container_width=False)


def experts_in_tasks_as_table(task, as_html):

    # Generate day labels and filter dataframe
    days = pd.date_range(start=task.Start, end=task.End, freq="D")

    experts = st.session_state.mprob["experts"].sort_values(by="Name")

    df = pd.DataFrame()
    for expert in experts.itertuples(index=False):
        schedule = st.session_state.glb[f"schedule {expert.Name}"][days]
        expert_data = schedule.loc[task.Name]
        if expert_data.sum() > 0:
            df[expert.Name] = expert_data

    df = df.replace(0, '')
    df.index = days.astype("str")
    df.insert(0, "Weekdays", days.day_name())

    # Style definitions
    row_hover = {'selector': 'tr:hover', 'props': [('background-color', '#555555')]}
    cell_format = {'selector': 'td', 'props': 'text-align: right;'}
    headers = {'selector': 'th:not(.index_name)', 'props': 'background-color: #000066; color: white;'}

    styled_df = df.style \
                  .format(precision=2) \
                  .apply(highlight_rows, axis=1) \
                  .set_table_styles([row_hover, cell_format, headers], overwrite=True) \
                  .map(lambda v: 'color:LightBlue', subset=['Weekdays'])

    if as_html :
        st.markdown(styled_df.to_html(), unsafe_allow_html=True)
    else:
        st.dataframe(styled_df)


def experts_in_tasks_as_table_html(task):
    experts_in_tasks_as_table(task, True)


def experts_in_tasks_as_table_simple(task):
    experts_in_tasks_as_table(task, False)


def show_commitment_per_task(expert_name):
    tasks = tasks_for_expert(expert_name)
    schedule = st.session_state.glb[f"schedule {expert_name}"]
    xbday = st.session_state.mprob["xbday"][st.session_state.mprob["xbday"]["Expert"] == expert_name]
    xbday_grouped = xbday.groupby('Task')
    cols = st.columns(3)

    for jj, task in enumerate(tasks.itertuples(index=False)):
        if task.Name in xbday_grouped.groups:
            bounds = xbday_grouped.get_group(task.Name)
        else:
            bounds = pd.DataFrame()
        with cols[jj % 3]:
            bimg.plot(task, schedule, bounds)


def show_summary():
    if st.session_state.glb["show_experts_overview"]:
        st.divider()

        st.header(":blue[Experts overview]", divider="blue")
        col1, col2, col3 = st.columns(3)
        with col1:
            gimgsum.plot()
        with col2:
            timgsum.plot()
        with col3:
            himgsum.plot()


def show_solver_output():
    st.subheader(f":green[Solver output at {st.session_state.glb['solver timestamp']}]", divider="blue")
    st.code(st.session_state.glb["solver output"])


def show_one_expert(expert_name):
    report_column_no = st.session_state.glb["report_expert_column_no"]
    col_list = st.columns(report_column_no)

    # Define the mapping of chart names to functions
    chart_functions = {
        "Task's Gantt chart": show_tasks_gantt_chart,
        "Tasks per day": timg.plot,
        "Hours per day": himg.plot,
        "Hours per day stacked": simg.plot,
        "Invoice period workload": wimg.plot
    }

    for ii, col in enumerate(col_list, start=1):
        with col:
            chart_name = st.session_state.glb[f"report_expert_column_{ii}"]
            # Call the corresponding function
            chart_functions.get(chart_name)(expert_name)


def show_all_experts():
    experts = st.session_state.mprob["experts"].sort_values(by="Name")
    report = st.session_state.glb["report:experts"]

    # Filter experts with any active field
    active_experts = experts[
        experts["Name"].apply(
            lambda name: any(report.at[name, col] for col in ["Charts", "Table", "Commitment"])
        )
    ]

    if active_experts.empty:
        return


    st.divider()

    st.header("Experts", divider="green")
    for expert in active_experts.itertuples(index=False):
        bCharts = report.at[expert.Name, "Charts"]
        bTable = report.at[expert.Name, "Table"]
        bCommitment = report.at[expert.Name, "Commitment"]

        if bCharts or bTable or bCommitment:
            st.subheader(f"Expert: :blue['{expert.Name}'], {expert.Comment}", divider="blue")

            if bCharts:
                show_one_expert(expert.Name)

            if bTable:
                show_schedule_as_table(expert.Name)

            if bCommitment:
                show_commitment_per_task(expert.Name)


def show_one_task(task):
    column_no = st.session_state.glb["report_task_column_no"]
    col_list = st.columns(column_no)

    chart_functions = {
        "Experts per day stacked": eimg.plot,
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


def show_all_tasks():
    tasks = st.session_state.mprob["tasks"].sort_values(by="Name")
    report = st.session_state.glb["report:tasks"]

    if not report.loc[tasks["Name"], "Report"].any():
        return

    st.divider()

    st.header("Tasks", divider="green")
    for task in tasks.itertuples(index=False):
        if report.at[task.Name, "Report"]:
            st.subheader(f"Task: :blue['{task.Name}']", divider="blue")
            show_one_task(task)


def show_time_counters():
    st.subheader(":green[Statistics on chart creation]", divider="blue")

    chart_data = [
        ("Plot task with its constrains", "bimg"),
        ("Task's Gantt Chart", "gimg"),
        ("Task's Gantt Chart (Summary)", "gimgsum"),
        ("Hours per day", "himg"),
        ("Hours per day  (Summary)", "himgsum"),
        ("Hours per day stacked", "simg"),
        ("Tasks per day", "timg"),
        ("Tasks per day (Summary)", "timgsum"),
        ("Invoicing Periods Workload", "wimg"),
        ("Experts per day stacked", "eimg"),
    ]

    time_total_col = "Total time [s]"
    time_avg_col = "Average time [s]"

    nbytes_total_col = "Total nbytes [KiB]"
    nbytes_avg_col = "Average nbytes [B]"

    # Extract relevant data in a single pass
    chart_titles = []
    short_names = []
    num_calls = []
    time_total = []
    time_avg = []
    nbytes_total = []
    nbytes_avg = []

    for title, short_name in chart_data:
        chart_titles.append(title)
        short_names.append(short_name)

        cnt = st.session_state.glb[f"time:{short_name}:cnt"]
        ttime = st.session_state.glb[f"time:{short_name}:ttime"]
        nbytes = st.session_state.glb[f"time:{short_name}:nbytes"]

        num_calls.append(cnt)
        time_total.append(ttime)
        time_avg.append(ttime / cnt if cnt != 0 else 0)
        nbytes_total.append(nbytes / 1024)
        nbytes_avg.append(nbytes / cnt if cnt != 0 else 0)

    # Create a DataFrame to organize the data
    data = pd.DataFrame({
        "Chart title": chart_titles,
        "Chart short name": short_names,
        "Number of calls": num_calls,
        time_total_col: time_total,
        time_avg_col: time_avg,
        nbytes_total_col: nbytes_total,
        nbytes_avg_col: nbytes_avg,
    })

    # Create DataFrame and format it
    format_spec = {
        time_total_col: "{:,.3f}",
        time_avg_col: "{:,.3f}",
        nbytes_total_col: "{:,.0f}",
        nbytes_avg_col: "{:,.0f}",
    }

    df = pd.DataFrame(data)
    df_styled = (
        df
        .sort_values(by=time_total_col, ascending=False)
        .style.format(format_spec)
    )

    # Display DataFrame
    st.dataframe(df_styled, hide_index=True, use_container_width=False)

    mb = df[nbytes_total_col].sum()  / 1024
    st.markdown("**For all figures, the total number of data downloaded is: :green[{:,.3f} MiB]**".format(mb))


def show_ampl_stats():
    st.subheader(":green[Statistics on AMPL solution]", divider="blue")

    st.markdown("**Total elapsed time: :green[{:.3f} [s]]**".format(st.session_state.glb['time:ampl:ttime']))

def show_main_panel():
    show_summary()
    show_all_experts()
    show_all_tasks()
    show_solver_output()
    show_time_counters()
    show_ampl_stats()


def set_page_config():
    st.set_page_config(page_title="Yumbo",layout="wide")
    # css = '''
    # <style>
    #     [data-testid="stSidebar"]{
    #         min-width: 400px;
    #         max-width: 800px;
    #     }
    # </style>
    # '''
    # st.html(css)


def show_page_header():
    st.title(":red[Yumbo.] Scheduling, Planning and Resource Allocation")
    st.subheader("Zbigniew Romanowski, Paweł Koczyk")
    st.caption("Source code, documentation and sample Excel input files can be found on [Yumbo's](https://github.com/romz-pl/yambo) GitHub repository.")
    st.caption("_{d}_".format(d=datetime.datetime.now().strftime("%d %B %Y, %H:%M:%S %p")))


def show_yumbo_description():
    st.divider()
    cols = st.columns(2)

    # The cols[1] and cols[2] are not used!
    with cols[0]:
        dd = os.path.dirname(__file__)
        with open(f"{dd}/../doc/yumbo.md", "r") as f:
            st.markdown(f'''{f.read()}''')

    st.divider()
    st.image(f"{dd}/../doc/yumbo.webp")
    st.caption("Image generated by ChatGPT")


def zero_time_counters():
    charts = ["bimg", "gimg", "gimgsum", "himg", "himgsum", "simg", "timg", "timgsum", "wimg", "eimg"]
    for v in charts:
        st.session_state.glb[f"time:{v}:cnt"] = 0
        st.session_state.glb[f"time:{v}:ttime"] = 0
        st.session_state.glb[f"time:{v}:nbytes"] = 0

    st.session_state.glb[f"time:ampl:ttime"] = 0


def main():

    if 'glb' not in st.session_state:
        st.session_state.glb = dict()

    if 'mprob' not in st.session_state:
        st.session_state.mprob = dict()

    # plt.style.use('seaborn-v0_8-whitegrid')
    set_page_config()
    show_page_header()
    zero_time_counters()

    with st.sidebar:
        uploaded_file = sbar.load_excel_file()
        if uploaded_file != None:
            new_input = sbar.show(uploaded_file)

    if uploaded_file == None:
        show_yumbo_description()
        return

    if new_input:
        try:
            romz_ampl.solve(uploaded_file)
        except Exception as e:
            st.subheader(f":red[Exception during solving process.] {e}")
            return

    show_main_panel()


######################## CALL MAIN FUNCTION ##################

if __name__ == "__main__":
    main()

