import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
import numpy as np
import os
import pandas as pd
import streamlit as st
import tempfile

import romz_ampl
import romz_datetime
import romz_excel
import plot_hours_per_day
import plot_invoicing_periods_histogram
import plot_shedule_stacked_histogram
import plot_task
import plot_tasks_gantt
import plot_tasks_per_day
import glb

def show_tasks():
    st.subheader("Tasks definition", divider="blue")
    format = {'Start day': "{:%Y-%m-%d}", 'End day': "{:%Y-%m-%d}", 'Avg': "{:.4f}"}
    df = glb.data["tasks"].style.format(format)
    st.dataframe(df, hide_index=True, use_container_width=True)


def show_links():
    st.subheader("Links", divider="blue")
    st.dataframe(glb.data["links"], hide_index=True, use_container_width=True)


def show_xbday():
    st.subheader("Bounds xbday", divider="blue")
    format = {'Start day': "{:%Y-%m-%d}", 'End day': "{:%Y-%m-%d}"}
    df = glb.data["xbday"].style.format(format)
    st.dataframe(df, hide_index=True, use_container_width=True)


def show_xbsum():
    st.subheader("Bounds xbsum", divider="blue")
    format = {'Start day': "{:%Y-%m-%d}", 'End day': "{:%Y-%m-%d}"}
    df = glb.data["xbsum"].style.format(format)
    st.dataframe(df, hide_index=True, use_container_width=True)


def show_ubday():
    st.subheader("Bounds ubday", divider="blue")
    format = {'Start day': "{:%Y-%m-%d}", 'End day': "{:%Y-%m-%d}"}
    df = glb.data["ubday"].style.format(format)
    st.dataframe(df, hide_index=True, use_container_width=True)


def show_ubsum():
    st.subheader("Bounds ubsum", divider="blue")
    format = {'Start day': "{:%Y-%m-%d}", 'End day': "{:%Y-%m-%d}"}
    df = glb.data["ubsum"].style.format(format)
    st.dataframe(df, hide_index=True, use_container_width=True)


def show_experts():
    st.subheader("Experts names", divider="blue")
    st.dataframe(glb.data["experts"], hide_index=True, use_container_width=True)


def show_expert_bounds():
    st.subheader("Expert bounds and preferences", divider="blue")
    format = {'Start day': "{:%Y-%m-%d}", 'End day': "{:%Y-%m-%d}"}
    df = glb.data["expert bounds"].style.format(format)
    st.dataframe(df, hide_index=True, use_container_width=True)


def show_invoicing_periods():
    st.subheader("Invoicing periods", divider="blue")
    format = {'Start day': "{:%Y-%m-%d}", 'End day': "{:%Y-%m-%d}"}
    df = glb.data["invoicing periods"].style.format(format)
    st.dataframe(df, hide_index=True, use_container_width=True)



def show_invoicing_periods_bounds():
    st.subheader("Invoicing periods bounds", divider="blue")
    st.dataframe(glb.data["invoicing periods bounds"], hide_index=True, use_container_width=True)


def load_excel_file():
    st.subheader("Load a Excel data file", divider="blue")
    uploaded_file = st.file_uploader("Excel file required in format 'xlsx'")
    if uploaded_file == None:
        st.subheader(":red[Select Excel data file for scheduling investigation!]")
    st.caption("See the [Yumbo](https://github.com/romz-pl/yambo/tree/main/ampl-data-input-excel) GitHub repository for sample Excel input files.")
    return uploaded_file


def prepare_global_data(uploaded_file):
    # global glb.data

    if 'key:uploaded_file' in st.session_state:
        new_input = ( st.session_state['key:uploaded_file'] != uploaded_file )
    else:
        new_input = True

    if new_input:
        with tempfile.NamedTemporaryFile(suffix=".xlsx") as f:
            f.write(uploaded_file.getvalue())
            f.flush()
            romz_excel.read(f.name)
        st.session_state['key:glb.data'] = glb.data
        st.session_state['key:uploaded_file'] = uploaded_file
    else:
        glb.data = st.session_state['key:glb.data']

    return new_input


def get_tasks_for_expert(expert_name):
    tasks = glb.data["tasks"]
    links = glb.data["links"]

    # Filter the tasks related to the expert
    tasks_for_expert = links[links["Expert"] == expert_name]["Task"]

    # Use .isin() to filter tasks directly
    return tasks[tasks["Name"].isin(tasks_for_expert)]



def show_tasks_gantt_chart(expert_name):
    tasks = get_tasks_for_expert(expert_name)
    work_done = glb.data[f"schedule {expert_name}"].loc[tasks["Name"]].sum(axis=1)
    plot_tasks_gantt.plot(tasks, work_done)


def show_tasks_per_day(expert_name):
    schedule = glb.data[f"schedule {expert_name}"]
    plot_tasks_per_day.plot(schedule, glb.tstart(), glb.tend())


def show_invoice_period_workload(expert_name):
    invper = glb.data["invoicing periods"]
    schedule = glb.data[f"schedule {expert_name}"]
    invper_bounds = glb.data["invoicing periods bounds"]
    bounds = invper_bounds[ invper_bounds["Expert"] == expert_name ]
    plot_invoicing_periods_histogram.plot(invper, schedule, bounds)


def show_hours_per_day(expert_name):
    start = glb.hstart()
    end = glb.hend()
    data = glb.data[f"schedule {expert_name}"]
    plot_hours_per_day.plot(data, start, end)


def show_hours_per_day_stacked(expert_name):
    start = glb.hstart()
    end = glb.hend()
    if pd.bdate_range(start=start, end=end, freq='C', holidays = glb.data["public holidays"]["Date"]).size > 10:
        width = 1
    else:
        width = 0.9
    plot_shedule_stacked_histogram.plot(glb.data[f"schedule {expert_name}"], start, end, width)


def show_schedule_as_table(expert_name):
    tasks = get_tasks_for_expert(expert_name)
    start_date = romz_datetime.to_string(tasks["Start day"].min())
    end_date = romz_datetime.to_string(tasks["End day"].max())

    # Retrieve the relevant schedule data
    df = glb.data[f"schedule {expert_name}"].loc[tasks["Name"], start_date:end_date]

    # Apply styling to the DataFrame
    styled_df = df.style.format(precision=2) \
                        .highlight_between(left=0.24, right=None, props='color:white; background-color:purple') \
                        .highlight_between(left=None, right=0.24, props='color:white; background-color:white;')

    st.dataframe(styled_df)



def show_commitment_per_task(expert_name):
    tasks_for_expert = get_tasks_for_expert(expert_name)
    col1, col2, col3 = st.columns(3)
    j = 0
    for idx in tasks_for_expert.index:
        j += 1
        task = tasks_for_expert.loc[idx]
        schedule = glb.data[f"schedule {expert_name}"]
        xbday = glb.data["xbday"]
        bounds = xbday.loc[ xbday["Task"] == task["Name"]].loc[ xbday["Expert"] == expert_name]
        with col1:
            if(j % 3 == 1):
                plot_task.plot(task, schedule, bounds)

        with col2:
            if(j % 3 == 2):
                plot_task.plot(task, schedule, bounds)

        with col3:
            if(j % 3 == 0):
                plot_task.plot(task, schedule, bounds)


def customise_report():
    st.subheader("Customise report", divider="blue")
    glb.data["show_experts_overview"] = st.checkbox("Show experts overview?", value=True)

    max_col_no = 4
    report_column_no = st.number_input("Number of columns", min_value=1, max_value=max_col_no, value=3)

    for ii in range(1, max_col_no + 1):
        glb.data[f"report_column_{ii}"] = st.selectbox(
            f"Col {ii}",
            ("Task's Gantt chart", "Tasks per day", "Hours per day stacked", "Hours per day", "Invoice period workload"),
            disabled = (ii > report_column_no),
            index = (ii - 1)
        )
    glb.data["report_column_no"] = report_column_no

    show_all_experts = st.checkbox("Show all experts?")

    expert = glb.data["experts"]["Name"].to_numpy()
    rowno = len(expert)
    colno = 4
    df = pd.DataFrame(np.zeros(rowno * colno, dtype='bool').reshape((rowno, colno)),
        index = expert,
        columns = ["Expert", "Show?", "Table?", "Commitment?"])
    df["Expert"] = expert

    if show_all_experts:
        df["Show?"] = np.ones(rowno, dtype='bool')

    edited_df = st.data_editor(
        df,
        hide_index=True,
        use_container_width=True,
        column_config = {
            "Expert": st.column_config.TextColumn(disabled=True, pinned=True),
            "Show?": st.column_config.CheckboxColumn(),
            "Table?": st.column_config.CheckboxColumn(),
            "Commitment?": st.column_config.CheckboxColumn(),
        }
    )

    glb.data["report"] = edited_df


def show_sidebar(uploaded_file):
    new_input = prepare_global_data(uploaded_file)
    st.subheader("Today: :green[{today}]".format(today=glb.today().date()), divider="blue")
    st.subheader("Hours per day: :green[{}]".format(glb.hours_per_day()), divider="blue")
    customise_report()
    show_tasks()
    show_experts()
    show_links()
    show_xbday()
    show_xbsum()
    show_ubday()
    show_ubsum()
    show_expert_bounds()
    show_invoicing_periods()
    show_invoicing_periods_bounds()
    return new_input


def show_tasks_gantt_chart_summary():
    plot_tasks_gantt.plot_summary(glb.data["tasks"])


def show_tasks_per_day_summary():
    dfs = [ glb.data[f"schedule {e}"]  for e in glb.data["experts"]["Name"] ]
    #start = glb.today() + datetime.timedelta(days=1)
    #end = glb.today() + datetime.timedelta(days=int(glb.data["DAY_NO"]))
    plot_tasks_per_day.plot(sum(dfs), glb.tstart(), glb.tend())


def show_hours_per_day_summary():
    dfs = [ glb.data[f"schedule {e}"]  for e in glb.data["experts"]["Name"] ]
    #start = glb.today() + datetime.timedelta(days=1)
    #end = glb.today() + datetime.timedelta(days=int(glb.data["DAY_NO"]))
    plot_hours_per_day.plot(sum(dfs), glb.hstart(), glb.hend())


def show_summary():
    if glb.data["show_experts_overview"]:
        st.subheader(":blue[Experts overview]", divider="blue")
        col1, col2, col3 = st.columns(3)
        with col1:
            show_tasks_gantt_chart_summary()
        with col2:
            show_tasks_per_day_summary()
        with col3:
            show_hours_per_day_summary()

def show_solver_output():
    st.subheader(f":green[Solver output at {glb.data['solver timestamp']}]", divider="blue")
    st.code(glb.data["solver output"])

def show_one_row(expert_name):
    report_column_no = glb.data["report_column_no"]
    col_list = st.columns(report_column_no)
    for ii, col in enumerate(col_list):
        with col:
            chart_name  = glb.data[f"report_column_{ii+1}"]
            if chart_name == "Task's Gantt chart":
                show_tasks_gantt_chart(expert_name)
            elif chart_name == "Tasks per day":
                show_tasks_per_day(expert_name)
            elif chart_name == "Hours per day":
                show_hours_per_day(expert_name)
            elif chart_name == "Hours per day stacked":
                show_hours_per_day_stacked(expert_name)
            elif chart_name == "Invoice period workload":
                show_invoice_period_workload(expert_name)
            else:
                st.write(chart_name)



def show_main_panel():
    show_summary()

    experts = glb.data["experts"].sort_values(by='Name')
    for e in experts.index:
        expert_name = experts.loc[e, "Name"]
        st.subheader(":blue[{name}] {comment}".format(name=expert_name, comment=experts.loc[e, "Comment"]), divider="blue")
        if glb.data["report"].loc[expert_name, "Show?"]:
            show_one_row(expert_name)

            if glb.data["report"].loc[expert_name, "Table?"]:
                show_schedule_as_table(expert_name)

            if glb.data["report"].loc[expert_name, "Commitment?"]:
                show_commitment_per_task(expert_name)
    show_solver_output()


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


def shwo_yumbo_description():
    st.divider()
    col1, col2, col3 = st.columns(3)

    with col1:
        dd = os.path.dirname(__file__)
        with open(f"{dd}/../doc/yumbo.md", "r") as f:
            st.markdown(f'''{f.read()}''')

    st.divider()
    st.image(f"{dd}/../doc/yumbo.webp")
    st.caption("Image generated by ChatGPT")

def main():
    # plt.style.use('seaborn-v0_8-whitegrid')
    set_page_config()
    show_page_header()

    with st.sidebar:
        uploaded_file = load_excel_file()
        if uploaded_file != None:
            new_input = show_sidebar(uploaded_file)

    if uploaded_file == None:
        shwo_yumbo_description()
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


