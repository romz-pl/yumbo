import numpy as np
import pandas as pd
import streamlit as st

import glb

def get_uploaded_file():
    st.subheader("Load Excel data file", divider="blue")

    uploaded_file = st.file_uploader("Excel file required in format 'xlsx'", label_visibility="collapsed")
    if uploaded_file == None:
        st.subheader(":red[Select Excel data file for scheduling investigation!]")

    # st.markdown("See the [Yumbo](https://github.com/romz-pl/yambo/tree/main/ampl-data-input-excel) GitHub repository for sample Excel input files.")
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


def init_show_experts():
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

    return df

def customise_show_experts():
    st.subheader("Look and feel", divider="blue")

    df = init_show_experts()

    # Use Streamlit data editor with configuration for interaction
    st.session_state.show["experts"] = st.data_editor(
        df,
        hide_index=False,
        use_container_width=True,
        column_config={
            "Expert": st.column_config.TextColumn(disabled=True, pinned=True),
            **{col: st.column_config.CheckboxColumn() for col in df.columns},
        },
    )


def init_show_tasks():
    # Extract tasks names and define row/column counts
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

    return df


def customise_show_tasks():
    st.subheader("Look and feel", divider="blue")

    # Use Streamlit data editor with configuration for interaction
    df = init_show_tasks()
    st.session_state.show["tasks"] = st.data_editor(
        df,
        hide_index=False,
        use_container_width=True,
        column_config={
            "Task": st.column_config.TextColumn(disabled=True, pinned=True),
            **{col: st.column_config.CheckboxColumn() for col in df.columns},
        },
    )


def customise_date_range():
    st.subheader("Date ranges", divider="blue")

    # Mapping data keys to labels
    sections = {
        ("imgt", "Tasks per day"),
        ("imgs", "Tasks per day stacked"),
        ("imgh", "Hours per day")
    }

    mprob = st.session_state.mprob
    for key, label in sections:
        row = st.columns(3)
        row[0].write(label)

        mprob[key].loc[0, "Start"] = row[1].date_input(
            f"{key}:Start",
            format="YYYY-MM-DD",
            min_value=glb.tomorrow(),
            max_value=glb.last_day(),
            label_visibility="collapsed",
            value=mprob[key].loc[0, "Start_init"],
        )

        mprob[key]["End"] = row[2].date_input(
            f"{key}:End",
            format="YYYY-MM-DD",
            min_value=glb.tomorrow(),
            max_value=glb.last_day(),
            label_visibility="collapsed",
            value=mprob[key].loc[0, "End_init"],
        )

def customise_chart_colours():
    st.subheader("Colours", divider="blue")

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




def customise_task():
    customise_task_report_layout()
    customise_show_tasks()


def show_planing_horizon():
    st.subheader(f"Planing horizon", divider="blue")
    st.markdown(f"Today: :green[{glb.today().date()}]")
    st.markdown(f"Tomorrow: :green[{glb.tomorrow().date()}]")
    st.markdown(f"Last day: :green[{glb.last_day().date()}]")
    st.markdown(f"Number of days: :green[{(glb.last_day() - glb.today()).days}]")


def customise_summary():
    st.subheader("Report layout", divider="blue")

    show = st.session_state.show
    show["experts_summary"] = st.checkbox("Experts summary", value=True)


def customise_problem():
    st.subheader("Report layout", divider="blue")

    show = st.session_state.show
    show["problem"] = st.checkbox("Problem definition", value=False)


def customise_stats():
    st.subheader("Report layout", divider="blue")

    show = st.session_state.show
    show["stats_chart"] = st.checkbox("Statistics on chart creation", value=True)
    show["stats_execution"] = st.checkbox("Statistics on Yumbo execution", value=True)


def customise_size_and_dpi():
    st.subheader("Size and DPI", divider="blue")

    with st.form("my_form"):
        height = st.slider("Height", min_value=1.0, max_value=12.0, value=3.0, step=0.1, format="%.1f")
        width = st.slider("Width", min_value=1.0, max_value=12.0, value=3.0, step=0.1, format="%.1f")
        dpi = st.slider("Dpi", min_value=10, max_value=600, value=96, step=1)

        submitted = st.form_submit_button("Set sizes and DPI")
        if submitted:
            img_type = ["imgh", "imgt", "imgs", "imgg", "imgw", "imgb", "imge"]
            for img in img_type:
                st.session_state.mprob[img].loc[0, "Height"] = height
                st.session_state.mprob[img].loc[0, "Width"] = width
                st.session_state.mprob[img].loc[0, "Dpi"] = dpi


def customise_chart():
    st.session_state.show["days_off"] = st.checkbox(f"Show days off", value=False)

    customise_chart_colours()
    customise_date_range()
    customise_size_and_dpi()



def show():

    # st.divider()

    tab = st.tabs(["**Expert**", "**Task**", "**Summary**", "**AMPL**", "**Problem**", "**Stats**", "**Chart**", "**Horizon**"])
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
    with tab[6]:
        customise_chart()
    with tab[7]:
        show_planing_horizon()

