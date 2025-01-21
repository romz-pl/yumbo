import glb
import numpy as np
import pandas as pd
import romz_datetime
import streamlit as st

def load_excel_file():
    st.subheader("Load a Excel data file", divider="blue")
    uploaded_file = st.file_uploader("Excel file required in format 'xlsx'")
    if uploaded_file == None:
        st.subheader(":red[Select Excel data file for scheduling investigation!]")
    st.caption("See the [Yumbo](https://github.com/romz-pl/yambo/tree/main/ampl-data-input-excel) GitHub repository for sample Excel input files.")
    return uploaded_file


def customise_report_layout():
    st.subheader("Report layout", divider="blue")
    glb.data["show_experts_overview"] = st.checkbox("Show experts overview?", value=True)
    max_col_no = 5
    report_column_no = st.number_input("Number of columns", min_value=1, max_value=max_col_no, value=max_col_no)

    for ii in range(1, max_col_no + 1):
        glb.data[f"report_column_{ii}"] = st.selectbox(
            f"Col {ii}",
            ("Task's Gantt chart", "Tasks per day", "Hours per day stacked", "Hours per day", "Invoice period workload"),
            disabled = (ii > report_column_no),
            index = (ii - 1),
            label_visibility = "collapsed",
        )
    glb.data["report_column_no"] = report_column_no


def customise_show_experts():
    st.subheader("Look and feel", divider="blue")

    # Extract expert names and define row/column counts
    experts = glb.data["experts"]["Name"].to_numpy()
    row_count = len(experts)

    # Create a DataFrame with predefined columns and default boolean values
    names = ["Charts", "Table", "Commitment"]
    df = pd.DataFrame(False, index=experts, columns=names)
    df.index.name = "Expert"

    # Sort the DataFrame by index (expert names)
    df.sort_index(inplace=True)

    # Update column values based on user input from Streamlit checkboxes
    df[names[0]] = st.checkbox(f"Show {names[0]}", value=True)
    df[names[1]] = st.checkbox(f"Show {names[1]}", value=False)
    df[names[2]] = st.checkbox(f"Show {names[2]}", value=False)

    # Use Streamlit data editor with configuration for interaction
    glb.data["report"] = st.data_editor(
        df,
        hide_index=True,
        use_container_width=True,
        column_config={
            "Expert": st.column_config.TextColumn(disabled=True, pinned=True),
            **{col: st.column_config.CheckboxColumn() for col in names},
        },
    )


def customise_date_range():
    st.subheader("Date ranges", divider="blue")

    # Mapping data keys to labels
    sections = {
        "timg": "Tasks per day",
        "simg": "Tasks per day stacked",
        "himg": "Hours per day",
    }

    for key, label in sections.items():
        row = st.columns(3)
        row[0].write(label)
        glb.data[key]["Start"] = row[1].date_input(
            f"{key}:Start",
            format="YYYY-MM-DD",
            min_value=glb.tomorrow(),
            max_value=glb.last_day(),
            label_visibility="collapsed",
            value=getattr(glb, key)("Start"),
        )
        glb.data[key]["End"] = row[2].date_input(
            f"{key}:End",
            format="YYYY-MM-DD",
            min_value=glb.tomorrow(),
            max_value=glb.last_day(),
            label_visibility="collapsed",
            value=getattr(glb, key)("End"),
        )


def customise_report():
    customise_report_layout()
    customise_show_experts()
    customise_date_range()


def show_tasks():
    st.subheader("Tasks definition", divider="blue")
    format = {'Start': "{:%Y-%m-%d}", 'End': "{:%Y-%m-%d}", 'Avg': "{:.4f}"}
    df = glb.data["tasks"].style.format(format)
    st.dataframe(df, hide_index=True, use_container_width=True)


def show_experts():
    st.subheader("Experts names", divider="blue")
    st.dataframe(glb.data["experts"], hide_index=True, use_container_width=True)


def show_links():
    st.subheader("Links", divider="blue")
    st.dataframe(glb.data["links"], hide_index=True, use_container_width=True)


def show_xbday():
    st.subheader("Bounds xbday", divider="blue")
    format = {'Start': "{:%Y-%m-%d}", 'End': "{:%Y-%m-%d}"}
    df = glb.data["xbday"].style.format(format)
    st.dataframe(df, hide_index=True, use_container_width=True)


def show_xbsum():
    st.subheader("Bounds xbsum", divider="blue")
    format = {'Start': "{:%Y-%m-%d}", 'End': "{:%Y-%m-%d}"}
    df = glb.data["xbsum"].style.format(format)
    st.dataframe(df, hide_index=True, use_container_width=True)


def show_ubday():
    st.subheader("Bounds ubday", divider="blue")
    format = {'Start': "{:%Y-%m-%d}", 'End': "{:%Y-%m-%d}"}
    df = glb.data["ubday"].style.format(format)
    st.dataframe(df, hide_index=True, use_container_width=True)


def show_ubsum():
    st.subheader("Bounds ubsum", divider="blue")
    format = {'Start': "{:%Y-%m-%d}", 'End': "{:%Y-%m-%d}"}
    df = glb.data["ubsum"].style.format(format)
    st.dataframe(df, hide_index=True, use_container_width=True)


def show_expert_bounds():
    st.subheader("Expert bounds and preferences", divider="blue")
    format = {'Start': "{:%Y-%m-%d}", 'End': "{:%Y-%m-%d}"}
    df = glb.data["expert bounds"].style.format(format)
    st.dataframe(df, hide_index=True, use_container_width=True)


def show_invoicing_periods():
    st.subheader("Invoicing periods", divider="blue")
    format = {'Start': "{:%Y-%m-%d}", 'End': "{:%Y-%m-%d}"}
    df = glb.data["invoicing periods"].style.format(format)
    st.dataframe(df, hide_index=True, use_container_width=True)


def show_invoicing_periods_bounds():
    st.subheader("Invoicing periods bounds", divider="blue")
    st.dataframe(glb.data["invoicing periods bounds"], hide_index=True, use_container_width=True)


def show(uploaded_file):
    new_input = glb.prepare(uploaded_file)
    st.subheader(f"Planing horizon", divider="blue")
    st.caption(f"Today: :green[{glb.today().date()}]")
    st.caption(f"Tomorrow: :green[{glb.tomorrow().date()}]")
    st.caption(f"Last day: :green[{glb.last_day().date()}]")

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

