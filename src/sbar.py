import glb
import numpy as np
import pandas as pd
import streamlit as st



def get_uploaded_file():
    st.subheader("Load a Excel data file", divider="blue")

    uploaded_file = st.file_uploader("Excel file required in format 'xlsx'")
    if uploaded_file == None:
        st.subheader(":red[Select Excel data file for scheduling investigation!]")

    st.caption("See the [Yumbo](https://github.com/romz-pl/yambo/tree/main/ampl-data-input-excel) GitHub repository for sample Excel input files.")
    return uploaded_file


def customise_expert_report_layout():
    st.subheader("Report layout", divider="blue")
    st.session_state.glb["show_experts_overview"] = st.checkbox("Show experts overview?", value=True)
    max_col_no = 5
    report_column_no = st.number_input("Number of columns", min_value=1, max_value=max_col_no, value=max_col_no)

    for ii in range(1, max_col_no + 1):
        st.session_state.glb[f"report_expert_column_{ii}"] = st.selectbox(
            f"Col {ii}",
            ("Task's Gantt chart", "Tasks per day", "Hours per day stacked", "Hours per day", "Invoice period workload"),
            disabled = (ii > report_column_no),
            index = (ii - 1),
            label_visibility = "collapsed",
        )
    st.session_state.glb["report_expert_column_no"] = report_column_no


def customise_task_report_layout():
    st.subheader("Report layout", divider="blue")
    max_col_no = 3
    report_column_no = st.number_input("Number of columns", min_value=1, max_value=max_col_no, value=1)

    for ii in range(1, max_col_no + 1):
        st.session_state.glb[f"report_task_column_{ii}"] = st.selectbox(
            f"Col {ii}",
            ("Experts per day stacked", "HTML table", "Simple table"),
            disabled = (ii > report_column_no),
            index = (ii - 1),
            label_visibility = "collapsed",
        )
    st.session_state.glb["report_task_column_no"] = report_column_no


def customise_show_experts():
    st.subheader("Look and feel", divider="blue")

    # Extract expert names and define row/column counts
    experts = st.session_state.mprob["expert"]["Name"].to_numpy()
    row_count = len(experts)

    # Create a DataFrame with predefined columns and default boolean values
    names = ["Charts", "Table", "Commitment"]
    df = pd.DataFrame(False, index=experts, columns=names)
    df.index.name = "Expert"

    # Sort the DataFrame by index (expert names)
    df.sort_index(inplace=True)

    # Update column values based on user input from Streamlit checkboxes
    df[names[0]] = st.checkbox(f"Show {names[0]}", value=True , key=f"expert_{names[0]}")
    df[names[1]] = st.checkbox(f"Show {names[1]}", value=False, key=f"expert_{names[1]}")
    df[names[2]] = st.checkbox(f"Show {names[2]}", value=False, key=f"expert_{names[2]}")

    # Use Streamlit data editor with configuration for interaction
    st.session_state.glb["report:experts"] = st.data_editor(
        df,
        hide_index=True,
        use_container_width=True,
        column_config={
            "Expert": st.column_config.TextColumn(disabled=True, pinned=True),
            **{col: st.column_config.CheckboxColumn() for col in names},
        },
    )


def customise_show_tasks():
    st.subheader("Look and feel", divider="blue")

    # Extract expert names and define row/column counts
    tasks = st.session_state.mprob["task"]["Name"].to_numpy()
    row_count = len(tasks)

    # Create a DataFrame with predefined columns and default boolean values
    names = ["Report"]
    df = pd.DataFrame(False, index=tasks, columns=names)
    df.index.name = "Task"

    # Sort the DataFrame by index (task names)
    df.sort_index(inplace=True)

    # Update column values based on user input from Streamlit checkboxes
    df[names[0]] = st.checkbox(f"Show all reports", value=False , key=f"task_{names[0]}")


    # Use Streamlit data editor with configuration for interaction
    st.session_state.glb["report:tasks"] = st.data_editor(
        df,
        hide_index=True,
        use_container_width=True,
        column_config={
            "Task": st.column_config.TextColumn(disabled=True, pinned=True),
            **{col: st.column_config.CheckboxColumn() for col in names},
        },
    )


def customise_date_range():
    st.subheader("Date ranges", divider="blue")

    # Mapping data keys to labels
    sections = {
        ("timg", "Tasks per day", glb.timg),
        ("simg", "Tasks per day stacked", glb.simg),
        ("himg", "Hours per day", glb.himg)
    }

    mprob = st.session_state.mprob
    for key, label, fun in sections:
        row = st.columns(3)
        row[0].write(label)

        mprob[key]["Start"] = row[1].date_input(
            f"{key}:Start",
            format="YYYY-MM-DD",
            min_value=glb.tomorrow(),
            max_value=glb.last_day(),
            label_visibility="collapsed",
            value=fun("Start"),
        )

        mprob[key]["End"] = row[2].date_input(
            f"{key}:End",
            format="YYYY-MM-DD",
            min_value=glb.tomorrow(),
            max_value=glb.last_day(),
            label_visibility="collapsed",
            value=fun("End"),
        )

def customise_chart_colours():
    st.subheader("Chart colours", divider="blue")

    # Mapping data keys to labels
    sections = [
        ("timg", "Tasks per day", "Bar:color", glb.timg),
        ("himg", "Hours per day", "Bar:color", glb.himg),
        ("gimg", "Task's Gantt Chart", "Barh:color", glb.gimg),
        ("wimg", "Invoicing Periods Workload", "Bar:color", glb.wimg),
    ]

    mprob = st.session_state.mprob
    for key, label, col, fun in sections:
        row = st.columns(2)
        row[0].write(label)

        mprob[key][col] = row[1].color_picker(
            f"{key}:Color",
            label_visibility="collapsed",
            value=fun(col),

        )


def show_task():
    st.subheader("Tasks", divider="blue")
    format = {'Start': "{:%Y-%m-%d}", 'End': "{:%Y-%m-%d}", 'Avg': "{:.4f}"}
    df = st.session_state.mprob["task"].style.format(format)
    st.dataframe(df, hide_index=False, use_container_width=True)


def show_expert():
    st.subheader("Experts", divider="blue")
    st.dataframe(st.session_state.mprob["expert"], hide_index=False, use_container_width=True)


def show_assign():
    st.subheader("Assignment (allocation)", divider="blue")
    st.dataframe(st.session_state.mprob["assign"], hide_index=True, use_container_width=True)


def show_xbday():
    st.subheader("XBDAY bounds", divider="blue")
    format = {'Start': "{:%Y-%m-%d}", 'End': "{:%Y-%m-%d}"}
    df = st.session_state.mprob["xbday"].style.format(format)
    st.dataframe(df, hide_index=True, use_container_width=True)


def show_ubday():
    st.subheader("UBDAY bounds", divider="blue")
    format = {'Start': "{:%Y-%m-%d}", 'End': "{:%Y-%m-%d}"}
    df = st.session_state.mprob["ubday"].style.format(format)
    st.dataframe(df, hide_index=True, use_container_width=True)



def show_ebday():
    st.subheader("EBDAY bounds", divider="blue")
    format = {'Start': "{:%Y-%m-%d}", 'End': "{:%Y-%m-%d}"}
    df = st.session_state.mprob["ebday"].style.format(format)
    st.dataframe(df, hide_index=True, use_container_width=True)


def show_period():
    st.subheader("Periods", divider="blue")
    format = {'Start': "{:%Y-%m-%d}", 'End': "{:%Y-%m-%d}"}
    df = st.session_state.mprob["period"].style.format(format)
    st.dataframe(df, hide_index=True, use_container_width=True)


def show_pbsum():
    st.subheader("PBSUM bounds", divider="blue")
    st.dataframe(st.session_state.mprob["pbsum"], hide_index=True, use_container_width=True)


def show_problem():
    show_task()
    show_expert()
    show_assign()
    show_xbday()
    show_ubday()
    show_ebday()
    show_period()
    show_pbsum()
    st.session_state.glb["show_ampl_data_file"] = st.checkbox("Show AMPL data file?", value=False)


def customise_expert():
    customise_expert_report_layout()
    customise_show_experts()
    customise_date_range()
    customise_chart_colours()


def customise_task():
    customise_task_report_layout()
    customise_show_tasks()


def show():
    st.subheader(f"Planing horizon", divider="blue")
    st.caption(f"Today: :green[{glb.today().date()}]")
    st.caption(f"Tomorrow: :green[{glb.tomorrow().date()}]")
    st.caption(f"Last day: :green[{glb.last_day().date()}]")
    st.caption(f"Number of days: :green[{(glb.last_day() - glb.today()).days}]")

    st.divider()

    tab0, tab1, tab2 = st.tabs(["**Problem**", "**Experts**", "**Tasks**"])
    with tab0:
        show_problem()
    with tab1:
        customise_expert()
    with tab2:
        customise_task()

