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
import romz_plot_shedule_stacked_histogram
import romz_plot_tasks_gantt
import romz_plot_tasks_per_day


def read_experts():
    st.subheader("Load a Excel data file", divider=True)
    uploaded_file = st.file_uploader("Excel file required")

    if uploaded_file:
        excel_filename = uploaded_file.name
        with tempfile.NamedTemporaryFile(suffix=".xlsx") as f:
            f.write(uploaded_file.getvalue())
            f.flush()
            return pd.read_excel(f.name, sheet_name="experts")

    return pd.DataFrame()


def show_hours_per_day(idx, use_stacked):
    today = get_TODAY().date()
    tomorrow = today + datetime.timedelta(days=1)
    format = "YYYY-MM-DD"

    cola, colb = st.columns(2)
    with cola:
        v = tomorrow
        start = st.date_input("Start date", v, format=format, min_value=tomorrow, key=f"schedule_start_{idx}")
    with colb:
        v = today + datetime.timedelta(days=int(global_data["DAY NO"]))
        end = st.date_input("End date", v, format=format, min_value=tomorrow, key=f"schedule_end_{idx}")

    if use_stacked:
        if romz_datetime.length_workdays(start, end, global_data["public holidays"]) > 10:
            width = 1
        else:
            width = 0.9
        romz_plot_shedule_stacked_histogram.plot(global_data, start, end, width)
    else:
        romz_plot_hours_per_day.plot(global_data, start, end)


def show_tasks_per_day(idx):
    today = get_TODAY().date()
    tomorrow = today + datetime.timedelta(days=1)
    format = "YYYY-MM-DD"

    cola, colb = st.columns(2)
    with cola:
        v = tomorrow
        start = st.date_input("Start date", v, format=format, min_value=tomorrow, key=f"tasks_start_{idx}")
    with colb:
        v = today + datetime.timedelta(days=int(global_data["DAY NO"]))
        end = st.date_input("End date", v, format=format, min_value=tomorrow, key=f"tasks_end_{idx}")

    romz_plot_tasks_per_day.plot(global_data, start, end)


def get_TODAY():
    return global_data["misc"].loc[0, "TODAY"]


def show_page_header():
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Zbigniew Romanowski romz@wp.pl")
        st.subheader("Paweł Koczyk pk@koczyk.pl")
    with col2:
        st.subheader("Date and time: _{d}_".format(d=datetime.datetime.now().strftime("%d %B %Y, %H:%M:%S %p")))
    st.divider()


def shoe_tasks_definition(use_gant):
    if use_gant:
        romz_plot_tasks_gantt.plot(global_data)
    else:
        st.subheader("Tasks definition", divider=True)
        format = {'Start day': "{:%Y-%m-%d}", 'End day': "{:%Y-%m-%d}", 'Avg': "{:.2f}"}
        st.dataframe(global_data["tasks"].style.format(format), hide_index=True, use_container_width=True)


def main():
    st.set_page_config(page_title="Scheduling and palnning",layout="wide")
    st.title("OBELIX: Scheduling, Planning and Resource Allocation")
    show_page_header()

    with st.sidebar:
        global global_data
        df = read_experts()
        st.divider()
        st.subheader("Paths to Excel files", divider=True)
        st.dataframe(df, hide_index=True, use_container_width=True)
        st.subheader("Customise report", divider=True)
        use_stacked = st.checkbox("Show schedule as stack histogram")
        use_gant = st.checkbox("Show tasks on the Gantt chart", value = 1)


    for j in df.index:
        st.subheader("{Name}, {Path}".format(Name=df.loc[j, "Name"], Path=df.loc[j, "Path"]), divider=True)
        excel_filename = df.loc[j, "Path"]
        global_data = romz_excel.read(excel_filename)
        ampl_data_file = romz_ampl.data_file(excel_filename, get_TODAY(), global_data)
        romz_ampl.solve(ampl_data_file, global_data)

        col1, col2, col3 = st.columns(3)
        with col1:
            shoe_tasks_definition(use_gant)

        with col2:
            show_tasks_per_day(j)
        with col3:
            show_hours_per_day(j, use_stacked)



######################## CALL MAIN FUNCTION ##################

main()


