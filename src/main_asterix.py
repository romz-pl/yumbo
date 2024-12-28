import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
import numpy as np
import pandas as pd
import streamlit as st
import tempfile
from pathlib import Path

import romz_ampl
import romz_datetime
import romz_excel
import romz_plot_hours_per_day
import romz_plot_invoicing_periods_gantt
import romz_plot_invoicing_periods_histogram
import romz_plot_shedule_stacked_histogram
import romz_plot_task
import romz_plot_tasks_gantt
import romz_plot_tasks_per_day


def show_complete_planing_horizon():
    st.subheader("Complete planing horizon", divider=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        romz_plot_hours_per_day.plot(global_data)

    with col2:
        romz_plot_tasks_per_day.plot(global_data)

    with col3:
        romz_plot_invoicing_periods_histogram.plot(global_data)


def show_commitment_per_task():
    st.subheader("Commitment per task", divider=True)
    col1, col2, col3 = st.columns(3)
    j = 0
    for idx in global_data["tasks"].index:
        j += 1
        with col1:
            if(j % 3 == 1):
                romz_plot_task.plot(idx, global_data)

        with col2:
            if(j % 3 == 2):
                romz_plot_task.plot(idx, global_data)

        with col3:
            if(j % 3 == 0):
                romz_plot_task.plot(idx, global_data)



def show_invoicing_periods():
    st.subheader("Invoicing periods", divider=True)
    format = {'Start day': "{:%Y-%m-%d}", 'End day': "{:%Y-%m-%d}"}
    st.dataframe(global_data["invoicing periods"].style.format(format), hide_index=True, use_container_width=True)


def show_tasks():
    st.subheader("Tasks definition", divider=True)
    format = {'Start day': "{:%Y-%m-%d}", 'End day': "{:%Y-%m-%d}", 'Avg': "{:.2f}"}
    st.dataframe(global_data["tasks"].style.format(format), hide_index=True, use_container_width=True)


def show_task_bounds():
    st.subheader("Task bounds", divider=True)
    format = {'Start day': "{:%Y-%m-%d}", 'End day': "{:%Y-%m-%d}"}
    st.dataframe(global_data["task bounds"].style.format(format), hide_index=True, use_container_width=True)


def show_expert_bounds():
    st.subheader("Expert bounds and preferences", divider=True)
    format = {'Start day': "{:%Y-%m-%d}", 'End day': "{:%Y-%m-%d}"}
    st.dataframe(global_data["expert bounds"].style.format(format), hide_index=True, use_container_width=True)


def prepare_global_data():
    st.subheader("Load a Excel data file", divider=True)
    uploaded_file = st.file_uploader("Excel file required")

    global global_data

    if uploaded_file:
        excel_filename = uploaded_file.name
        with tempfile.NamedTemporaryFile(suffix=".xlsx") as f:
            f.write(uploaded_file.getvalue())
            f.flush()
            global_data = romz_excel.read(f.name)
    else:
        excel_filename = "PM-01-no-bounds.xlsx"
        path = "../ampl-data-input-excel/{name}".format(name=excel_filename)
        global_data = romz_excel.read(path)

    return excel_filename



def show_schedule_dataframe():
    st.subheader("Schedule in the form of a table", divider=True)
    df = global_data["schedule"]
    df = df.style.highlight_between(left=0.5, right=None, props='color:white; background-color:purple;')\
                 .highlight_between(left=None, right=0.5, props='color:white; background-color:white;')
    st.dataframe(df)



def show_shedule_stacked_histogram():
    st.subheader("Schedule as a cumulative bar chart", divider=True)
    col1, col2, col3 = st.columns(3)

    today = get_TODAY().date()
    tomorrow = today + datetime.timedelta(days=1)
    format = "YYYY-MM-DD"

    with col1:
        cola, colb = st.columns(2)
        with cola:
            v = tomorrow
            start = st.date_input("Start date", v, format=format, min_value=tomorrow, key="date_col_1a")
        with colb:
            v = today + datetime.timedelta(days=5)
            end = st.date_input("End date", v, format=format, min_value=tomorrow, key="date_col_1b")

        romz_plot_shedule_stacked_histogram.plot(global_data, start, end, 0.9)

    with col2:
        cola, colb = st.columns(2)
        with cola:
            v = tomorrow
            start = st.date_input("Start date", v, format=format, min_value=tomorrow, key="date_col_2a")
        with colb:
            v = today + datetime.timedelta(days=28)
            end = st.date_input("End date", v, format=format, min_value=tomorrow, key="date_col_2b")

        romz_plot_shedule_stacked_histogram.plot(global_data, start, end, 1.0)

    with col3:
        cola, colb = st.columns(2)
        with cola:
            v = tomorrow
            start = st.date_input("Start date", v, format=format, min_value=tomorrow, key="date_col_3a")
        with colb:
            v = today + datetime.timedelta(days=int(global_data["DAY NO"]))
            end = st.date_input("End date", v, format=format, min_value=tomorrow, key="date_col_3b")

        romz_plot_shedule_stacked_histogram.plot(global_data, start, end, 1.0)


def show_problem_description():
    st.subheader("Problem description", divider=True)
    md_file = Path("../res/problem_description.md").read_text()
    st.markdown(md_file, unsafe_allow_html=True)


def show_tasks_and_invoicing_periods():
    st.subheader("Task and Invoicing periods", divider=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        romz_plot_tasks_gantt.plot(global_data)

    with col2:
        romz_plot_invoicing_periods_gantt.plot(global_data)

    with col3:
        st.image("../res/ampl_python_logos.svg", use_container_width=True)


def get_HOURS_PER_DAY():
    return global_data["misc"].loc[0, "HOURS PER DAY"]


def get_TODAY():
    return global_data["misc"].loc[0, "TODAY"]


def show_page_header(excel_filename):
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Zbigniew Romanowski romz@wp.pl")
        st.subheader("Paweł Koczyk pk@koczyk.pl")
    with col2:
        st.subheader("Exel input data file: _{f}_ ".format(f=excel_filename))
        st.subheader("Date and time: _{d}_".format(d=datetime.datetime.now().strftime("%d %B %Y, %H:%M:%S %p")))
    st.divider()


def main():
    st.set_page_config(page_title="Scheduling and palnning",layout="wide")
    st.title("ASTERIX: Scheduling, Planning and Resource Allocation")

    with st.sidebar:
        excel_filename = prepare_global_data()
        st.subheader("TODAY: {}".format(get_TODAY().date()), divider=True)
        st.subheader("Hours per day: {}".format(get_HOURS_PER_DAY()), divider=True)
        show_tasks()
        show_invoicing_periods()
        show_task_bounds()
        show_expert_bounds()
        ampl_data_file = romz_ampl.data_file(excel_filename, get_TODAY(), global_data)


    show_page_header(excel_filename)
    show_tasks_and_invoicing_periods()
    romz_ampl.solve(ampl_data_file, global_data)
    show_shedule_stacked_histogram()
    show_complete_planing_horizon()
    show_commitment_per_task()
    show_schedule_dataframe()
    show_problem_description()



######################## CALL MAIN FUNCTION ##################

main()


