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
    max_col_no = 4
    report_column_no = st.number_input("Number of columns", min_value=1, max_value=max_col_no, value=4)

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

    glb.data["report"] = st.data_editor(
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





def customise_date_range():
    st.subheader("Date ranges", divider="blue")

    rowa = st.columns(3)
    rowa[0].write("Tasks per day")
    glb.data["timg"]["Start"] = rowa[1].date_input("timg:Start", format="YYYY-MM-DD", min_value=glb.tomorrow(), max_value=glb.last_day(), label_visibility="collapsed", value=glb.timg("Start"))
    glb.data["timg"]["End"]   = rowa[2].date_input("timg:End"  , format="YYYY-MM-DD", min_value=glb.tomorrow(), max_value=glb.last_day(), label_visibility="collapsed", value=glb.timg("End"))


    rowb = st.columns(3)
    rowb[0].write("Tasks per day stacked")
    glb.data["simg"]["Start"] = rowb[1].date_input("simg:Start", format="YYYY-MM-DD", min_value=glb.tomorrow(), max_value=glb.last_day(), label_visibility="collapsed", value=glb.simg("Start"))
    glb.data["simg"]["End"]   = rowb[2].date_input("simg:End"  , format="YYYY-MM-DD", min_value=glb.tomorrow(), max_value=glb.last_day(), label_visibility="collapsed", value=glb.simg("End"))


    rowc = st.columns(3)
    rowc[0].write("Hours per day")
    glb.data["himg"]["Start"] = rowc[1].date_input("himg:Start", format="YYYY-MM-DD", min_value=glb.tomorrow(), max_value=glb.last_day(), label_visibility="collapsed", value=glb.himg("Start"))
    glb.data["himg"]["End"]   = rowc[2].date_input("himg:End"  , format="YYYY-MM-DD", min_value=glb.tomorrow(), max_value=glb.last_day(), label_visibility="collapsed", value=glb.himg("End"))

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

