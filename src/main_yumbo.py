import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
import numpy as np
import pandas as pd
import streamlit as st
import tempfile

import romz_ampl
import romz_datetime
import romz_excel
import romz_plot_hours_per_day
import romz_plot_invoicing_periods_histogram
import romz_plot_shedule_stacked_histogram
import romz_plot_task
import romz_plot_tasks_gantt
import romz_plot_tasks_per_day

def get_Hours_per_day():
    return global_data["misc"].loc[0, "Hours per day"]


def get_Today():
    return global_data["misc"].loc[0, "Today"]


def get_dpi():
    return int(global_data["misc"].loc[0, "dpi"])


def get_last_date():
    return (get_Today() + datetime.timedelta(days=int(global_data["DAY_NO"]))).date()

def get_tstart():
    return global_data["misc"].loc[0, "T:start"]


def get_tend():
    return global_data["misc"].loc[0, "T:end"]


def get_hstart():
    return global_data["misc"].loc[0, "H:start"]


def get_hend():
    return global_data["misc"].loc[0, "H:end"]


def show_tasks():
    st.subheader("Tasks definition", divider="blue")
    format = {'Start day': "{:%Y-%m-%d}", 'End day': "{:%Y-%m-%d}", 'Avg': "{:.2f}"}
    st.dataframe(global_data["tasks"].style.format(format), hide_index=True, use_container_width=True)


def show_links():
    st.subheader("Links", divider="blue")
    st.dataframe(global_data["links"].style.format(format), hide_index=True, use_container_width=True)


def show_xbday():
    st.subheader("Bounds xbday", divider="blue")
    format = {'Start day': "{:%Y-%m-%d}", 'End day': "{:%Y-%m-%d}"}
    st.dataframe(global_data["xbday"].style.format(format), hide_index=True, use_container_width=True)


def show_xbsum():
    st.subheader("Bounds xbsum", divider="blue")
    format = {'Start day': "{:%Y-%m-%d}", 'End day': "{:%Y-%m-%d}"}
    st.dataframe(global_data["xbsum"].style.format(format), hide_index=True, use_container_width=True)


def show_ubday():
    st.subheader("Bounds ubday", divider="blue")
    format = {'Start day': "{:%Y-%m-%d}", 'End day': "{:%Y-%m-%d}"}
    st.dataframe(global_data["ubday"].style.format(format), hide_index=True, use_container_width=True)


def show_ubsum():
    st.subheader("Bounds ubsum", divider="blue")
    format = {'Start day': "{:%Y-%m-%d}", 'End day': "{:%Y-%m-%d}"}
    st.dataframe(global_data["ubsum"].style.format(format), hide_index=True, use_container_width=True)


def show_experts():
    st.subheader("Experts names", divider="blue")
    st.dataframe(global_data["experts"], hide_index=True, use_container_width=True)


def show_expert_bounds():
    st.subheader("Expert bounds and preferences", divider="blue")
    format = {'Start day': "{:%Y-%m-%d}", 'End day': "{:%Y-%m-%d}"}
    st.dataframe(global_data["expert bounds"].style.format(format), hide_index=True, use_container_width=True)


def show_invoicing_periods():
    st.subheader("Invoicing periods", divider="blue")
    format = {'Start day': "{:%Y-%m-%d}", 'End day': "{:%Y-%m-%d}"}
    st.dataframe(global_data["invoicing periods"].style.format(format), hide_index=True, use_container_width=True)



def show_invoicing_periods_bounds():
    st.subheader("Invoicing periods bounds", divider="blue")
    st.dataframe(global_data["invoicing periods bounds"].style.format(format), hide_index=True, use_container_width=True)


def load_excel_file():
    st.subheader("Load a Excel data file", divider="blue")
    uploaded_file = st.file_uploader("Excel file required in format 'xlsx'")
    if uploaded_file == None:
        st.subheader(":red[Select Excel data file for scheduling investigation!]")
    st.caption("See the [Yumbo](https://github.com/romz-pl/yambo/tree/main/ampl-data-input-excel) GitHub repository for sample Excel input files.")
    return uploaded_file


def prepare_global_data(uploaded_file):
    global global_data

    if 'key:uploaded_file' in st.session_state:
        new_input = ( st.session_state['key:uploaded_file'] != uploaded_file )
    else:
        new_input = True

    if new_input:
        with tempfile.NamedTemporaryFile(suffix=".xlsx") as f:
            f.write(uploaded_file.getvalue())
            f.flush()
            global_data = romz_excel.read(f.name)
        st.session_state['key:global_data'] = global_data
        st.session_state['key:uploaded_file'] = uploaded_file
    else:
        global_data = st.session_state['key:global_data']

    return new_input


def get_tasks_for_expert(expert_name):
    tasks = global_data["tasks"]
    links = global_data["links"]
    tasks_for_expert = links[ links["Expert"] == expert_name ]
    mask = tasks["Name"].isin(tasks_for_expert["Task"].array)
    return tasks[mask]


def show_tasks_gantt_chart(expert_name):
    tasks = get_tasks_for_expert(expert_name)
    work_done = global_data[f"schedule {expert_name}"].loc[tasks["Name"]].sum(axis=1)
    romz_plot_tasks_gantt.plot(tasks, work_done, get_dpi())


def show_tasks_per_day(expert_name):
    schedule = global_data[f"schedule {expert_name}"]
    romz_plot_tasks_per_day.plot(schedule, get_tstart(), get_tend(), get_dpi())


def show_invoice_period_workload(expert_name):
    invper = global_data["invoicing periods"]
    schedule = global_data[f"schedule {expert_name}"]
    invper_bounds = global_data["invoicing periods bounds"]
    bounds = invper_bounds[ invper_bounds["Expert"] == expert_name ]
    romz_plot_invoicing_periods_histogram.plot(invper, schedule, bounds, get_dpi())


def show_hours_per_day(expert_name):
    start = get_tstart()
    end = get_tend()
    data = global_data[f"schedule {expert_name}"]
    romz_plot_hours_per_day.plot(data, start, end, get_dpi())


def show_hours_per_day_stacked(expert_name):
    start = get_tstart()
    end = get_tend()
    data = global_data[f"schedule {expert_name}"]
    if romz_datetime.length_workdays(start, end, global_data["public holidays"]) > 10:
        width = 1
    else:
        width = 0.9
    romz_plot_shedule_stacked_histogram.plot(data, start, end, width, get_dpi())


def show_schedule_as_table(expert_name):
    tasks = get_tasks_for_expert(expert_name)
    start_date = romz_datetime.to_string(tasks["Start day"].min())
    end_date = romz_datetime.to_string(tasks["End day"].max())
    df = global_data[f"schedule {expert_name}"]
    df = df.loc[tasks["Name"].to_list(), start_date : end_date ]

    df = df.style.highlight_between(left=0.5, right=None, props='color:white; background-color:purple;')\
                 .highlight_between(left=None, right=0.5, props='color:white; background-color:white;')
    st.dataframe(df)


def show_commitment_per_task(expert_name):
    tasks_for_expert = get_tasks_for_expert(expert_name)
    col1, col2, col3 = st.columns(3)
    j = 0
    for idx in tasks_for_expert.index:
        j += 1
        task = tasks_for_expert.loc[idx]
        schedule = global_data[f"schedule {expert_name}"]
        xbday = global_data["xbday"]
        bounds = xbday.loc[ xbday["Task"] == task["Name"]].loc[ xbday["Expert"] == expert_name]
        with col1:
            if(j % 3 == 1):
                romz_plot_task.plot(task, schedule, bounds, get_dpi())

        with col2:
            if(j % 3 == 2):
                romz_plot_task.plot(task, schedule, bounds, get_dpi())

        with col3:
            if(j % 3 == 0):
                romz_plot_task.plot(task, schedule, bounds, get_dpi())


def customise_report():
    st.subheader("Customise report", divider="blue")
    max_col_no = 4
    report_column_no = st.number_input("Number of columns", min_value=1, max_value=max_col_no)

    for ii in range(1, max_col_no + 1):
        global_data[f"report_column_{ii}"] = st.selectbox(
            f"Col {ii}",
            ("Task's Gantt chart", "Tasks per day", "Hours per day", "Hours per day stacked", "Invoice period workload"),
            disabled= (ii > report_column_no)
        )
    global_data["report_column_no"] = report_column_no

    show_all_experts = st.checkbox("Show all experts?")

    expert = global_data["experts"]["Name"].to_numpy()
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

    global_data["report"] = edited_df

    global_data["show_experts_overview"] = st.checkbox("Show experts overview?")


def show_sidebar(uploaded_file):
    new_input = prepare_global_data(uploaded_file)
    st.subheader("Today: :green[{}]".format(get_Today().date()), divider="blue")
    st.subheader("Hours per day: :green[{}]".format(get_Hours_per_day()), divider="blue")
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
    romz_plot_tasks_gantt.plot_summary(global_data["tasks"], get_dpi())


def show_tasks_per_day_summary():
    dfs = [ global_data[f"schedule {e}"]  for e in global_data["experts"]["Name"] ]
    #start = get_Today() + datetime.timedelta(days=1)
    #end = get_Today() + datetime.timedelta(days=int(global_data["DAY_NO"]))
    romz_plot_tasks_per_day.plot(sum(dfs), get_tstart(), get_tend(), get_dpi())


def show_hours_per_day_summary():
    dfs = [ global_data[f"schedule {e}"]  for e in global_data["experts"]["Name"] ]
    #start = get_Today() + datetime.timedelta(days=1)
    #end = get_Today() + datetime.timedelta(days=int(global_data["DAY_NO"]))
    romz_plot_hours_per_day.plot(sum(dfs), get_hstart(), get_hend(), get_dpi())


def show_summary():
    if global_data["show_experts_overview"]:
        st.subheader(":blue[Experts overview]", divider="blue")
        col1, col2, col3 = st.columns(3)
        with col1:
            show_tasks_gantt_chart_summary()
        with col2:
            show_tasks_per_day_summary()
        with col3:
            show_hours_per_day_summary()

def show_solver_output():
    st.subheader(f":green[Solver output at {global_data['solver timestamp']}]", divider="blue")
    st.code(global_data["solver output"])

def show_one_row(expert_name):
    report_column_no = global_data["report_column_no"]
    col_list = st.columns(report_column_no)
    for ii, col in enumerate(col_list):
        with col:
            chart_name  = global_data[f"report_column_{ii+1}"]
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

    experts = global_data["experts"]
    for e in experts.index:
        expert_name = experts.loc[e, "Name"]
        st.subheader(":blue[{name}] {comment}".format(name=expert_name, comment=experts.loc[e, "Comment"]), divider="blue")
        if global_data["report"].loc[expert_name, "Show?"]:
            show_one_row(expert_name)

            if global_data["report"].loc[expert_name, "Table?"]:
                show_schedule_as_table(expert_name)

            if global_data["report"].loc[expert_name, "Commitment?"]:
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

def main():
    # plt.style.use('seaborn-v0_8-whitegrid')
    set_page_config()
    show_page_header()
    global global_data

    with st.sidebar:
        uploaded_file = load_excel_file()
        if uploaded_file == None:
            return
        new_input = show_sidebar(uploaded_file)

    if new_input:
        try:
            romz_ampl.solve(uploaded_file.name, get_Today(), global_data)
        except Exception as e:
            st.subheader(":red[Exception during solving process.] {m}".format(m=repr(e)))
            return

    show_main_panel()


######################## CALL MAIN FUNCTION ##################

if __name__ == "__main__":
    main()


