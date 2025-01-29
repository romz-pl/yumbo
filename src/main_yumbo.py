import bimg
import datetime
import gimg
import glb
import himg
import numpy as np
import os
import pandas as pd
import romz_ampl
import sbar
import simg
import streamlit as st
import timg
import wimg


def show_tasks_gantt_chart(expert_name):
    tasks = glb.tasks_for_expert(expert_name)
    work_done = st.session_state.glb[f"schedule {expert_name}"].loc[tasks["Name"]].sum(axis=1)
    gimg.plot(tasks, work_done)


def highlight_rows(row):
    if row['Weekdays'] in ['Saturday', 'Sunday']:
        return ['background-color: rgba(144,238,144, 0.2)'] * len(row)
    else:
        return [''] * len(row)


def show_schedule_as_table(expert_name):
    tasks = glb.tasks_for_expert(expert_name)
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


def show_commitment_per_task(expert_name):
    tasks_for_expert = glb.tasks_for_expert(expert_name)
    schedule = st.session_state.glb[f"schedule {expert_name}"]
    xbday = st.session_state.glb["xbday"][st.session_state.glb["xbday"]["Expert"] == expert_name]
    xbday_grouped = xbday.groupby('Task')
    cols = st.columns(3)

    for jj, task in enumerate(tasks_for_expert.itertuples(index=False)):
        if task.Name in xbday_grouped.groups:
            bounds = xbday_grouped.get_group(task.Name)
        else:
            bounds = pd.DataFrame()
        with cols[jj % 3]:
            bimg.plot(task, schedule, bounds)


def show_summary():
    if st.session_state.glb["show_experts_overview"]:
        st.subheader(":blue[Experts overview]", divider="blue")
        col1, col2, col3 = st.columns(3)
        with col1:
            gimg.plot_summary()
        with col2:
            timg.plot_summary()
        with col3:
            himg.plot_summary()


def show_solver_output():
    st.subheader(f":green[Solver output at {st.session_state.glb['solver timestamp']}]", divider="blue")
    st.code(st.session_state.glb["solver output"])


def show_one_row(expert_name):
    report_column_no = st.session_state.glb["report_column_no"]
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
            chart_name = st.session_state.glb[f"report_column_{ii}"]
            # Call the corresponding function
            chart_functions.get(chart_name)(expert_name)


def show_all_rows():
    experts = st.session_state.glb["experts"].sort_values(by="Name")
    report = st.session_state.glb["report"]

    for row in experts.itertuples(index=False):
        expert_name = row.Name
        st.subheader(f":blue[{expert_name}] {row.Comment}", divider="blue")

        if report.at[expert_name, "Charts"]:
            show_one_row(expert_name)

        if report.at[expert_name, "Table"]:
            show_schedule_as_table(expert_name)

        if report.at[expert_name, "Commitment"]:
            show_commitment_per_task(expert_name)


def show_time_counters():
    st.subheader(":green[Elapsed time for chart creation]", divider="blue")

    chart_data = [
        ("Plot task with its constrains", "bimg"),
        ("Task's Gantt Chart", "gimg"),
        ("Hours per day", "himg"),
        ("Hours per day stacked", "simg"),
        ("Tasks per day", "timg"),
        ("Invoicing Periods Workload", "wimg"),
    ]

    elapsed_time_col = "Elapsed time [s]"
    avg_time_col = "Average time per chart [s]"

    # Extract relevant data in a single pass
    chart_titles = []
    short_names = []
    num_calls = []
    elapsed_times = []
    avg_times = []

    for title, short_name in chart_data:
        chart_titles.append(title)
        short_names.append(short_name)

        cnt = st.session_state.glb[f"time:{short_name}:cnt"]
        val = st.session_state.glb[f"time:{short_name}:val"]

        num_calls.append(cnt)
        elapsed_times.append(val)
        avg_times.append(val / cnt if cnt != 0 else 0)

    # Create a DataFrame to organize the data
    data = pd.DataFrame({
        "Chart title": chart_titles,
        "Chart short name": short_names,
        "Number of calls": num_calls,
        elapsed_time_col: elapsed_times,
        avg_time_col: avg_times,
    })

    # Create DataFrame and format it
    format_spec = {
        elapsed_time_col: "{:.3f}",
        avg_time_col: "{:.3f}",
    }

    df = (
        pd.DataFrame(data)
        .sort_values(by=elapsed_time_col, ascending=False)
        .style.format(format_spec)
    )

    # Display DataFrame
    st.dataframe(df, hide_index=True, use_container_width=False)


def show_main_panel():
    show_summary()
    show_all_rows()
    show_solver_output()
    show_time_counters()


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
    charts = ["bimg", "gimg", "himg", "simg", "timg", "wimg"]
    for v in charts:
        st.session_state.glb[f"time:{v}:cnt"] = 0
        st.session_state.glb[f"time:{v}:val"] = 0


def main():

    if 'glb' not in st.session_state:
        st.session_state.glb = dict()

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
            romz_ampl.solve(uploaded_file.name)
        except Exception as e:
            st.subheader(f":red[Exception during solving process.] {e}")
            return

    show_main_panel()


######################## CALL MAIN FUNCTION ##################

if __name__ == "__main__":
    main()

