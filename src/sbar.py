import glb
import numpy as np
import pandas as pd
import streamlit as st

def load_excel_file():
    st.subheader("Load a Excel data file", divider="blue")
    uploaded_file = st.file_uploader("Excel file required in format 'xlsx'")
    if uploaded_file == None:
        st.subheader(":red[Select Excel data file for scheduling investigation!]")
    st.caption("See the [Yumbo](https://github.com/romz-pl/yambo/tree/main/ampl-data-input-excel) GitHub repository for sample Excel input files.")
    return uploaded_file


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

    df.sort_values(by="Expert", inplace=True)

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
    st.caption(f"Today: :green[{glb.today()}]")
    st.caption(f"Tomorrow: :green[{glb.tomorrow()}]")
    st.caption(f"Last day: :green[{glb.last_day()}]")
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

