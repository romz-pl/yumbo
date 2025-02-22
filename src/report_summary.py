import numpy as np
import pandas as pd
import os
import streamlit as st
import tempfile
import time
import uuid
import zipfile

import glb
import imggsum
import imghsum
import imgtsum
import styled_table


def show_charts():
    show = st.session_state.show

    b_list = [
        show["summary_tasks_gantt_chart"],
        show["summary_tasks_per_day"],
        show["summary_hours_per_day"],
    ]

    if not any(b_list):
        return

    days_off = show["days_off"]
    func_list = [imggsum.plot, imgtsum.plot, imghsum.plot]

    if show["summary_charts_in_one_column"]:
        # Loop through and plot charts in one column
        for func, show_chart in zip(func_list, b_list):
            if show_chart:
                func(days_off)
    else:
        # Create columns only for the charts that need to be shown
        col_list = st.columns(sum(b_list))
        col_index = 0

        for func, show_chart in zip(func_list, b_list):
            if show_chart:
                with col_list[col_index]:
                    func(days_off)
                col_index += 1


def show_overflow():
    task_overflows = st.session_state.show["summary_task_overflows"]

    if glb.is_ampl_model_overflow() and task_overflows:
        overflow = st.session_state.overflow
        if overflow.sum() > 0:
            st.subheader(":red[There are task overflows!]", divider="red")
            df = pd.DataFrame(overflow[ overflow > 0])
            format = {'Overflow': "{:.2f}"}
            df_styled = df.style.format(format)
            st.dataframe(df_styled)
        else:
            st.subheader(":green[There in no overflows]", divider="green")


@st.cache_resource(max_entries=1000)
def save_to_compressed_file(df, schedule_file_name):
    f_tmp = tempfile.NamedTemporaryFile(
        mode='w+',
        prefix="yumbo-",
        delete=False,
        delete_on_close=False,
    )
    f_tmp.close()

    csv = df.to_csv(index=False).encode("utf-8")
    ampl_data_file = st.session_state.mprob["ampl_data_file"]
    solver_log = st.session_state.stats["solver_log"]

    ampl_model_file = glb.get_ampl_model_file()
    with open(ampl_model_file, "r") as f:
        ampl_model = f.read()

    with open(ampl_model_file + ".run", "r") as f:
        ampl_model_run = f.read()

    with zipfile.ZipFile(f_tmp.name, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        zf.writestr(f"{schedule_file_name}.csv", csv)
        zf.writestr("ampl_data_file.dat", ampl_data_file)
        zf.writestr("solver_log.txt", solver_log)
        zf.writestr("model.ampl", ampl_model)
        zf.writestr("model.ampl.run", ampl_model_run)

    with open(f_tmp.name, "rb") as f:
        buf_zip = f.read()

    with zipfile.ZipFile(f_tmp.name, 'w', compression=zipfile.ZIP_BZIP2, compresslevel=9) as zf:
        zf.writestr(f"{schedule_file_name}.csv", csv)
        zf.writestr("ampl_data_file.dat", ampl_data_file)
        zf.writestr("solver_log.txt", solver_log)
        zf.writestr("model.ampl", ampl_model)
        zf.writestr("model.ampl.run", ampl_model_run)

    with open(f_tmp.name, "rb") as f:
        buf_bz2 = f.read()

    os.unlink(f_tmp.name)
    return buf_zip, buf_bz2



def download_results(df, schedule_file_name):
    buf_zip, buf_bz2 = save_to_compressed_file(df, schedule_file_name)

    file_name = f"{uuid.uuid4().hex}.zip"
    size_in_Kib = len(buf_zip) / 1024
    st.download_button(
        label=f"Download results :green[{file_name}] -> {size_in_Kib:,.1f} KiB",
        data=buf_zip,
        file_name=file_name,
    )

    file_name = f"{uuid.uuid4().hex}.bz2"
    size_in_Kib = len(buf_bz2) / 1024
    st.download_button(
        label=f"Download results :green[{file_name}] -> {size_in_Kib:,.1f} KiB",
        data=buf_bz2,
        file_name=file_name,
    )


@st.fragment()
def show_full_schedule(as_html):
    if not st.session_state.show["summary_full_schedule"]:
        return

    st.subheader(":green[Full schedule]", divider="green")

    if st.checkbox("Show as multiples of a quarter", value=False):
        df = (st.session_state.schedule * 4).astype("uint8")
        schedule_file_name = "schedule_quarters"
    else:
        df = st.session_state.schedule
        schedule_file_name = "schedule_hours"

    # .strftime('%a') Returns 'Mon', 'Tue', etc.
    # .strftime('%A') Returns 'Monday', 'Tuesday', etc.
    df.insert(0, "Weekday", df.index.strftime('%a'))
    df.insert(0, "Date", df.index.strftime(glb.format()))

    #
    # streamlit.errors.StreamlitAPIException:
    # The dataframe has 309748 cells, but the maximum number of cells allowed to be rendered by Pandas Styler is configured to 262144.
    # To allow more cells to be styled, you can change the "styler.render.max_elements" config.
    # For example: pd.set_option("styler.render.max_elements", 309748)
    #
    # Always display the dataframe as a Streamlit table without styles to avoid the above error.
    st.dataframe(df, use_container_width=False, hide_index=True)

    download_results(df, schedule_file_name)

    df.drop(columns="Date", inplace=True)
    df.drop(columns="Weekday", inplace=True)


def show_report():
    show = st.session_state.show

    # Extract relevant values from the session state
    b_list = [
        show["summary_tasks_gantt_chart"],
        show["summary_tasks_per_day"],
        show["summary_hours_per_day"],
        show["summary_task_overflows"],
        show["summary_full_schedule"],
    ]

    # Return early if no charts are to be shown
    if not any(b_list):
        return

    st.divider()
    st.header(":blue[Summary]", divider="blue")

    show_charts()
    show_overflow()
    show_full_schedule(False)


def show():
    time_start = time.perf_counter()
    show_report()
    time_end = time.perf_counter()
    st.session_state.stats["report_summary:ttime"] += time_end - time_start
