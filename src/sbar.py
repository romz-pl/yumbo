import numpy as np
import pandas as pd
import streamlit as st

import glb

def get_uploaded_file():
    st.subheader("Load Excel data file", divider="blue")

    uploaded_file = st.file_uploader("Excel file required in format 'xlsx'")
    if uploaded_file == None:
        st.subheader(":red[Select Excel data file for scheduling investigation!]")

    st.markdown("See the [Yumbo](https://github.com/romz-pl/yambo/tree/main/ampl-data-input-excel) GitHub repository for sample Excel input files.")
    return uploaded_file


def customise_expert_report_layout():
    st.subheader("Report layout", divider="blue")

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
    df[names[0]] = st.checkbox(f"Show {names[0]}", value=False , key=f"expert_{names[0]}")
    df[names[1]] = st.checkbox(f"Show {names[1]}", value=False, key=f"expert_{names[1]}")
    df[names[2]] = st.checkbox(f"Show {names[2]}", value=False, key=f"expert_{names[2]}")

    st.session_state.glb["days_off"] = st.checkbox(f"Include days off", value=False)

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
    df[names[0]] = st.checkbox(f"All reports", value=False , key=f"task_{names[0]}")


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
        ("imgt", "Tasks per day", glb.imgt),
        ("imgs", "Tasks per day stacked", glb.imgs),
        ("imgh", "Hours per day", glb.imgh)
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
        ("imgt", "Tasks per day", "Bar:color", glb.imgt),
        ("imgh", "Hours per day", "Bar:color", glb.imgh),
        ("imgg", "Task's Gantt Chart", "Barh:color", glb.imgg),
        ("imgw", "Invoicing Periods Workload", "Bar:color", glb.imgw),
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


def customise_ampl():
    st.subheader("Report layout", divider="blue")
    show = st.session_state.show

    show["ampl_solver_log"] = st.checkbox("Solver log", value=False)
    show["ampl_data_file"] = st.checkbox("AMPL data file", value=False)
    show["ampl_model_file"] = st.checkbox("AMPL model file", value=False)


def customise_expert():
    customise_expert_report_layout()
    customise_show_experts()
    customise_date_range()
    customise_chart_colours()


def customise_task():
    customise_task_report_layout()
    customise_show_tasks()

def show_planing_horizon():
    st.divider()
    st.subheader(f"Planing horizon", divider="blue")
    st.markdown(f"Today: :green[{glb.today().date()}]")
    st.markdown(f"Tomorrow: :green[{glb.tomorrow().date()}]")
    st.markdown(f"Last day: :green[{glb.last_day().date()}]")
    st.markdown(f"Number of days: :green[{(glb.last_day() - glb.today()).days}]")


def customise_summary():
    st.subheader("Report layout", divider="blue")
    st.session_state.show["experts_summary"] = st.checkbox("Experts summary", value=True)


def customise_problem():
    st.subheader("Report layout", divider="blue")
    st.session_state.show["problem"] = st.checkbox("Problem definition", value=False)


def customise_stats():
    st.subheader("Report layout", divider="blue")
    st.session_state.show["stats_chart"] = st.checkbox("Statistics on chart creation", value=True)
    st.session_state.show["stats_execution"] = st.checkbox("Statistics on Yumbo execution", value=True)


def show():
    show_planing_horizon()
    st.divider()

    tab = st.tabs(["**Experts**", "**Tasks**", "**Summary**", "**AMPL**", "**Problem**", "**Stats**"])
    with tab[0]:
        customise_expert()
    with tab[1]:
        customise_task()
    with tab[2]:
        customise_summary()
    with tab[3]:
        customise_ampl()
    with tab[4]:
        customise_problem()
    with tab[5]:
        customise_stats()

